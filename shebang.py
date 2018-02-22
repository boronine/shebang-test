#!/usr/bin/env python
"""Prints the maximum length of the shebang, including the newline
"""
import os
import sys
import stat
import subprocess

# We are going to change the length of shebang by adding a number of -R flags to Python
shebang_prefix = '#!' + sys.executable + ' -R'
shebang_suffix = '\n'
shebang_length_min = len(shebang_prefix) + len(shebang_suffix)

ROOT = os.path.abspath(os.path.dirname(__file__))
TEST_FILE_PATH = os.path.join(ROOT, 'shebang_test_delete_me.py')


def executable(shebang_length):
    assert shebang_length >= shebang_length_min
    num_extra_chars = shebang_length - shebang_length_min
    extra_chars = 'R' * num_extra_chars
    shebang = shebang_prefix + extra_chars + shebang_suffix
    return shebang + 'import sys; sys.exit(7)\n'


def shebang_works(shebang_length):
    with open(TEST_FILE_PATH, 'w') as f:
        f.write(executable(shebang_length))

    os.chmod(TEST_FILE_PATH, os.stat(TEST_FILE_PATH).st_mode | stat.S_IEXEC)

    try:
        # Raises OSError
        proc = subprocess.Popen([TEST_FILE_PATH])
    except OSError as err:
        if err.args == (8, 'Exec format error'):
            # This OSError means shebang is bad
            return False
        else:
            # Not sure what this one means
            raise err

    returncode = proc.wait()
    # Supposed to exit 7
    return returncode == 7


def main():
    # shebang works when (<=) bound_lower and does not work when (>=) bound_upper
    bound_lower = length_test = shebang_length_min
    bound_upper = None

    # Find upper bound
    while bound_upper is None:
        if shebang_works(length_test):
            bound_lower = length_test
            if length_test > 1000000:
                print('Maximum shebang length > 1MB, not testing further')
            length_test *= 2
        else:
            bound_upper = length_test

    # Find cutoff point
    while bound_upper - bound_lower > 1:
        length_test = bound_lower + (bound_upper - bound_lower) // 2
        if shebang_works(length_test):
            bound_lower = length_test
        else:
            bound_upper = length_test

    print(bound_lower)


if __name__ == '__main__':
    main()
