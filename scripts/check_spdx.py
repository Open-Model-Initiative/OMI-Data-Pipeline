# SPDX-License-Identifier: Apache-2.0
import argparse
import sys
from pathlib import Path

REQUIRED_HEADER = "SPDX-License-Identifier: Apache-2.0"
EXIT_SUCCESS = 0
EXIT_FAILURE = 1


def check_file(filename):
    if Path(filename).name == 'pnpm-lock.yaml':
        return True
    try:
        # Read only first 1000 bytes - license header should be at the top
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read(1000)
            if REQUIRED_HEADER not in content:
                print(f"Error: {filename} is missing the required SPDX license identifier")
                print(f"Required header: {REQUIRED_HEADER}")
                return False
    except Exception as e:
        print(f"Error reading {filename}: {str(e)}")
        return False
    return True


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    args = parser.parse_args(argv)

    retval = EXIT_SUCCESS

    for filename in args.filenames:
        if not check_file(filename):
            retval = EXIT_FAILURE

    return retval

if __name__ == '__main__':
    sys.exit(main())
