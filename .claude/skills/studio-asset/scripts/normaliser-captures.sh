#!/usr/bin/env bash
# Met des captures d'app mobile (iPhone, Android, n'importe quelle taille) au format de l'écran du téléphone de la scène :
# 1170×2532 (390×844 × 3), en recadrant au centre si le rapport diffère, sans déformer.
# Usage : normaliser-captures.sh <dossier des captures d'origine> <dossier de sortie>
# Les noms sont gardés (renommer d'abord en 01-accueil.png, 02-…, dans l'ordre du storyboard).
# Après coup : retirer la barre d'état réelle (heure, batterie) si elle gêne, en la recouvrant dans la scène ou en refaisant la capture.
set -euo pipefail
src=${1:?dossier source}; dst=${2:?dossier de sortie}; mkdir -p "$dst"
for f in "$src"/*.png "$src"/*.jpg "$src"/*.jpeg "$src"/*.PNG "$src"/*.JPG; do
  [ -e "$f" ] || continue
  nom=$(basename "${f%.*}")
  ffmpeg -y -loglevel error -i "$f" -vf "scale=1170:2532:force_original_aspect_ratio=increase,crop=1170:2532" "$dst/$nom.png"
  echo "$dst/$nom.png"
done
