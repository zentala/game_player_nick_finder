# PowerShell script to fix user account (activate and verify email)
# Usage: .\fix_user.ps1 <username>

param(
    [Parameter(Mandatory=$true)]
    [string]$Username
)

Write-Host "Fix User Account" -ForegroundColor Cyan
Write-Host "================" -ForegroundColor Cyan

# Check if pipenv is available
if (-not (Get-Command pipenv -ErrorAction SilentlyContinue)) {
    Write-Host "Error: pipenv is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Install it with: pip install pipenv" -ForegroundColor Yellow
    exit 1
}

# Get script directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not $scriptDir) {
    $scriptDir = Get-Location
}

$scriptPath = Join-Path $scriptDir "scripts\fix_user.py"

Write-Host "`nFixing user: $Username" -ForegroundColor Yellow

pipenv run python $scriptPath $Username

if ($LASTEXITCODE -eq 0) {
    Write-Host "`nUser fixed successfully!" -ForegroundColor Green
    Write-Host "`nTry logging in at: http://localhost:8000/accounts/login/" -ForegroundColor Cyan
} else {
    Write-Host "`nError: Failed to fix user" -ForegroundColor Red
    exit 1
}

