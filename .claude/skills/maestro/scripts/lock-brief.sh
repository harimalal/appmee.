#!/usr/bin/env bash
# Verrouille brief.md après le GO de l'utilisateur : vérifie qu'il est complet, écrit son empreinte
# dans .brief.lock, passe etat.md à la phase 1.
# Usage : lock-brief.sh <dossier-de-mission>
#         lock-brief.sh <dossier-de-mission> --avenant "ce qui change et pourquoi"   (après verrouillage)
set -euo pipefail

fail() { echo "ÉCHEC : $*" >&2; exit 1; }

dir="${1:-}"; [ -n "$dir" ] && [ -d "$dir" ] || fail "usage : lock-brief.sh <dossier-de-mission> [--avenant \"texte\"]"
shift
avenant=""
if [ "${1:-}" = "--avenant" ]; then avenant="${2:-}"; [ -n "$avenant" ] || fail "--avenant demande un texte"; fi

brief="$dir/brief.md"; lock="$dir/.brief.lock"; etat="$dir/etat.md"
[ -f "$brief" ] || fail "brief.md introuvable dans $dir"

if [ -f "$lock" ] && [ -z "$avenant" ]; then
  fail "brief déjà verrouillé. Pour changer le périmètre : lock-brief.sh $dir --avenant \"ce qui change et pourquoi\""
fi
if [ ! -f "$lock" ] && [ -n "$avenant" ]; then
  fail "pas de verrouillage existant : verrouiller d'abord le brief, sans --avenant"
fi

# 1. Aucun champ à remplir ne doit rester
if grep -Fq '[[' "$brief"; then
  echo "Champs encore à remplir dans brief.md :" >&2
  grep -Fn '[[' "$brief" | head -15 >&2
  fail "brief incomplet"
fi

# 2. Verdict utilisable
verdict="$(sed -n 's/^verdict:[[:space:]]*//p' "$brief" | head -1 | sed 's/[[:space:]]*$//' | tr 'A-Z' 'a-z')"
case "$verdict" in
  "lancer"|"lancer sous condition") ;;
  *) fail "verdict « $verdict » : seuls « lancer » et « lancer sous condition » se verrouillent" ;;
esac

# 3. Sections obligatoires
missing=0
for h in "## À retenir" "## Objectif" "## Définition de « fini »" "## Livrables" "## Périmètre" "## Contraintes" \
         "## Décisions de fond" "## Doctrine d'arbitrage" "## Actions exigeant un accord humain" "## Options d'exécution" "## Avenants"; do
  if ! grep -Fq "$h" "$brief"; then echo "Section manquante : $h" >&2; missing=1; fi
done
[ "$missing" -eq 0 ] || fail "brief sans toutes ses sections"

date_iso="$(date +%F)"

if [ -n "$avenant" ]; then
  [ -z "$(tail -c1 "$brief")" ] || echo >> "$brief"
  echo "- $date_iso : $avenant" >> "$brief"
else
  sed -i -E "s/^verrouillé:.*/verrouillé: oui ($date_iso)/" "$brief"
fi

sha256sum "$brief" | awk '{print $1}' > "$lock"

# 4. État : phase 1 après le premier verrouillage, journal dans tous les cas
if [ -f "$etat" ]; then
  now="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  if [ -z "$avenant" ] && grep -q '^phase: 0' "$etat"; then
    sed -i -E "s/^phase:.*/phase: 1/; s/^prochaine_sous_tache:.*/prochaine_sous_tache: 1.0 — vérifier l'outillage puis benchmark/; s/^derniere_sous_tache_finie:.*/derniere_sous_tache_finie: 0 — cadrage et gate/" "$etat"
    echo "# $now — brief verrouillé après GO, passage en phase 1" >> "$etat"
  elif [ -n "$avenant" ]; then
    echo "# $now — avenant : $avenant" >> "$etat"
  fi
  sed -i -E "s/^maj:.*/maj: $now/" "$etat"
fi

if [ -n "$avenant" ]; then echo "Avenant enregistré, brief reverrouillé."; else echo "Brief verrouillé (verdict : $verdict). Empreinte écrite dans $lock."; fi
