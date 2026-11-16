#!/usr/bin/env bash
# Liste les missions MAESTRO du dépôt avec leur phase, leur statut et le temps écoulé depuis la dernière mise à jour.
# Usage : mission-status.sh [dossier-des-missions] [--stale MINUTES]
#   Une étoile signale une mission EN_COURS (phase >= 1) sans mise à jour depuis MINUTES (45 par défaut) :
#   c'est une candidate à la reprise.
set -uo pipefail

root=""; stale=45
while [ $# -gt 0 ]; do
  case "$1" in
    --stale) stale="${2:-45}"; shift 2 ;;
    *) root="$1"; shift ;;
  esac
done
top="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
root="${root:-$top/missions}"

[ -d "$root" ] || { echo "Aucune mission (dossier $root absent)."; exit 0; }

found=0
printf '%-42s %-9s %-5s %-9s %-9s %s\n' "mission" "mode" "phase" "statut" "inactif" "prochaine sous-tâche"
for etat in "$root"/*/etat.md; do
  [ -f "$etat" ] || continue
  found=1
  f() { sed -n "s/^$1:[[:space:]]*//p" "$etat" | head -1; }
  slug="$(basename "$(dirname "$etat")")"
  maj="$(f maj)"
  age="?"
  if ts="$(date -d "$maj" +%s 2>/dev/null)"; then age=$(( ( $(date +%s) - ts ) / 60 )); fi
  flag=" "
  if [ "$(f statut)" = "EN_COURS" ] && [ "$(f phase)" != "0" ] && [ "$age" != "?" ] && [ "$age" -ge "$stale" ]; then flag="*"; fi
  printf '%-42s %-9s %-5s %-9s %-9s %s\n' "$slug" "$(f mode)" "$(f phase)" "$(f statut)" "${age}min$flag" "$(f prochaine_sous_tache)"
done
[ "$found" -eq 1 ] || echo "Aucune mission dans $root."
exit 0
