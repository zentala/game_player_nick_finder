#!/bin/bash

# Find the path to the virtual environment
VENV_PATH=$(pipenv --venv)

# Activate the virtual environment
source "$VENV_PATH/bin/activate"

# Check if the environment is activated
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "Virtual environment activated."
else
    echo "Failed to activate virtual environment."
    exit 1
fi

# Install dependencies
pipenv install

# Run Django server
pipenv run python manage.py runserver
