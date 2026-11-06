#!/usr/bin/env bash
# Auto-test des verrous de MAESTRO : crée une mission jetable et vérifie que chaque verrou bloque puis libère.
# Usage : bash selftest.sh        (code 0 = tous les verrous fonctionnent)
set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
n=0; ko=0
ok()   { n=$((n+1)); echo "  ok   $*"; }
nok()  { n=$((n+1)); ko=$((ko+1)); echo "  FAIL $*"; }
expect_ok()   { local label="$1"; shift; if "$@" >/dev/null 2>&1; then ok "$label"; else nok "$label (attendu : succès)"; fi; }
expect_fail() { local label="$1"; shift; if "$@" >/dev/null 2>&1; then nok "$label (attendu : échec)"; else ok "$label"; fi; }

dir="$(bash "$HERE/new-mission.sh" "Test éclair ÀÉ" --mode standard --root "$tmp" 2>/dev/null)"
[ -d "$dir" ] && ok "création du dossier ($(basename "$dir"))" || { nok "création du dossier"; exit 1; }
case "$(basename "$dir")" in *-test-eclair-ae) ok "slug normalisé" ;; *) nok "slug normalisé : $(basename "$dir")" ;; esac

C="bash $HERE/check-mission.sh"; L="bash $HERE/lock-brief.sh"

expect_ok   "phase 0 : fichiers de base présents"            $C "$dir" --phase 0
expect_fail "phase 1 refusée : brief non verrouillé"          $C "$dir" --phase 1
expect_fail "verrouillage refusé : brief incomplet"           $L "$dir"

sed -i -E 's/\[\[[^]]*\]\]/ok/g; s/^verdict:.*/verdict: ne pas lancer/' "$dir/brief.md"
expect_fail "verrouillage refusé : verdict « ne pas lancer »" $L "$dir"
sed -i -E 's/^verdict:.*/verdict: lancer/' "$dir/brief.md"
expect_ok   "verrouillage accepté"                            $L "$dir"
grep -q '^phase: 1' "$dir/etat.md" && ok "etat.md passé en phase 1" || nok "etat.md passé en phase 1"
expect_fail "second verrouillage refusé (sans avenant)"       $L "$dir"
expect_ok   "phase 1 acceptée"                                $C "$dir" --phase 1

cp "$dir/brief.md" "$tmp/brief.bak"; echo "dérive" >> "$dir/brief.md"
expect_fail "brief modifié après verrouillage détecté"        $C "$dir" --phase 1
cp "$tmp/brief.bak" "$dir/brief.md"
expect_ok   "brief restauré, contrôle au vert"                $C "$dir" --phase 1
expect_ok   "avenant accepté"                                 $L "$dir" --avenant "périmètre élargi au kit email"
expect_ok   "contrôle au vert après avenant"                  $C "$dir" --phase 1

expect_fail "phase 3 refusée : gabarit BENCHMARK non rempli"  $C "$dir" --phase 3
printf '# BENCHMARK\n\n## Structure du plan\n- Cas 1 : exemple — https://example.com\n  Pattern extrait : x\n' > "$dir/BENCHMARK.md"
expect_fail "phase 3 refusée : aucune décision clôturée"      $C "$dir" --phase 3
printf '# DECISIONS\n\nAucune décision structurante.\n' > "$dir/decisions.md"
expect_ok   "phase 3 acceptée"                                $C "$dir" --phase 3

printf 'Plan\nTODO écrire la suite\n' > "$dir/livrables/L01-plan.md"
expect_fail "placeholder TODO détecté dans un livrable"       $C "$dir" --phase 3
printf 'Plan complet et final\n' > "$dir/livrables/L01-plan.md"
expect_ok   "livrable propre accepté"                         $C "$dir" --phase 4

expect_fail "phase 5 refusée : pas d'audit"                   $C "$dir" --phase 5
printf '| L01-plan.md | stratégie | 1 | 74 | 2 | A_CORRIGER | x |\n' >> "$dir/audit.md"
expect_fail "phase 5 refusée : dernière passe A_CORRIGER"     $C "$dir" --phase 5
printf '| L01-plan.md | stratégie | 2 | 88 | 3 | OK | |\n' >> "$dir/audit.md"
expect_fail "phase 5 refusée : LIVRAISON.md non rempli"       $C "$dir" --phase 5
printf '# LIVRAISON\n\n| `livrables/L01-plan.md` | le plan | dépôt |\n' > "$dir/LIVRAISON.md"
expect_ok   "phase 5 acceptée"                                $C "$dir" --phase 5

sed -i -E 's/^phase:.*/phase: 6/; s/^statut:.*/statut: LIVRÉ/' "$dir/etat.md"
expect_ok   "phase 6 acceptée (statut LIVRÉ)"                 $C "$dir" --phase 6
sed -i -E 's/^phase:.*/phase: 9/' "$dir/etat.md"
expect_fail "etat.md invalide détecté"                        $C "$dir"

out="$(bash "$HERE/mission-status.sh" "$tmp" 2>&1)"
printf '%s' "$out" | grep -q "test-eclair-ae" && ok "mission-status liste la mission" || nok "mission-status liste la mission"

edir="$(bash "$HERE/new-mission.sh" "mini" --mode eclair --root "$tmp" 2>/dev/null)"
[ ! -f "$edir/equipe.md" ] && ok "mode éclair : pas de fichiers d'équipe" || nok "mode éclair : pas de fichiers d'équipe"

echo
if [ "$ko" -eq 0 ]; then echo "selftest : $n vérifications OK"; exit 0; fi
echo "selftest : $ko échec(s) sur $n" >&2; exit 1
