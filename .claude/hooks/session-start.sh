#!/bin/bash
# Installe les skills HyperFrames (montage vidéo en HTML) au niveau utilisateur
# à chaque session cloud. Rien n'est ajouté au dépôt. Idempotent.
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

if [ -d "$HOME/.claude/skills/hyperframes" ]; then
  echo "Skills HyperFrames déjà installés."
  exit 0
fi

SKILLS="hyperframes hyperframes-core hyperframes-cli hyperframes-audio hyperframes-creative faceless-explainer product-launch-video"

cd "$HOME"
npx --yes skills add heygen-com/hyperframes -g -a claude-code -s $SKILLS --copy -y 2>&1 | tail -n 5
