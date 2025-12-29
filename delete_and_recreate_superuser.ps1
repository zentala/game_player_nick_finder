# PowerShell script to delete existing superuser and create a new one
# Usage: .\delete_and_recreate_superuser.ps1

Write-Host "Delete and Recreate Superuser" -ForegroundColor Cyan
Write-Host "==============================" -ForegroundColor Cyan

# Check if pipenv is available
if (-not (Get-Command pipenv -ErrorAction SilentlyContinue)) {
    Write-Host "Error: pipenv is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Install it with: pip install pipenv" -ForegroundColor Yellow
    exit 1
}

Write-Host "`nEnter new superuser credentials:" -ForegroundColor Yellow

$username = Read-Host "Username"
$email = Read-Host "Email"

# Secure password input
$securePassword = Read-Host "Password" -AsSecureString
$password = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
    [Runtime.InteropServices.Marshal]::SecureStringToBSTR($securePassword)
)

# Get script directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not $scriptDir) {
    $scriptDir = Get-Location
}

$scriptPath = Join-Path $scriptDir "scripts\delete_and_recreate_superuser.py"
if (-not (Test-Path $scriptPath)) {
    $scriptPath = Join-Path (Get-Location) "scripts\delete_and_recreate_superuser.py"
}

Write-Host "`nDeleting existing user and creating new superuser..." -ForegroundColor Yellow

# Escape special characters in password for PowerShell
$passwordEscaped = $password -replace '"', '`"'

pipenv run python $scriptPath "$username" "$email" "$passwordEscaped"

if ($LASTEXITCODE -eq 0) {
    Write-Host "`nSuperuser recreated successfully!" -ForegroundColor Green
    Write-Host "`nDjango Admin Panel: http://localhost:7600/admin/" -ForegroundColor Cyan
} else {
    Write-Host "`nError: Failed to recreate superuser" -ForegroundColor Red
    exit 1
}
