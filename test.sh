#!/usr/bin/env bash

export PYTHONPATH=janggi:${PYTHONPATH}
python -m unittest discover -v -s janggi/
