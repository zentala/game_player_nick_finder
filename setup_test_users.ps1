# PowerShell script to set passwords for test users
# Sets passwords for test users defined in tests/helpers/auth-helpers.ts

Write-Host "Setting passwords for test users..." -ForegroundColor Cyan

# Check if pipenv is available
if (-not (Get-Command pipenv -ErrorAction SilentlyContinue)) {
    Write-Host "Error: pipenv is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Install it with: pip install pipenv" -ForegroundColor Yellow
    exit 1
}

# Test users and their passwords (from tests/helpers/auth-helpers.ts)
$testUsers = @(
    @{ username = "testuser"; password = "testpass123" },
    @{ username = "otheruser"; password = "pass" },
    @{ username = "privateuser"; password = "testpass123" }
)

Write-Host "`nUpdating test user passwords..." -ForegroundColor Yellow

$scriptContent = @"
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
"@

# Save script to temporary file
$tempScript = Join-Path $env:TEMP "setup_test_users_$(Get-Date -Format 'yyyyMMddHHmmss').py"
$scriptContent | Out-File -FilePath $tempScript -Encoding UTF8

try {
    # Run the script using Get-Content and pipe (PowerShell way)
    # PowerShell doesn't support < operator, so we use Get-Content and pipe
    Get-Content $tempScript | pipenv run python manage.py shell
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n✓ All test user passwords set successfully!" -ForegroundColor Green
        Write-Host "`nTest users ready:" -ForegroundColor Cyan
        foreach ($user in $testUsers) {
            Write-Host "  - $($user.username) / $($user.password)" -ForegroundColor Cyan
        }
    } else {
        Write-Host "`n✗ Some errors occurred while setting passwords" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "`n✗ Error running script: $_" -ForegroundColor Red
    exit 1
} finally {
    # Clean up temporary file if it exists
    if (Test-Path $tempScript) {
        Remove-Item $tempScript -Force -ErrorAction SilentlyContinue
    }
}

