# PowerShell script to set up Django development environment
# This script sets up the virtual environment, installs dependencies, and prepares the database

Write-Host "Setting up Django development environment..." -ForegroundColor Cyan

# Check if pipenv is available
if (-not (Get-Command pipenv -ErrorAction SilentlyContinue)) {
    Write-Host "Error: pipenv is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Install it with: pip install pipenv" -ForegroundColor Yellow
    exit 1
}

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pipenv install --python 3.11

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Failed to install dependencies" -ForegroundColor Red
    exit 1
}

Write-Host "Dependencies installed successfully!" -ForegroundColor Green

# Run migrations
Write-Host "Running database migrations..." -ForegroundColor Yellow
pipenv run python manage.py migrate sites
pipenv run python manage.py migrate

if ($LASTEXITCODE -ne 0) {
    Write-Host "Warning: Some migrations may have failed" -ForegroundColor Yellow
}

Write-Host "`nSetup complete! You can now:" -ForegroundColor Green
Write-Host "  1. Run '.\start_django.ps1' to start the development server" -ForegroundColor Cyan
Write-Host "  2. Run 'pipenv run python manage.py createsuperuser' to create an admin user" -ForegroundColor Cyan
Write-Host "  3. Run 'pipenv run python manage.py loaddata app/fixtures/categories_fixtures.json' to load fixtures" -ForegroundColor Cyan

