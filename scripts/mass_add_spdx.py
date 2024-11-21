# SPDX-License-Identifier: Apache-2.0
import os
import argparse
import fnmatch

SPDX_COMMENT_STYLES = {
    'hash': {
        'start': '# ',
        'end': '',
        'extensions': ['.py', '.sh', '.yaml', '.yml']
    },
    'double_slash': {
        'start': '// ',
        'end': '',
        'extensions': ['.js', '.ts']
    },
    'html': {
        'start': '<!-- ',
        'end': ' -->',
        'extensions': ['.html', '.xml']
    },
    'batch': {
        'start': 'REM ',
        'end': '',
        'extensions': ['.bat', '.cmd']
    }
}

IGNORE_PATTERNS = [
    '.git',
    'venv',
    'node_modules',
    '*.egg-info',
    '__pycache__',
    'build',
    'dist',
    '.idea',
    '.vscode',
    'cache',
    'env',
    'tmp',
    '.svelte-kit'
]


def should_ignore(path):
    for pattern in IGNORE_PATTERNS:
        if fnmatch.fnmatch(path, pattern) or any(fnmatch.fnmatch(part, pattern) for part in path.split(os.sep)):
            return True
    return False


def get_comment_style(file_extension):
    for style in SPDX_COMMENT_STYLES.values():
        if file_extension in style['extensions']:
            return style
    return SPDX_COMMENT_STYLES['hash']  # Default to hash-style comments


def add_spdx_header(file_path, dry_run=False):
    _, file_extension = os.path.splitext(file_path)
    comment_style = get_comment_style(file_extension)

    spdx_line = f"{comment_style['start']}SPDX-License-Identifier: Apache-2.0{comment_style['end']}\n"

    with open(file_path, 'r') as file:
        content = file.read()

    if spdx_line in content:
        print(f"SPDX header already present in {file_path}")
        return False

    new_content = spdx_line + content

    if dry_run:
        print(f"Would add SPDX header to {file_path}")
    else:
        with open(file_path, 'w') as file:
            file.write(new_content)
        print(f"Added SPDX header to {file_path}")

    return True


def process_directory(dry_run=False):
    for root, dirs, files in os.walk('../.', topdown=True):
        # Modify dirs in-place to exclude ignored directories
        dirs[:] = [d for d in dirs if not should_ignore(os.path.join(root, d))]

        for file in files:
            file_path = os.path.join(root, file)

            if should_ignore(file_path):
                continue

            _, file_extension = os.path.splitext(file_path)

            if file_extension in [ext for style in SPDX_COMMENT_STYLES.values() for ext in style['extensions']]:
                add_spdx_header(file_path, dry_run)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add SPDX license headers to files.")
    parser.add_argument("--dry-run", action="store_true", help="Perform a dry run without making changes")
    args = parser.parse_args()

    process_directory(args.dry_run)
