#!/usr/bin/env python
"""
Django management script to fix all users (activate and verify email).
Usage: python fix_all_users.py
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

def fix_all_users():
    """Fix all user accounts: activate and verify email."""
    try:
        users = User.objects.all()
        print(f"Found {users.count()} users")
        
        fixed_count = 0
        for user in users:
            changed = False
            
            # Ensure user is active
            if not user.is_active:
                user.is_active = True
                user.save()
                changed = True
                print(f"  Activated user '{user.username}'")
            
            # Verify email in allauth
            try:
                from allauth.account.models import EmailAddress
                
                if user.email:
                    email_count = EmailAddress.objects.filter(user=user).count()
                    if email_count == 0:
                        # Create verified email address
                        EmailAddress.objects.create(
                            user=user,
                            email=user.email,
                            verified=True,
                            primary=True
                        )
                        changed = True
                        print(f"  Verified email for user '{user.username}': {user.email}")
                    else:
                        # Update existing email addresses to verified
                        emails = EmailAddress.objects.filter(user=user)
                        for email in emails:
                            if not email.verified:
                                email.verified = True
                                email.save()
                                changed = True
                                print(f"  Verified existing email for user '{user.username}': {email.email}")
            except ImportError:
                print("WARNING: allauth not installed, skipping email verification")
            except Exception as e:
                print(f"WARNING: Could not verify email for '{user.username}': {e}")
            
            if changed:
                fixed_count += 1
        
        print(f"\nFixed {fixed_count} out of {users.count()} users")
        return True
    except Exception as e:
        print(f"Error fixing users: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = fix_all_users()
    sys.exit(0 if success else 1)

