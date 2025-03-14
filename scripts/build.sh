#!/usr/bin/env bash
# exit on error
set -o errexit

pip install pipenv
pipenv install --deploy --system

python manage.py collectstatic --no-input
python manage.py migrate

# Run first-time seeding check after migrations
echo "🌱 Checking if initial database seeding is needed..."
bash scripts/first_time_seed.sh || echo "⚠️ Seeding was not completed. You may need to run it manually."