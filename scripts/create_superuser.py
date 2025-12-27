#!/usr/bin/env python
"""
Django management script to create superuser automatically.
This script can be used by shell scripts to create superuser non-interactively.
"""
import os
import sys
import django

# Setup Django
# Get project root (parent of scripts directory)
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
sys.path.insert(0, project_root)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'game_player_nick_finder.settings.local')
django.setup()

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

def create_superuser(username, email, password):
    """Create superuser if it doesn't exist."""
    try:
        if User.objects.filter(username=username).exists():
            print(f"Superuser '{username}' already exists. Skipping creation.")
            return True  # Success - user already exists, no need to create
        
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        
        # Ensure user is active
        user.is_active = True
        user.save()
        
        # Verify email in allauth if allauth is installed
        try:
            from allauth.account.models import EmailAddress
            # Delete existing email addresses for this user
            EmailAddress.objects.filter(user=user).delete()
            # Create verified email address
            EmailAddress.objects.create(
                user=user,
                email=email,
                verified=True,
                primary=True
            )
        except ImportError:
            # allauth not installed, skip
            pass
        except Exception:
            # Ignore errors - email verification is optional
            pass
        
        print(f"Superuser '{username}' created successfully!")
        return True
    except ValidationError as e:
        print(f"Error creating superuser: {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return False

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python create_superuser.py <username> <email> <password>", file=sys.stderr)
        sys.exit(1)
    
    username = sys.argv[1]
    email = sys.argv[2]
    password = sys.argv[3]
    
    success = create_superuser(username, email, password)
    sys.exit(0 if success else 1)

