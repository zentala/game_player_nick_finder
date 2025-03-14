#!/usr/bin/env bash
# exit on error
set -o errexit

pip install pipenv
pipenv install --deploy --system

python manage.py collectstatic --no-input
python manage.py migrate