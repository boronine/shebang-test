#!/usr/bin/env python
"""Prints the maximum length of the shebang, including the newline
"""
import os
import stat
import subprocess

shebang_prefix = '#!/usr/bin/env '
shebang_suffix = 'python\n'
shebang_length_min = len(shebang_prefix) + len(shebang_suffix)

ROOT = os.path.abspath(os.path.dirname(__file__))
TEST_FILE_PATH = os.path.join(ROOT, 'shebang_test_delete_me.py')


def executable(shebang_length):
    assert shebang_length >= shebang_length_min
    num_extra_chars = shebang_length - shebang_length_min
    extra_chars = ' ' * num_extra_chars
    shebang = shebang_prefix + extra_chars + shebang_suffix
    return shebang + 'import sys; sys.exit(7)\n'


def shebang_works(shebang_length):
    with open(TEST_FILE_PATH, 'w') as f:
        f.write(executable(shebang_length))

    os.chmod(TEST_FILE_PATH, os.stat(TEST_FILE_PATH).st_mode | stat.S_IEXEC)

    try:
        # Raises OSError
        proc = subprocess.Popen([TEST_FILE_PATH])
        returncode = proc.wait()
        # Supposed to exit 7
        works = (returncode == 7)

    except OSError as err:
        if err.args == (8, 'Exec format error'):
            # This OSError means shebang is bad
            works = False
        else:
            # Not sure what this one means
            raise err

    os.remove(TEST_FILE_PATH)
    return works


def main():
    # shebang works when (<=) bound_lower and does not work when (>=) bound_upper
    bound_lower = length_test = 32
    bound_upper = None

    # Find upper bound
    while bound_upper is None:
        if shebang_works(length_test):
            bound_lower = length_test
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
