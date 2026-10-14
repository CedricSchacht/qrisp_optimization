#!/usr/bin/env bash
# Run all checks and build the docs.
#
# Usage: scripts/check.sh [--fix]
#   --fix   format the code and apply automatic lint fixes instead of only checking
#
# Every check runs even if an earlier one fails; the exit code is non-zero if any failed.

set -uo pipefail

cd "$(dirname "$0")/.."

fix=false
if [[ "${1:-}" == "--fix" ]]; then
    fix=true
elif [[ $# -gt 0 ]]; then
    echo "usage: $0 [--fix]" >&2
    exit 2
fi

failed=()

run() {
    local name=$1
    shift
    echo -e "\n\033[1m==> $name\033[0m"
    if ! uv run --all-groups "$@"; then
        failed+=("$name")
    fi
}

if $fix; then
    run "ruff format" ruff format
    run "ruff check" ruff check --fix
else
    run "ruff format" ruff format --check
    run "ruff check" ruff check
fi
run "mypy" mypy
run "pytest" pytest
run "docs" properdocs build --strict

echo
if [[ ${#failed[@]} -eq 0 ]]; then
    echo -e "\033[32mAll checks passed.\033[0m"
else
    echo -e "\033[31mFailed: ${failed[*]}\033[0m"
    exit 1
fi
