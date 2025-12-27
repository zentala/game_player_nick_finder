#!/usr/bin/env python
"""
Django management script to delete existing superuser and create a new one.
Usage: python delete_and_recreate_superuser.py <username> <email> <password>
"""
import os
import sys
import django

# Setup Django
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
sys.path.insert(0, project_root)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'game_player_nick_finder.settings.local')
django.setup()

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

def delete_and_recreate_superuser(username, email, password):
    """Delete existing user if exists and create new superuser."""
    try:
        # Delete existing user if exists
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            user.delete()
            print(f"Deleted existing user '{username}'")
        
        # Create new superuser
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        print(f"Superuser '{username}' created successfully!")
        print(f"\nYou can now login to Django admin at: http://localhost:8000/admin/")
        print(f"Username: {username}")
        print(f"Email: {email}")
        return True
    except ValidationError as e:
        print(f"Error creating superuser: {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return False

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python delete_and_recreate_superuser.py <username> <email> <password>", file=sys.stderr)
        sys.exit(1)
    
    username = sys.argv[1]
    email = sys.argv[2]
    password = sys.argv[3]
    
    success = delete_and_recreate_superuser(username, email, password)
    sys.exit(0 if success else 1)

