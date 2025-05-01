#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0

import sys
import subprocess
import re

def check_dco():
    # Get the commit message
    commit_msg_file = sys.argv[1]
    with open(commit_msg_file, 'r') as f:
        commit_msg = f.read()

    # Check for DCO sign-off
    dco_pattern = r'Signed-off-by: .+ <.+@.+\..+>'
    if not re.search(dco_pattern, commit_msg):
        print("Error: No DCO sign-off found in commit message.")
        print("Please add a DCO sign-off using:")
        print("git commit -s -m 'your commit message'")
        print("or add the following line to your commit message:")
        print("Signed-off-by: Your Name <your.email@example.com>")
        sys.exit(1)

if __name__ == '__main__':
    check_dco() 