#!/usr/bin/env bash
# Crée le dossier d'une mission MAESTRO à partir des templates.
# Usage : new-mission.sh <slug> [--mode eclair|standard|complete] [--root <dossier>]
# Sortie : le chemin du dossier créé (dernière ligne).
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MAESTRO="$(dirname "$HERE")"
CADRAGE="$(dirname "$MAESTRO")/cadrage-projet"

slug_in=""; mode="standard"; root=""
while [ $# -gt 0 ]; do
  case "$1" in
    --mode) mode="${2:-}"; shift 2 ;;
    --root) root="${2:-}"; shift 2 ;;
    -h|--help) sed -n '2,4p' "$0"; exit 0 ;;
    *) if [ -z "$slug_in" ]; then slug_in="$1"; shift; else echo "argument inattendu : $1" >&2; exit 2; fi ;;
  esac
done
[ -n "$slug_in" ] || { echo "usage : new-mission.sh <slug> [--mode eclair|standard|complete] [--root dossier]" >&2; exit 2; }
case "$mode" in eclair|standard|complete) ;; *) echo "mode invalide : $mode (eclair, standard ou complete)" >&2; exit 2 ;; esac

slug="$(python3 -I -c 'import sys,unicodedata,re; s=unicodedata.normalize("NFKD",sys.argv[1]).encode("ascii","ignore").decode().lower(); print(re.sub(r"[^a-z0-9]+","-",s).strip("-"))' "$slug_in")"
[ -n "$slug" ] || { echo "slug vide après normalisation : $slug_in" >&2; exit 2; }

top="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
root="${root:-$top/missions}"
date_iso="$(date +%F)"
now="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
branch="$(git branch --show-current 2>/dev/null || true)"; branch="${branch:-—}"
dir="$root/$date_iso-$slug"
[ ! -e "$dir" ] || { echo "le dossier existe déjà : $dir" >&2; exit 1; }
reldir="$(realpath --relative-to="$top" "$dir" 2>/dev/null || echo "$dir")"

mkdir -p "$dir/livrables"
: > "$dir/livrables/.gitkeep"

copy() { # copy <dossier source> <fichier>
  [ -f "$1/templates/$2" ] || { echo "template manquant : $1/templates/$2" >&2; exit 1; }
  cp "$1/templates/$2" "$dir/$2"
}

for f in etat.md plan.md BENCHMARK.md audit.md LIVRAISON.md; do copy "$MAESTRO" "$f"; done
copy "$CADRAGE" brief.md
if [ "$mode" != "eclair" ]; then
  for f in decisions.md TOOLING.md; do copy "$MAESTRO" "$f"; done
  for f in reconnaissance.md dossier-de-choix.md equipe.md journal-decisions.md; do copy "$CADRAGE" "$f"; done
fi

for f in "$dir"/*.md; do
  sed -i "s|__SLUG__|$slug|g; s|__DIR__|$reldir|g; s|__MODE__|$mode|g; s|__DATE__|$date_iso|g; s|__NOW__|$now|g; s|__BRANCH__|$branch|g" "$f"
done

echo "Mission créée en mode $mode" >&2
echo "$dir"
