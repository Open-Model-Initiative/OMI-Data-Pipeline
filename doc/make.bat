:: SPDX-License-Identifier: Apache-2.0


@ECHO OFF

pushd %~dp0

REM Command file for building Open Model Initiative Data Repository documentation with Sphinx

if "%SPHINXBUILD%" == "" (
	set SPHINXBUILD=sphinx-build
)
set SOURCEDIR=.
set BUILDDIR=_build

%SPHINXBUILD% >NUL 2>NUL
if errorlevel 9009 (
	echo.
	echo.The 'sphinx-build' command was not found. Please ensure Sphinx is installed.
	echo.Set the SPHINXBUILD environment variable to the full path of the 'sphinx-build' executable.
	echo.Or add the Sphinx directory to your PATH.
	echo.
	echo.Download Sphinx from https://www.sphinx-doc.org/
	exit /b 1
)

if "%1" == "" goto help

%SPHINXBUILD% -M %1 %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%
goto end

:help
%SPHINXBUILD% -M help %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%

:end
popd
