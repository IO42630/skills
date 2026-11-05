#!/usr/bin/env bash

set -Eeuo pipefail

if [ -f .env ]; then
  set -a
  . ./.env
  set +a
fi

SKILLS_DIR="${SKILLS_DIR:-.agents/skills}"
GITEA_REPO_URL="${GITEA_REPO_URL:-}"
GITEA_TOKEN="${GITEA_TOKEN:-}"
GITEA_USER="${GITEA_USER:-git}"
GITEA_SKILLS=(
    "io-shell"
)

case "$SKILLS_DIR" in
  /|.|..) echo "Invalid SKILLS_DIR: $SKILLS_DIR" >&2; exit 1 ;;
esac

exclude_file="$(git rev-parse --git-path info/exclude)"
if [ ! -f "$exclude_file" ] || ! grep -Fxq '/.agents/skills/' "$exclude_file"; then
  printf '%s\n' '/.agents/skills/' > "$exclude_file"
fi

if [ -n "$GITEA_REPO_URL" ]; then
  case "$GITEA_REPO_URL" in
    http://*|https://*)
      if [ -z "$GITEA_TOKEN" ]; then
        echo "GITEA_TOKEN is required for $GITEA_REPO_URL" >&2
        exit 1
      fi
      ;;
  esac
fi

rm -rf .agents/skills
mkdir -p "$SKILLS_DIR"

echo "Updating agent skills..."

redact_secrets() {
  if [ -n "${GITEA_TOKEN:-}" ]; then
    sed "s|${GITEA_TOKEN}|***|g"
  else
    cat
  fi
}

show_failure_log() {
  local log="$1"
  {
    echo "  --- installer output ---"
    redact_secrets < "$log" | tail -n 25
    echo "  ------------------------"
  } >&2
}

install_skill() {
  local repo="$1"
  local skill="$2"
  local log rc
  log="$(mktemp "${TMPDIR:-/tmp}/skills-install.XXXXXX")"
  printf "Installing skill '%s'... " "$skill"
  if npx -y skills add "$repo" --skill "$skill" -a universal -y > "$log" 2>&1; then
    echo "done."
    rm -f "$log"
  else
    rc=$?
    echo "FAILED!"
    show_failure_log "$log"
    rm -f "$log"
    return "$rc"
  fi
}

install_gitea_skill() {
  local skill="$1"
  local origin=""
  local url="${GITEA_REPO_URL%/}"
  local log rc
  case "$GITEA_REPO_URL" in
    http://*|https://*)
      origin="$(printf '%s\n' "$GITEA_REPO_URL" | sed -E 's#^([a-z]+://[^/]+).*#\1#')"
      ;;
  esac
  case "$url" in
    *.git) ;;
    *) url="$url.git" ;;
  esac

  log="$(mktemp "${TMPDIR:-/tmp}/skills-install.XXXXXX")"
  printf "Installing private skill '%s'... " "$skill"
  if (
    export GITEA_USER GITEA_TOKEN
    if [ -n "$origin" ]; then
      export GIT_CONFIG_COUNT=1
      export GIT_CONFIG_KEY_0="credential.${origin}.helper"
      export GIT_CONFIG_VALUE_0='!f() { printf "username=%s\npassword=%s\n" "$GITEA_USER" "$GITEA_TOKEN"; }; f'
    fi
    export GIT_TERMINAL_PROMPT=0
    export DISABLE_TELEMETRY=1
    npx -y skills add "$url" --skill "$skill" -a universal -y
  ) > "$log" 2>&1; then
    echo "done."
    rm -f "$log"
  else
    rc=$?
    echo "FAILED!"
    show_failure_log "$log"
    rm -f "$log"
    return "$rc"
  fi
}

move_skills_to_target() {
  [ -d ".agents/skills" ] || return 0
  mkdir -p "$SKILLS_DIR"
  local source_dir target_dir src name
  source_dir="$(cd ".agents/skills" && pwd -P)"
  target_dir="$(cd "$SKILLS_DIR" && pwd -P)"
  [ "$source_dir" = "$target_dir" ] && return 0
  case "$target_dir" in
    "$source_dir"/*) echo "SKILLS_DIR cannot be inside .agents/skills" >&2; exit 1 ;;
  esac
  for src in .agents/skills/*; do
    [ -d "$src" ] || continue
    name="$(basename "$src")"
    rm -rf "${SKILLS_DIR:?}/$name"
    mv "$src" "$SKILLS_DIR/$name"
  done
  rmdir .agents/skills 2>/dev/null || true
}

cleanup_empty_agent_dirs() {
  local dir
  for dir in .claude .junie; do
    if [ -d "$dir" ]; then
      find "$dir" -depth -type d -empty -delete
    fi
  done
}

cleanup_lockfiles() {
  local lockfile removed=0
  while IFS= read -r -d '' lockfile; do
    rm -f "$lockfile"
    removed=$((removed + 1))
  done < <(find . \( -name .git -o -name node_modules \) -prune -o -type f \
    \( -name 'skills-lock.json' -o -name '.skills.json' \) -print0)
  if [ "$removed" -gt 0 ]; then
    echo "Removed $removed skill lockfile(s)."
  fi
  return 0
}

trap cleanup_lockfiles EXIT

install_skill "https://github.com/io42630/skills" "plexy-markdown"
install_skill "https://github.com/io42630/skills" "plexy-probe"
install_skill "https://github.com/io42630/skills" "plexy-save"

if [ -n "$GITEA_REPO_URL" ]; then
  if [ "${#GITEA_SKILLS[@]}" -eq 0 ]; then
    echo "GITEA_SKILLS is empty; skipping private skills." >&2
  fi
  for skill in "${GITEA_SKILLS[@]}"; do
    install_gitea_skill "$skill"
  done
fi

move_skills_to_target
cleanup_empty_agent_dirs
cleanup_lockfiles

echo "Skills updated successfully in $SKILLS_DIR"
