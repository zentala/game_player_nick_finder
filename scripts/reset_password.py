#!/usr/bin/env python
"""
Django management script to reset user password.
Usage: python reset_password.py <username> <new_password>
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

User = get_user_model()

def reset_password(username, new_password):
    """Reset user password."""
    try:
        if not User.objects.filter(username=username).exists():
            print(f"ERROR: User '{username}' does not exist!")
            return False
        
        user = User.objects.get(username=username)
        user.set_password(new_password)
        user.save()
        
        print(f"Password reset successfully for user '{username}'")
        print(f"New password: {new_password}")
        return True
    except Exception as e:
        print(f"Error resetting password: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python reset_password.py <username> <new_password>", file=sys.stderr)
        sys.exit(1)
    
    username = sys.argv[1]
    new_password = sys.argv[2]
    success = reset_password(username, new_password)
    sys.exit(0 if success else 1)

