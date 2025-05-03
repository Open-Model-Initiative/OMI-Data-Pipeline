#!/bin/bash
# SPDX-License-Identifier: Apache-2.0
python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r ./requirements-dev.txt
pre-commit install
