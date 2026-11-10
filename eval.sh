#!/usr/bin/env bash

set -Eeuo pipefail

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

if ! command -v promptfoo >/dev/null 2>&1; then
  echo "promptfoo not found; run ./setup.sh first." >&2
  exit 1
fi

if [ -f .env ]; then
  set -a
  . ./.env
  set +a
fi

summarize() {
  node -e '
const fs = require("node:fs");
try {
  const data = JSON.parse(fs.readFileSync(process.argv[1], "utf8"));
  let failed = 0;
  for (const result of data.results.results) {
    const label = result.prompt?.label ?? "unknown";
    const checks = result.gradingResult?.componentResults ?? [];
    if (checks.length === 0) {
      console.log(`  ${label}: ERROR ${result.error ?? "no assertions"}`);
      failed = 1;
      continue;
    }
    const passed = checks.filter((check) => check.pass).length;
    console.log(`  ${label}: ${passed}/${checks.length} (${(result.score ?? 0).toFixed(2)})`);
    if (label === "yes_skill" && passed < checks.length) failed = 1;
  }
  process.exit(failed);
} catch (error) {
  console.error(error.message);
  process.exit(2);
}
' "$1"
}

errors=0
skill_failures=0
skills_found=0

for skill_file in */SKILL.md; do
  [ -f "$skill_file" ] || continue
  skill="${skill_file%/SKILL.md}"
  skills_found=$((skills_found + 1))
  dir="$skill/evals"
  if [ ! -f "$dir/package.json" ]; then
    echo "ERROR $skill (missing $dir/package.json)" >&2
    errors=$((errors + 1))
    continue
  fi

  echo "==> $skill"
  rm -f "$dir/result.json"
  if (cd "$dir" && npm run eval); then
    rc=0
  else
    rc=$?
  fi

  if [ ! -f "$dir/result.json" ]; then
    echo "ERROR $skill (no result.json)" >&2
    errors=$((errors + 1))
    continue
  fi

  if summarize "$dir/result.json"; then
    echo "DONE $skill"
  else
    code=$?
    if [ "$code" -eq 1 ]; then
      echo "FAIL $skill (yes_skill assertions failed)" >&2
      skill_failures=$((skill_failures + 1))
    else
      echo "ERROR $skill (could not read result.json)" >&2
      errors=$((errors + 1))
    fi
  fi

  if [ "$rc" -ne 0 ] && [ "$rc" -ne 100 ]; then
    echo "ERROR $skill (eval exit $rc)" >&2
    errors=$((errors + 1))
  fi
done

if [ "$skills_found" -eq 0 ]; then
  echo "ERROR no root skill directories containing SKILL.md" >&2
  errors=$((errors + 1))
fi

if [ "$errors" -gt 0 ] || [ "$skill_failures" -gt 0 ]; then
  echo "$skill_failures skill(s) failed; $errors error(s)." >&2
  exit 1
fi

echo "All yes_skill evaluations passed."
