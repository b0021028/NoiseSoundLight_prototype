#!/bin/bash

sudo pigpiod
source "$(dirname "$0")/.venv/bin/activate"
python3 "$(dirname "$0")/prototype20240129/core.py"
