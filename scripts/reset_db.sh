#!/bin/bash

# Script to reset database and load fixtures
# Usage: ./scripts/reset_db.sh [--create-superuser]

echo "⚠️ This will delete your current database and all data! ⚠️"
read -p "Are you sure you want to continue? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    echo "Operation cancelled."
    exit 1
fi

echo "🗑️ Removing migrations..."
rm -f app/migrations/000*.py

echo "🗑️ Removing database..."
rm -f db.sqlite3

echo "🔄 Creating new migrations..."
python manage.py makemigrations app

echo "🔄 Applying migrations..."
python manage.py migrate

echo "📦 Loading fixtures..."
echo "  ↪ Categories..."
python manage.py loaddata app/fixtures/categories_fixtures.json
echo "  ↪ Games..."
python manage.py loaddata app/fixtures/games_fixtures.json
echo "  ↪ Users and characters..."
python manage.py loaddata app/fixtures/users_and_characters.json

# Tworzenie superusera tylko gdy podano parametr --create-superuser
if [[ "$1" == "--create-superuser" ]]; then
    echo "👤 Creating superuser..."
    # Use the new create_superuser script in auto mode
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
    CREATE_SUPERUSER_SCRIPT="$PROJECT_ROOT/create_superuser.sh"
    
    if [[ -f "$CREATE_SUPERUSER_SCRIPT" ]]; then
        bash "$CREATE_SUPERUSER_SCRIPT" --auto
    else
        python manage.py createsuperuser
    fi
else
    echo "ℹ️ Skipping superuser creation (use --create-superuser to create one)"
fi

echo "✅ Database reset completed successfully!"
echo "You can now run: python manage.py runserver"
