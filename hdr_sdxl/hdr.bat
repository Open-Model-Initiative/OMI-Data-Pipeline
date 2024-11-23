REM SPDX-License-Identifier: Apache-2.0
@echo off
setlocal

set PYTHON=python
set VENV=venv
set UV_INDEX_STRATEGY=unsafe-any-match

echo HDR: launch
%PYTHON% -c "import venv" 2>nul
if errorlevel 1 (
    echo HDR error: python or venv not installed
    exit /b 1
)

if not exist %VENV% (
    echo HDR: create
    %PYTHON% -m venv %VENV%
    set INITIAL=1
)

if exist %VENV%\Scripts\activate.bat (
    echo HDR: activate
    call %VENV%\Scripts\activate.bat
) else (
    echo HDR error: venv cannot activate
    exit /b 1
)

if defined INITIAL (
    echo HDR: install
    pip install uv
) else (
  echo HDR: verify
)
uv pip install -r requirements.txt
echo HDR: exec
python hdr.py %*
