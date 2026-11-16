#!/usr/bin/env bash
# Contrôle d'une mission MAESTRO : fichiers requis, état valide, empreinte du brief, placeholders, audit.
# Usage : check-mission.sh <dossier-de-mission> [--phase N]
#   --phase N : phase que l'on s'apprête à ouvrir ou à exécuter (par défaut : la phase de etat.md)
# Sortie : code 0 si tout est au vert, 1 sinon, avec la liste des problèmes.
# Les mots légitimes à ignorer dans les livrables (ex. un livrable sur les "TODO") : un mot par ligne
# dans <dossier>/.placeholder-allow
set -uo pipefail

dir="${1:-}"; [ -n "$dir" ] && [ -d "$dir" ] || { echo "usage : check-mission.sh <dossier-de-mission> [--phase N]" >&2; exit 2; }
shift
target=""
if [ "${1:-}" = "--phase" ]; then target="${2:-}"; fi

problems=()
bad() { problems+=("$*"); }

etat="$dir/etat.md"
field() { sed -n "s/^$1:[[:space:]]*//p" "$etat" 2>/dev/null | head -1 | sed 's/[[:space:]]*$//'; }

[ -f "$etat" ] || { echo "ÉCHEC : etat.md introuvable dans $dir" >&2; exit 1; }

mode="$(field mode)"; phase_etat="$(field phase)"; statut="$(field statut)"; maj="$(field maj)"
case "$mode" in eclair|standard|complete) ;; *) bad "etat.md : mode invalide « $mode »" ;; esac
case "$phase_etat" in 0|1|2|3|4|5|6) ;; *) bad "etat.md : phase invalide « $phase_etat »" ;; esac
case "$statut" in EN_COURS|BLOQUÉ|LIVRÉ) ;; *) bad "etat.md : statut invalide « $statut »" ;; esac
[ -n "$maj" ] || bad "etat.md : champ maj vide"
[ "$statut" != "BLOQUÉ" ] || echo "Attention : la mission est BLOQUÉE ($(field blocage))" >&2

P="${target:-$phase_etat}"
case "$P" in 0|1|2|3|4|5|6) ;; *) bad "phase demandée invalide « $P »"; P=0 ;; esac

need() { [ -f "$dir/$1" ] || bad "fichier requis manquant : $1 (phase $P)"; }

# Phase 0 et plus
need etat.md; need brief.md; need plan.md

# Phase 1 et plus : brief verrouillé et fichiers de cadrage
if [ "$P" -ge 1 ]; then
  if [ ! -f "$dir/.brief.lock" ]; then
    bad "brief non verrouillé : lancer lock-brief.sh après le GO"
  else
    now_hash="$(sha256sum "$dir/brief.md" 2>/dev/null | awk '{print $1}')"
    if [ "$now_hash" != "$(cat "$dir/.brief.lock")" ]; then
      bad "brief.md modifié après verrouillage : demander l'accord puis lock-brief.sh --avenant \"…\""
    fi
  fi
  grep -Fq '[[' "$dir/brief.md" 2>/dev/null && bad "brief.md contient encore des champs [[…]]"
  need BENCHMARK.md
  if [ "$mode" != "eclair" ]; then need TOOLING.md; need equipe.md; need decisions.md; fi
fi

# Phase 3 et plus : base benchmarkée, décisions, aucun placeholder
if [ "$P" -ge 3 ]; then
  if [ -f "$dir/BENCHMARK.md" ]; then
    grep -Eq '^## ' "$dir/BENCHMARK.md" || bad "BENCHMARK.md : aucune entrée (ni dispense motivée)"
    grep -Eq '^## <' "$dir/BENCHMARK.md" && bad "BENCHMARK.md : une entrée de gabarit « ## <…> » n'est pas remplie (la remplir ou la supprimer)"
  fi
  if [ "$mode" != "eclair" ] && [ -f "$dir/decisions.md" ]; then
    grep -Eq '^- CLÔTURE : [^<[:space:]]|Aucune décision structurante' "$dir/decisions.md" || bad "decisions.md : aucune clôture de décision réellement écrite (écrire « Aucune décision structurante » si c'est le cas)"
  fi
  if [ -d "$dir/livrables" ]; then
    pat='\b(todo|fixme|tbd|xxx)\b|lorem ipsum|à compléter|a completer|à remplir|a remplir|\[\[|\{\{|__[a-z]+__|placeholder'
    hits="$(grep -rIniE "$pat" "$dir/livrables" 2>/dev/null || true)"
    if [ -n "$hits" ] && [ -s "$dir/.placeholder-allow" ]; then
      hits="$(printf '%s\n' "$hits" | grep -vFf "$dir/.placeholder-allow" || true)"
    fi
    if [ -n "$hits" ]; then
      bad "placeholder dans les livrables :"$'\n'"$(printf '%s\n' "$hits" | head -10)"
    fi
  fi
fi

# Phase 4 et plus : au moins un livrable
entries=()
if [ -d "$dir/livrables" ]; then
  while IFS= read -r e; do entries+=("$e"); done < <(find "$dir/livrables" -mindepth 1 -maxdepth 1 ! -name '.*' -printf '%f\n' | sort)
fi
if [ "$P" -ge 4 ] && [ "${#entries[@]}" -eq 0 ]; then bad "livrables/ est vide"; fi

# Phase 5 et plus : audit et livraison
if [ "$P" -ge 5 ]; then
  need audit.md; need LIVRAISON.md
  for e in "${entries[@]}"; do
    if [ -f "$dir/audit.md" ]; then
      last="$(grep -F "$e" "$dir/audit.md" | tail -1 || true)"
      if [ -z "$last" ]; then bad "audit.md : aucune ligne pour $e"
      elif ! printf '%s' "$last" | grep -Fq '| OK |'; then bad "audit.md : la dernière passe de $e n'est pas « OK »"; fi
    fi
    if [ -f "$dir/LIVRAISON.md" ] && ! grep -Fq "$e" "$dir/LIVRAISON.md"; then bad "LIVRAISON.md ne liste pas $e"; fi
  done
  if [ -f "$dir/LIVRAISON.md" ] && grep -Eq '<(nom|une ligne|chemin|horodatage|mesurée|décision|action|lien)' "$dir/LIVRAISON.md"; then
    bad "LIVRAISON.md contient encore des éléments de gabarit"
  fi
fi

# Phase 6 : mission livrée
if [ "$P" -ge 6 ] && [ "$statut" != "LIVRÉ" ]; then bad "etat.md : statut doit être LIVRÉ en phase 6"; fi

if [ "${#problems[@]}" -eq 0 ]; then
  echo "check-mission : OK (mode $mode, phase $P)"
  exit 0
fi
echo "check-mission : ÉCHEC (${#problems[@]} problème(s), mode $mode, phase $P)" >&2
for p in "${problems[@]}"; do echo " - $p" >&2; done
exit 1
