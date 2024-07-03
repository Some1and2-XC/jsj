python -m build
python -m twine upload --repository pypi dist/*
python -m pip install --upgrade jsj
rm -rf dist
