#!/usr/bin/env bash

# Script for automatically pushing updates to PyPi

python -m unittest

if [[ $? -ne 0 ]]; then
    read -p ""
    exit 1
fi

python -m build
python -m twine upload --repository pypi dist/*
python -m pip install --upgrade jsj
rm -rf dist

read -p "Deployment completed Successfully! Press [enter] to finish..."
