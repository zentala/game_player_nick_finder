#!/bin/bash

# Check Python3/Python
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "Neither Python3 nor Python is installed."
    exit 1
fi

# Check Python version
python_version=$($PYTHON_CMD -c 'import sys; print(sys.version_info.major, sys.version_info.minor)')
read -r major minor <<< "$python_version"

if [[ "$major" -lt 3 || ("$major" -eq 3 && "$minor" -lt 8) ]]; then
    echo "Python 3.8 or newer is required."
    exit 1
fi

# Check pipenv
if ! command -v pipenv &> /dev/null; then
    echo "pipenv is not installed."
    exit 1
fi

echo "Environment is ready."
