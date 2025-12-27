#!/usr/bin/env python
"""
Django management script to fix user account (activate and verify email).
Usage: python fix_user.py <username>
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

def fix_user(username):
    """Fix user account: activate and verify email."""
    try:
        if not User.objects.filter(username=username).exists():
            print(f"ERROR: User '{username}' does not exist!")
            return False
        
        user = User.objects.get(username=username)
        
        # Ensure user is active
        if not user.is_active:
            user.is_active = True
            user.save()
            print(f"Activated user '{username}'")
        else:
            print(f"User '{username}' is already active")
        
        # Verify email in allauth
        try:
            from allauth.account.models import EmailAddress
            
            if user.email:
                # Delete existing email addresses for this user
                EmailAddress.objects.filter(user=user).delete()
                # Create verified email address
                email_address, created = EmailAddress.objects.get_or_create(
                    user=user,
                    email=user.email,
                    defaults={
                        'verified': True,
                        'primary': True
                    }
                )
                if not created:
                    email_address.verified = True
                    email_address.primary = True
                    email_address.save()
                
                print(f"Verified email address: {user.email}")
            else:
                print("WARNING: User has no email address set")
        except ImportError:
            print("WARNING: allauth not installed, skipping email verification")
        except Exception as e:
            print(f"WARNING: Could not verify email: {e}")
        
        print(f"\nUser '{username}' fixed successfully!")
        print(f"Is Active: {user.is_active}")
        print(f"Email: {user.email}")
        return True
    except Exception as e:
        print(f"Error fixing user: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python fix_user.py <username>", file=sys.stderr)
        sys.exit(1)
    
    username = sys.argv[1]
    success = fix_user(username)
    sys.exit(0 if success else 1)
