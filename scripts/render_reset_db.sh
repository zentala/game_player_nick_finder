#!/bin/bash

# Script to be run manually on Render when you want to completely reset the database
# WARNING: This will delete all data in the database!

# Set up Django environment
export DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:-game_player_nick_finder.settings.production}

echo "⚠️ WARNING: This will delete ALL DATA in your database! ⚠️"
echo "Type 'yes' to continue:"
read CONFIRMATION

if [ "$CONFIRMATION" != "yes" ]; then
  echo "Operation cancelled."
  exit 1
fi

echo "🗑️ Flushing database..."
python manage.py flush --no-input

# Remove the seeding flag file if it exists
if [ -f ".db_seeded" ]; then
  rm .db_seeded
fi

echo "🔄 Applying migrations..."
python manage.py migrate

echo "🌱 Running database seeding..."
bash scripts/first_time_seed.sh

echo "✅ Database has been reset and re-seeded successfully!"
