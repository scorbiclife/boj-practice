#!/bin/sh

print_usage() {
    cat <<'USAGE' >&2
Usage: ./check.sh [options] <problem_id>

Options:
  -n <num>         Number of test cases (default: 1)
  -e <ext>         Source file extension (default: js). Can be supplied with or without a leading dot.
  --with <cmd>     Command to run the solution (default: node)
  -h, --help       Show this help

Examples:
  ./check.sh 1406 -n 3 --with node
  ./check.sh 31428 -e py --with 'python3 -u'
USAGE
}

num_tests=1
runner=node
src_ext=js
problem_id=""

# Parse options. Options may appear before or after the problem_id.
while [ $# -gt 0 ]; do
    case "$1" in
        -n)
            shift
            if [ $# -eq 0 ]; then
                echo "Error: -n requires an argument" >&2
                print_usage
                exit 2
            fi
            num_tests="$1"
            ;;
        -n*)
            num_tests="${1#-n}"
            ;;
        --with)
            shift
            if [ $# -eq 0 ]; then
                echo "Error: --with requires an argument" >&2
                print_usage
                exit 2
            fi
            runner="$1"
            ;;
        --with=*)
            runner="${1#--with=}"
            ;;
        -e)
            shift
            if [ $# -eq 0 ]; then
                echo "Error: -e requires an argument" >&2
                print_usage
                exit 2
            fi
            src_ext="$1"
            ;;
        -e*)
            src_ext="${1#-e}"
            ;;
        --ext)
            shift
            if [ $# -eq 0 ]; then
                echo "Error: --ext requires an argument" >&2
                print_usage
                exit 2
            fi
            src_ext="$1"
            ;;
        --ext=*)
            src_ext="${1#--ext=}"
            ;;
        -h|--help)
            print_usage
            exit 0
            ;;
        --)
            shift
            if [ -z "$problem_id" ] && [ $# -gt 0 ]; then
                problem_id="$1"
                shift
            fi
            break
            ;;
        -*)
            echo "Unknown option: $1" >&2
            print_usage
            exit 2
            ;;
        *)
            if [ -z "$problem_id" ]; then
                problem_id="$1"
            else
                echo "Unexpected argument: $1" >&2
                print_usage
                exit 2
            fi
            ;;
    esac
    shift
done

if [ -z "$problem_id" ]; then
    echo "Error: problem_id is required" >&2
    print_usage
    exit 2
fi

# Validate num_tests is a positive integer
case "$num_tests" in
    ''|*[!0-9]*)
        echo "Error: -n requires a positive integer" >&2
        exit 2
        ;;
esac

# Prepare temporary files for comparison
TMP_EXPECTED=$(mktemp 2>/dev/null || printf "/tmp/check_expected_%s" "$$")
TMP_ACTUAL=$(mktemp 2>/dev/null || printf "/tmp/check_actual_%s" "$$")
trap 'rm -f "$TMP_EXPECTED" "$TMP_ACTUAL"' EXIT INT TERM

# Sanitize extension: remove leading dot if present and ensure non-empty
case "$src_ext" in
    .*) src_ext="${src_ext#.}";;
esac
if [ -z "$src_ext" ]; then
    echo "Error: extension is empty" >&2
    exit 2
fi

# Determine source file. Prefer the file prefixed with "Problem" but fall back
# to the unprefixed name for backwards compatibility. The extension is configurable.
src_prefixed="Problem${problem_id}.${src_ext}"
if [ -f "$src_prefixed" ]; then
    src="$src_prefixed"
else
    echo "Error: source file not found. Tried: $src_prefixed" >&2
    exit 2
fi

i=1
while [ "$i" -le "$num_tests" ]; do
    in_file="Problem${problem_id}.${i}.in.txt"
    if [ -z "$in_file" ]; then
        echo "Missing input file for test $i (tried: $in_file)" >&2
        i=$((i + 1))
        continue
    fi

    out_file="Problem${problem_id}.${i}.out.txt"
    if [ -z "$out_file" ]; then
        echo "Missing output file for test $i (tried: $out_file)" >&2
        i=$((i + 1))
        continue
    fi

    # Run the solution; capture stdout into a shell variable (command substitution
    # trims trailing newlines, matching the old behavior).
    expected="$(sh -c "$runner \"${src}\"" < "$in_file" 2>/dev/null)"
    actual="$(cat "$out_file")"

    if [ "$expected" = "$actual" ]; then
        echo "Success: test case $i" >&2
    else
        echo "Fail: test case $i" >&2
        printf '%s\n' "$expected" > "$TMP_EXPECTED"
        printf '%s\n' "$actual" > "$TMP_ACTUAL"
        diff -u "$TMP_EXPECTED" "$TMP_ACTUAL" || true
    fi

    i=$((i + 1))
done
