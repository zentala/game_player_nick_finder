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
            print(f"Email address verified in allauth")
        except ImportError:
            # allauth not installed, skip
            pass
        except Exception as e:
            print(f"Warning: Could not verify email in allauth: {e}")
        
        print(f"Superuser '{username}' created successfully!")
        print(f"User is_active: {user.is_active}")
        print(f"\nYou can now login at: http://localhost:8000/accounts/login/")
        print(f"Username: {username}")
        print(f"Email: {email}")
        return True
    except ValidationError as e:
        print(f"Error creating superuser: {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
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

