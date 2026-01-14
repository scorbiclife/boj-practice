declare -ri problem_id="$1"

declare -ri last_test_id="${2:-1}"

declare -i i
for ((i=1; i<="$last_test_id"; ++i)); do
    if { node "$problem_id".js <"$problem_id"."$i".in.txt |
        diff - "$problem_id"."$i".out.txt; } then
        echo "Success: test case $i" >&2
    else
        echo "Fail: test case $i" >&2
    fi
done
