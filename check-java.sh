#!/usr/bin/env bash
declare -ri problem_id="$1"

declare -ri last_test_id="${2:-1}"

declare -i i
declare expected
declare actual
for ((i=1; i<="$last_test_id"; ++i)); do
    # Posix command substitution trims trailing newlines
    expected="$(jbang "Problem$problem_id.java" <"$problem_id.$i.in.txt")"
    actual="$(cat "$problem_id.$i.out.txt")"
    if [[ "$expected" = "$actual" ]]; then
        echo "Success: test case $i" >&2
    else
        echo "Fail: test case $i" >&2
        diff <(echo "$expected") <(echo "$actual")
    fi
done
