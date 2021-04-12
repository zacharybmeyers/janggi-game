#!/usr/bin/env bash

export PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH=janggi:${PYTHONPATH}
./janggi/game.py "$@"
