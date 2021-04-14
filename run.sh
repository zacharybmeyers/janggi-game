#!/usr/bin/env bash

export PYGAME_HIDE_SUPPORT_PROMPT=1
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH=.:${PYTHONPATH}
./janggi/game.py "$@"