#!/usr/bin/env python
"""
Django management script to check user account status and authentication.
Usage: python check_user.py <username>
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

from django.contrib.auth import get_user_model, authenticate
from allauth.account.models import EmailAddress

User = get_user_model()

def check_user(username):
    """Check user account status and authentication details."""
    try:
        # Check if user exists
        if not User.objects.filter(username=username).exists():
            print(f"ERROR: User '{username}' does not exist!")
            return False
        
        user = User.objects.get(username=username)
        print(f"\n=== User Account Information ===")
        print(f"Username: {user.username}")
        print(f"Email: {user.email}")
        print(f"Is Active: {user.is_active}")
        print(f"Is Staff: {user.is_staff}")
        print(f"Is Superuser: {user.is_superuser}")
        print(f"Password (hashed): {user.password[:50]}...")
        print(f"Last Login: {user.last_login}")
        
        # Check email verification status (for allauth)
        try:
            email_address = EmailAddress.objects.get(email=user.email, user=user)
            print(f"\n=== Email Verification Status ===")
            print(f"Email Verified: {email_address.verified}")
            print(f"Primary Email: {email_address.primary}")
            if not email_address.verified:
                print("WARNING: Email is not verified! This may prevent login.")
        except EmailAddress.DoesNotExist:
            print(f"\n=== Email Verification Status ===")
            print("WARNING: No EmailAddress record found in allauth!")
            print("This user may have been created outside of allauth.")
        
        # Test password authentication
        print(f"\n=== Authentication Test ===")
        print("To test password, run:")
        print(f"  python scripts/test_password.py {username} <password>")
        
        return True
    except Exception as e:
        print(f"Error checking user: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python check_user.py <username>", file=sys.stderr)
        sys.exit(1)
    
    username = sys.argv[1]
    success = check_user(username)
    sys.exit(0 if success else 1)

