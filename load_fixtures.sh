#!/bin/bash

# Bash script to load all Django fixtures
# Loads categories and games fixtures

echo "Loading Django fixtures..."

# Check if pipenv is available
if ! command -v pipenv &> /dev/null; then
    echo "Error: pipenv is not installed or not in PATH"
    echo "Install it with: pip install pipenv"
    exit 1
fi

echo "Loading categories fixtures..."
pipenv run python manage.py loaddata app/fixtures/categories_fixtures.json

if [ $? -ne 0 ]; then
    echo "Error: Failed to load categories fixtures"
    exit 1
fi

echo "Loading games fixtures..."
pipenv run python manage.py loaddata app/fixtures/games_fixtures.json

if [ $? -ne 0 ]; then
    echo "Error: Failed to load games fixtures"
    exit 1
fi

echo "Loading users and characters fixtures..."
pipenv run python manage.py loaddata app/fixtures/users_and_characters.json

if [ $? -ne 0 ]; then
    echo "Error: Failed to load users and characters fixtures"
    exit 1
fi

echo ""
echo "All fixtures loaded successfully!"
echo "  - Categories: 7 objects"
echo "  - Games: 17 objects"
echo "  - Users, Characters, Messages, Friend Requests, Friendships"

