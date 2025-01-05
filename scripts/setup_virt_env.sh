#!/bin/bash
# SPDX-License-Identifier: Apache-2.0
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
# pip install -e ./modules/odr_core
# pip install -e ./modules/odr_api
# pip install -e ./modules/odr_monitoring
# pip install -e ./modules/odr_caption
pip install -r ./requirements-dev.txt
# pip install git+https://github.com/dottxt-ai/outlines.git --upgrade
pre-commit install
