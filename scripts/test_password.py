#!/usr/bin/env python
"""
Django management script to test user password authentication.
Usage: python test_password.py <username> <password>
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

User = get_user_model()

def test_password(username, password):
    """Test if password authentication works for user."""
    try:
        # Try to authenticate
        user = authenticate(username=username, password=password)
        
        if user is not None:
            print(f"SUCCESS: Password authentication works for user '{username}'")
            print(f"User is active: {user.is_active}")
            print(f"User is authenticated: {user.is_authenticated}")
            return True
        else:
            print(f"FAILED: Password authentication failed for user '{username}'")
            print("Possible reasons:")
            print("  1. Incorrect password")
            print("  2. User is inactive (is_active=False)")
            print("  3. Email not verified (if ACCOUNT_EMAIL_VERIFICATION is required)")
            return False
    except Exception as e:
        print(f"Error testing password: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python test_password.py <username> <password>", file=sys.stderr)
        sys.exit(1)
    
    username = sys.argv[1]
    password = sys.argv[2]
    success = test_password(username, password)
    sys.exit(0 if success else 1)

