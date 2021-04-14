#!/usr/bin/env bash

export PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH=.:${PYTHONPATH}
./janggi/gui.py "$@"
