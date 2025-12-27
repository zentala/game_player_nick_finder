# PowerShell script to start Django development server
# This script activates pipenv environment and runs Django server

Write-Host "Starting Django development environment..." -ForegroundColor Cyan

# Check if pipenv is available
if (-not (Get-Command pipenv -ErrorAction SilentlyContinue)) {
    Write-Host "Error: pipenv is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Install it with: pip install pipenv" -ForegroundColor Yellow
    exit 1
}

# Install dependencies if needed
Write-Host "Installing/updating dependencies..." -ForegroundColor Yellow
pipenv install

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Failed to install dependencies" -ForegroundColor Red
    exit 1
}

# Run Django server
Write-Host "Starting Django development server..." -ForegroundColor Green
pipenv run python manage.py runserver
