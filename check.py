#!/usr/bin/env python3
import sys
import os
import subprocess
import shlex
import argparse
import difflib


def parse_args(argv):
    def positive_int(value):
        try:
            ivalue = int(value)
        except ValueError:
            raise argparse.ArgumentTypeError(f"invalid int value: {value!r}")
        if ivalue <= 0:
            raise argparse.ArgumentTypeError("must be a positive integer")
        return ivalue

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


def main(argv):
    args = parse_args(argv)

    num_tests = args.num_tests
    runner = args.runner
    src_ext = args.src_ext
    problem_id = args.problem_id

    class MyCommandException(Exception):
        def __init__(self, test_number, message):
            self.message = f"Test {test_number}: {message}"
            super().__init__(self.message)

    def check_all_tests():
        for test_number in range(1, num_tests + 1):
            check_test(test_number)

    def check_test(test_number):
        src_filename = f"Problem{problem_id}.{src_ext}"
        in_filename = f"Problem{problem_id}.{test_number}.in.txt"
        out_filename = f"Problem{problem_id}.{test_number}.out.txt"

        def get_actual_output() -> str:
            command = shlex.split(runner) + [src_filename]

            def run_command():
                proc = subprocess.run(
                    command,
                    shell=False,
                    stdin=in_file,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=False,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                )
                return proc

            try:
                with open(in_filename, "rb") as in_file:
                    try:
                        proc = run_command()
                        if proc.stderr:
                            print(f"Stderr output while running command {command}", file=sys.stderr)
                            print(proc.stderr, file=sys.stderr)
                        actual_output = proc.stdout
                        return actual_output
                    except FileNotFoundError:
                        raise MyCommandException(test_number, f"Could not find command: {command}")
                    except Exception as e:
                        raise MyCommandException(test_number, f"Unknown exception while running command: {command}\n{e}")
            except FileNotFoundError:
                raise MyCommandException(test_number, f"Input file not found: {in_filename}")

        def get_expected_output() -> str:
            try:
                with open(out_filename, "r", encoding="utf-8", errors="replace") as f:
                    return f.read()
            except FileNotFoundError:
                raise MyCommandException(test_number, f"Output file not found: {out_filename}")

        def normalize_output(output: str) -> list[str]:
            return output.rstrip("\n")

        def get_diff(actual, expected) -> str:
            diff_lines = difflib.unified_diff(actual.splitlines(), expected.splitlines())
            return "\n".join(diff_lines)

        actual = normalize_output(get_actual_output())
        expected = normalize_output(get_expected_output())
        diff = get_diff(actual, expected)
        if not diff:
            print(f"Test {test_number}: Success", file=sys.stdout)
        else:
            print(f"Test {test_number}: Failure\n{diff}", file=sys.stdout)

    try:
        check_all_tests()
    except MyCommandException as e:
        print(e, file=sys.stderr)
        sys.exit(2)


if __name__ == '__main__':
    _program_name, *argv = sys.argv
    main(argv)
