#!/usr/bin/env bash
set -ev

rm -rf build
rm -rf dist
python setup.py sdist
python setup.py bdist_wheel
twine upload dist/*
