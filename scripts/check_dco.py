#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0

import sys
import re


def check_dco():
    # Get the commit message
    commit_msg_file = sys.argv[1]
    with open(commit_msg_file, 'r') as f:
        commit_msg = f.read()

    # Check for DCO sign-off using a ReDoS-safe pattern
    # Pattern breakdown:
    # ^ - start of line
    # Signed-off-by: - literal text
    # [^<]{1,100} - 1 to 100 non-< characters (name, with reasonable length limit)
    # <[^>@]{1,64}@ - local part of email (limited to 64 chars per RFC 5321)
    # [^>\.]{1,255}\. - domain part before dot (limited to 255 chars per RFC 5321)
    # [^>]{1,255}> - domain part after dot (limited to 255 chars per RFC 5321)
    # $ - end of line
    dco_pattern = r'^Signed-off-by:\s[^<]{1,100}<[^>@]{1,64}@[^>\.]{1,255}\.[^>]{1,255}>$'

    # Check each line for the DCO pattern
    for line in commit_msg.splitlines():
        if re.match(dco_pattern, line.strip(), re.ASCII):
            return

    print("Error: No DCO sign-off found in commit message.")
    print("Please add a DCO sign-off using:")
    print("git commit -s -m 'your commit message'")
    print("or add the following line to your commit message:")
    print("Signed-off-by: Your Name <your.email@example.com>")
    sys.exit(1)


if __name__ == '__main__':
    check_dco()
