#!/usr/bin/env bash

export PYTHONDONTWRITEBYTECODE=1
coverage run -m unittest discover -v -s janggi/

if [[ "$(uname)" == "Darwin" ]]; then
  coverage html
  open -a 'Google Chrome' "file://$(pwd)/htmlcov/index.html"
else
  coverate report
fi
