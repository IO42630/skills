#!/usr/bin/env bash

set -Eeuo pipefail

PROMPTFOO_VERSION="${PROMPTFOO_VERSION:-0.125.1}"

if ! command -v node >/dev/null 2>&1; then
  echo "node is required" >&2
  exit 1
fi

if ! command -v npm >/dev/null 2>&1; then
  echo "npm is required" >&2
  exit 1
fi

current_version="$(promptfoo --version 2>/dev/null || true)"
if [ "$current_version" = "$PROMPTFOO_VERSION" ]; then
  echo "promptfoo $PROMPTFOO_VERSION is already installed."
  exit 0
fi

echo "Installing promptfoo@$PROMPTFOO_VERSION globally..."
npm install --global --no-fund --no-audit "promptfoo@$PROMPTFOO_VERSION"

hash -r
global_bin="$(npm prefix --global)/bin"
if ! command -v promptfoo >/dev/null 2>&1; then
  echo "promptfoo was installed, but $global_bin is not on PATH." >&2
  echo "Add it to PATH and rerun this script." >&2
  exit 1
fi

echo "promptfoo $(promptfoo --version) installed."
