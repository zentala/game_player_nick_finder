#!/bin/bash

# Bash script to delete existing superuser and create a new one
# Usage: ./delete_and_recreate_superuser.sh

echo "Delete and Recreate Superuser"
echo "=============================="

# Check if pipenv is available
if ! command -v pipenv &> /dev/null; then
    echo "Error: pipenv is not installed or not in PATH"
    echo "Install it with: pip install pipenv"
    exit 1
fi

echo ""
echo "Enter new superuser credentials:"
read -p "Username: " username
read -p "Email: " email
read -sp "Password: " password
echo ""

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT_PATH="$SCRIPT_DIR/scripts/delete_and_recreate_superuser.py"

if [[ ! -f "$SCRIPT_PATH" ]]; then
    SCRIPT_PATH="scripts/delete_and_recreate_superuser.py"
    if [[ ! -f "$SCRIPT_PATH" ]]; then
        SCRIPT_PATH="./scripts/delete_and_recreate_superuser.py"
    fi
fi

echo ""
echo "Deleting existing user and creating new superuser..."

pipenv run python "$SCRIPT_PATH" "$username" "$email" "$password"

if [[ $? -eq 0 ]]; then
    echo ""
    echo "Superuser recreated successfully!"
    echo ""
    echo "Django Admin Panel: http://localhost:7600/admin/"
else
    echo ""
    echo "Error: Failed to recreate superuser"
    exit 1
fi
