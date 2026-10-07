#!/usr/bin/env bash
# Instala las skills personalizadas de este repo en ~/.claude/skills/
# Se ejecuta automáticamente en SessionStart si está configurado el hook.
set -euo pipefail

REPO_SKILLS="$(cd "$(dirname "$0")/skills" && pwd)"
TARGET="$HOME/.claude/skills"

mkdir -p "$TARGET"

for skill_dir in "$REPO_SKILLS"/*/; do
  skill_name=$(basename "$skill_dir")
  dest="$TARGET/$skill_name"
  if [ -d "$dest" ]; then
    # Solo actualiza si el repo tiene cambios más nuevos
    if [ "$skill_dir/SKILL.md" -nt "$dest/SKILL.md" ] 2>/dev/null; then
      rm -rf "$dest"
      cp -r "$skill_dir" "$dest"
      echo "[skills] Actualizado: $skill_name"
    fi
  else
    cp -r "$skill_dir" "$dest"
    echo "[skills] Instalado: $skill_name"
  fi
done

echo "[skills] Skills listas en $TARGET"
