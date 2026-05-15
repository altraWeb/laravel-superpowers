#!/usr/bin/env bash
# Shell test driver for hooks/teamcity-always.sh
#
# Each scenario invokes the hook with a mocked tool_input JSON on stdin,
# captures exit code, asserts.
#
# Run from repo root: bash tests/test_teamcity_always_hook.sh

set -uo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
HOOK="${REPO_ROOT}/hooks/teamcity-always.sh"

[ -x "$HOOK" ] || { echo "FAIL: hook not executable at $HOOK"; exit 1; }

failures=0

run_with_command() {
    local cmd="$1"
    local stderr_file
    stderr_file="$(mktemp)"
    export CLAUDE_PLUGIN_ROOT="$REPO_ROOT"
    local exit_code
    set +e
    printf '{"tool_input":{"command":%s}}' "$(printf '%s' "$cmd" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))')" \
        | bash "$HOOK" 2> "$stderr_file"
    exit_code=$?
    set -e
    printf 'exit=%s\n' "$exit_code"
    printf -- '--- stderr ---\n'
    cat "$stderr_file"
    printf -- '--- end ---\n'
    rm -f "$stderr_file"
}

assert_exit() {
    local actual="$1" expected="$2" name="$3"
    if [ "$actual" = "$expected" ]; then
        printf '  ✅ %s — exit %s (expected)\n' "$name" "$actual"
    else
        printf '  ❌ %s — got exit %s, expected %s\n' "$name" "$actual" "$expected"
        failures=$((failures + 1))
    fi
}

extract_exit() {
    printf '%s' "$1" | grep -oE 'exit=[0-9]+' | head -1 | cut -d= -f2
}

# ─── Test 1: Block plain php artisan test ────────────────────────────────────
echo
echo "▶ Test 1: Block plain \`php artisan test\`"
result=$(run_with_command "php artisan test")
assert_exit "$(extract_exit "$result")" "2" "Plain php artisan test should block"

# ─── Test 2: Block with --filter ─────────────────────────────────────────────
echo
echo "▶ Test 2: Block \`php artisan test --filter=UserTest\`"
result=$(run_with_command "php artisan test --filter=UserTest")
assert_exit "$(extract_exit "$result")" "2" "test --filter should block"

# ─── Test 3: Block test:parallel ─────────────────────────────────────────────
echo
echo "▶ Test 3: Block \`php artisan test:parallel\`"
result=$(run_with_command "php artisan test:parallel")
assert_exit "$(extract_exit "$result")" "2" "test:parallel should block"

# ─── Test 4: Allow --teamcity already present ────────────────────────────────
echo
echo "▶ Test 4: Allow \`php artisan test --teamcity\`"
result=$(run_with_command "php artisan test --teamcity")
assert_exit "$(extract_exit "$result")" "0" "test --teamcity should pass"

# ─── Test 5: Allow --testdox (alt reporter) ──────────────────────────────────
echo
echo "▶ Test 5: Allow \`php artisan test --testdox\`"
result=$(run_with_command "php artisan test --testdox")
assert_exit "$(extract_exit "$result")" "0" "test --testdox should pass"

# ─── Test 6: Passthrough php artisan migrate ─────────────────────────────────
echo
echo "▶ Test 6: Passthrough \`php artisan migrate\` (not test)"
result=$(run_with_command "php artisan migrate")
assert_exit "$(extract_exit "$result")" "0" "migrate should pass through"

# ─── Test 7: Passthrough ./vendor/bin/pest ───────────────────────────────────
echo
echo "▶ Test 7: Passthrough \`./vendor/bin/pest\` (not artisan)"
result=$(run_with_command "./vendor/bin/pest")
assert_exit "$(extract_exit "$result")" "0" "vendor/bin/pest should pass through"

# ─── Test 8: Passthrough git status ──────────────────────────────────────────
echo
echo "▶ Test 8: Passthrough \`git status\` (not artisan)"
result=$(run_with_command "git status")
assert_exit "$(extract_exit "$result")" "0" "git status should pass through"

# ─── Test 9: Suggested rewrite includes --teamcity in right spot ─────────────
echo
echo "▶ Test 9: Diagnostic suggests \`php artisan test --teamcity --filter=X\`"
result=$(run_with_command "php artisan test --filter=UserTest")
exit_code=$(extract_exit "$result")
assert_exit "$exit_code" "2" "Diagnostic test should block"
if printf '%s' "$result" | grep -q "php artisan test --teamcity --filter=UserTest"; then
    echo "  ✅ suggested rewrite includes --teamcity in correct position"
else
    echo "  ❌ suggested rewrite missing or wrong position"
    failures=$((failures + 1))
fi

# ─── Summary ─────────────────────────────────────────────────────────────────
echo
if [ "$failures" -eq 0 ]; then
    echo "🟢 All hook scenarios passed."
    exit 0
else
    echo "🔴 ${failures} scenario(s) failed."
    exit 1
fi
