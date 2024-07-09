# !/bin/bash

# Script for automatically pushing updates to PyPi

source ./venv/bin/activate

python3 -m unittest

if [[ $? -ne 0 ]]; then
    read -p ""
    exit 1
fi

python3 -m build
python3 -m twine upload --repository pypi dist/*
python3 -m pip install --upgrade jsj
rm -rf dist

read -p "Deployment completed Successfully! Press [enter] to finish..."
