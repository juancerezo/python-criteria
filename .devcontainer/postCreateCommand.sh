#!/bin/bash

sudo -u vscode bash << EOF
pip install --no-warn-script-location --user -e .
pip install pre-commit
pre-commit install
rm -Rf *.egg-info build
