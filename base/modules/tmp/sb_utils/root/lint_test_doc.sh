#!/usr/bin/env bash

# Lint
pylint --rcfile=.pylintrc --output-format=json sb_utils | pylint-json2html -o lint.html
# Test
python -m unittest -f tests
# Doc
python mkdocs.py