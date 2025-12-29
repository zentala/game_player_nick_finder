#!/bin/bash
# Bash script to set passwords for test users
# Sets passwords for test users defined in tests/helpers/auth-helpers.ts

echo "Setting passwords for test users..."

# Check if pipenv is available
if ! command -v pipenv &> /dev/null; then
    echo "Error: pipenv is not installed or not in PATH"
    echo "Install it with: pip install pipenv"
    exit 1
fi

# Test users and their passwords (from tests/helpers/auth-helpers.ts)
echo ""
echo "Updating test user passwords..."

pipenv run python manage.py shell << 'EOF'
from django.contrib.auth import get_user_model
import sys

User = get_user_model()
errors = []

test_users = [
    ('testuser', 'testpass123'),
    ('otheruser', 'pass'),
    ('privateuser', 'testpass123'),
]

for username, password in test_users:
    try:
        user = User.objects.get(username=username)
        user.set_password(password)
        user.is_active = True
        user.save()
        print(f'✓ Password set for user: {username}')
    except User.DoesNotExist:
        errors.append(f'User {username} does not exist')
        print(f'✗ User not found: {username}')
    except Exception as e:
        errors.append(f'Error setting password for {username}: {str(e)}')
        print(f'✗ Error for {username}: {str(e)}')

if errors:
    print(f'\nErrors occurred: {len(errors)}')
    for error in errors:
        print(f'  - {error}')
    sys.exit(1)
else:
    print(f'\n✓ All test user passwords set successfully!')
    sys.exit(0)
EOF

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ All test user passwords set successfully!"
    echo ""
    echo "Test users ready:"
    echo "  - testuser / testpass123"
    echo "  - otheruser / pass"
    echo "  - privateuser / testpass123"
else
    echo ""
    echo "✗ Some errors occurred while setting passwords"
    exit 1
fi

