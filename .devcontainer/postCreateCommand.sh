#!/bin/bash

sudo -u vscode bash << EOF
pip install --no-warn-script-location --user -e .
npx husky
rm -Rf *.egg-info build
