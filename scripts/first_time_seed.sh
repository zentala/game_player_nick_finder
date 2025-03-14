#!/bin/bash

# Script to check if the database is empty and load fixtures if it is
# This is designed to run only on first deployment or when explicitly called

# Function to check if a table is empty
check_table_empty() {
  TABLE_NAME=$1
  COUNT=$(python -c "import django; django.setup(); from app.models import $TABLE_NAME; print($TABLE_NAME.objects.count())")
  
  if [ "$COUNT" -eq "0" ]; then
    return 0  # Table is empty
  else
    return 1  # Table has records
  fi
}

# Set up Django environment
export DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:-game_player_nick_finder.settings.production}

echo "🔍 Checking if database needs seeding..."

# Check if Game table is empty (as indicator for first run)
DB_CHECK=$(python -c "import django; django.setup(); from app.models import Game; print(Game.objects.count())" 2>/dev/null || echo "error")

if [ "$DB_CHECK" = "error" ]; then
  echo "⚠️ Could not check database state. This might be normal if migrations are incomplete."
  echo "   Seeding will be skipped for now."
elif [ "$DB_CHECK" = "0" ]; then
  echo "📊 Database appears to be empty. Running first-time seeding..."
  
  # Load fixtures in the correct order
  echo "  ↪ Loading Categories..."
  python manage.py loaddata app/fixtures/categories_fixtures.json || { echo "❌ Failed to load categories"; exit 1; }
  
  echo "  ↪ Loading Games..."
  python manage.py loaddata app/fixtures/games_fixtures.json || { echo "❌ Failed to load games"; exit 1; }
  
  # Conditionally load users data (usually not for production)
  if [ "$LOAD_USER_FIXTURES" = "true" ]; then
    echo "  ↪ Loading Users and characters..."
    python manage.py loaddata app/fixtures/users_and_characters.json || { echo "❌ Failed to load users"; exit 1; }
  else
    echo "  ↪ Skipping users fixture (set LOAD_USER_FIXTURES=true to load)"
  fi
  
  # Create a flag file to indicate seeding was done
  touch .db_seeded
  
  echo "✅ Database seeding completed successfully!"
else
  echo "🔄 Database already contains data. Skipping seeding."
fi