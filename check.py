#!/usr/bin/env python3
import sys
import os
import subprocess
import shlex
import argparse
import difflib


def positive_int(value):
    try:
        ivalue = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"invalid int value: {value!r}")
    if ivalue <= 0:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return ivalue


def parse_args(argv):
    parser = argparse.ArgumentParser(
        usage="%(prog)s <problem_id> [-n num] [-e ext] [--with RUNNER]",
        description="Check if the given solution transforms the given inputs into the given outputs",
        epilog=f"Examples:\n  {sys.argv[0]} 1406 -n 3 --with node\n  ./check.py 31428 -e py --with 'python3 -u'",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        allow_abbrev=False,
    )
    parser.add_argument('-n', type=positive_int, default=1, metavar='num', dest='num_tests',
                        help='Number of test cases (default: 1)')
    parser.add_argument('-e', '--ext', dest='src_ext', default='js', metavar='ext',
                        help='Source file extension (default: js). Should be supplied without a leading dot.')
    parser.add_argument('--with', dest='runner', default='node',
                        help='Command to run the solution (default: node)')
    parser.add_argument('problem_id', help='Problem id')

    return parser.parse_args(argv)


def require_condition(condition, /, exit_message, exit_code):
    if not condition:
        sys.stderr.write(exit_message)
        sys.exit(exit_code)


def require_file(file, /, exit_message, exit_code):
    require_condition(os.path.isfile(file), exit_message, exit_code)


def main(argv):
    args = parse_args(argv)

    num_tests_int = args.num_tests
    runner = args.runner
    src_ext = args.src_ext
    problem_id = args.problem_id

    src = f"Problem{problem_id}.{src_ext}"
    require_file(src,
                 exit_message=f"Error: source file not found. Tried: {src}",
                 exit_code=1)

    for t in range(1, num_tests_int + 1):
        in_file = f"Problem{problem_id}.{t}.in.txt"
        # Build command. Run the runner directly (no shell). Accept runner flags (e.g. "python3 -u").
        runner_parts = shlex.split(runner)
        require_condition(len(runner_parts) != 0,
                          exit_message="Error: runner is empty\n",
                          exit_code=1)
        cmd_list = runner_parts + [src]
        proc_stdout = ""
        try:
            with open(in_file, 'rb') as stdin_f:
                proc = subprocess.run(
                    cmd_list,
                    shell=False,
                    stdin=stdin_f,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=False,
                )
                proc_stdout = proc.stdout.decode('utf-8', errors='replace')
                sys.stderr.write(proc.stderr.decode('utf-8', errors='replace'))
                if proc.returncode != 0:
                    sys.stderr.write(
                        f"Error: runner exited with status {proc.returncode}\n")
                    sys.exit(1)
        except FileNotFoundError:
            if not os.file.isfile(in_file):
                sys.stdout.write(f"Missing input file for test {t} (tried: {in_file})\n")
                sys.exit(1)
            # runner executable not found
            runner_name = runner_parts[0]
            sys.stderr.write(f"Error: runner not found: {runner_name}\n")
            sys.exit(1)
        except Exception as e:
            sys.stderr.write(f"Unknown error while running runner: {e}\n")
            sys.exit(1)

        # Normalize trailing newlines
        actual = proc_stdout.rstrip('\n')

        # Read output file to get expected output and also normalize trailing newlines
        out_file = f"Problem{problem_id}.{t}.out.txt"
        try:
            with open(out_file, 'r', encoding='utf-8', errors='replace') as f:
                out_file_contents = f.read()
        except Exception as e:
            if not os.file.isfile(out_file):
                sys.stderr.write(f"Missing output file for test {t} (tried: {out_file})\n")
                sys.exit(1)
            sys.stderr.write(
                f"Unknown error while reading from output file: {e}")
            sys.exit(1)
        expected = out_file_contents.rstrip('\n')

        if actual == expected:
            sys.stderr.write(f"Success: test case {t}\n")
            continue

        sys.stderr.write(f"Fail: test case {t}\n")
        # Show unified diff using Python's difflib (no external 'diff' required)
        diff_lines = difflib.unified_diff(
            actual.splitlines(), expected.splitlines())
        for line in diff_lines:
            sys.stdout.write(line)


if __name__ == '__main__':
    main(sys.argv[1:])
