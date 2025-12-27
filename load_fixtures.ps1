# PowerShell script to load all Django fixtures
# Loads categories and games fixtures

Write-Host "Loading Django fixtures..." -ForegroundColor Cyan

# Check if pipenv is available
if (-not (Get-Command pipenv -ErrorAction SilentlyContinue)) {
    Write-Host "Error: pipenv is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Install it with: pip install pipenv" -ForegroundColor Yellow
    exit 1
}

Write-Host "Loading categories fixtures..." -ForegroundColor Yellow
pipenv run python manage.py loaddata app/fixtures/categories_fixtures.json

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Failed to load categories fixtures" -ForegroundColor Red
    exit 1
}

Write-Host "Loading games fixtures..." -ForegroundColor Yellow
pipenv run python manage.py loaddata app/fixtures/games_fixtures.json

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Failed to load games fixtures" -ForegroundColor Red
    exit 1
}

Write-Host "Loading users and characters fixtures..." -ForegroundColor Yellow
pipenv run python manage.py loaddata app/fixtures/users_and_characters.json

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Failed to load users and characters fixtures" -ForegroundColor Red
    exit 1
}

Write-Host "`nAll fixtures loaded successfully!" -ForegroundColor Green
Write-Host "  - Categories: 7 objects" -ForegroundColor Cyan
Write-Host "  - Games: 17 objects" -ForegroundColor Cyan
Write-Host "  - Users, Characters, Messages, Friend Requests, Friendships" -ForegroundColor Cyan

# Create superuser automatically if credentials file exists
Write-Host "`nCreating superuser..." -ForegroundColor Yellow
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not $scriptDir) {
    $scriptDir = Get-Location
}

$createSuperuserScript = Join-Path $scriptDir "create_superuser.ps1"
if (Test-Path $createSuperuserScript) {
    & $createSuperuserScript -Auto
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Superuser created/verified successfully!" -ForegroundColor Green
    } else {
        Write-Host "Note: Superuser creation skipped (credentials file may not exist)" -ForegroundColor Yellow
        Write-Host "Run '.\create_superuser.ps1' to create superuser manually" -ForegroundColor Cyan
    }
} else {
    Write-Host "Note: create_superuser.ps1 not found. Skipping superuser creation." -ForegroundColor Yellow
}

