#!/bin/bash

# Check for Python
if ! command -v python &> /dev/null; then
  echo "Python is not installed."
  exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(sys.version_info.major, sys.version_info.minor)')
read -r major minor <<< "$python_version"

if [[ "$major" -lt 3 || ("$major" -eq 3 && "$minor" -lt 8) ]]; then
  echo "You need Python 3.8 or higher."
  exit 1
fi


# Check for pipenv
if ! command -v pipenv &> /dev/null; then
  echo "pipenv is not installed."
  exit 1
fi


# Check for nvm
source ~/.nvm/nvm.sh
if ! command -v nvm &> /dev/null; then
  echo "nvm is not installed."
  exit 1
fi


# Check for npm
if ! command -v npm &> /dev/null; then
  echo "npm is not installed."
  exit 1
fi

echo "Environment is ready."
