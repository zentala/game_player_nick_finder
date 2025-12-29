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

# Set passwords for test users
echo ""
echo "Setting passwords for test users..."
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SETUP_TEST_USERS_SCRIPT="$SCRIPT_DIR/setup_test_users.sh"

if [ -f "$SETUP_TEST_USERS_SCRIPT" ]; then
    bash "$SETUP_TEST_USERS_SCRIPT"
    if [ $? -ne 0 ]; then
        echo ""
        echo "Warning: Failed to set test user passwords"
        echo "Run './setup_test_users.sh' manually to set passwords"
    fi
else
    echo ""
    echo "Note: setup_test_users.sh not found. Skipping password setup."
    echo "Run './setup_test_users.sh' manually to set test user passwords"
fi
echo "  - Categories: 7 objects"
echo "  - Games: 17 objects"
echo "  - Users, Characters, Messages, Friend Requests, Friendships"

# Create superuser automatically if credentials file exists
echo ""
echo "Creating superuser..."

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CREATE_SUPERUSER_SCRIPT="$SCRIPT_DIR/create_superuser.sh"

if [[ -f "$CREATE_SUPERUSER_SCRIPT" ]]; then
    bash "$CREATE_SUPERUSER_SCRIPT" --auto
    if [[ $? -eq 0 ]]; then
        echo "Superuser created/verified successfully!"
    else
        echo "Note: Superuser creation skipped (credentials file may not exist)"
        echo "Run './create_superuser.sh' to create superuser manually"
    fi
else
    echo "Note: create_superuser.sh not found. Skipping superuser creation."
fi
