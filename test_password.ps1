# PowerShell script to test user password authentication
# Usage: .\test_password.ps1 <username> <password>

param(
    [Parameter(Mandatory=$true)]
    [string]$Username,
    
    [Parameter(Mandatory=$true)]
    [string]$Password
)

Write-Host "Test Password Authentication" -ForegroundColor Cyan
Write-Host "============================" -ForegroundColor Cyan

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

$scriptPath = Join-Path $scriptDir "scripts\test_password.py"

Write-Host "`nTesting password for user: $Username" -ForegroundColor Yellow

pipenv run python $scriptPath $Username $Password

if ($LASTEXITCODE -eq 0) {
    Write-Host "`nPassword authentication successful!" -ForegroundColor Green
} else {
    Write-Host "`nPassword authentication failed!" -ForegroundColor Red
    exit 1
}
