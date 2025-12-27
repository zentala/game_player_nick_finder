# PowerShell script to check user account status
# Usage: .\check_user.ps1 <username>

param(
    [Parameter(Mandatory=$true)]
    [string]$Username
)

Write-Host "Checking User Account Status" -ForegroundColor Cyan
Write-Host "=============================" -ForegroundColor Cyan

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

$scriptPath = Join-Path $scriptDir "scripts\check_user.py"

Write-Host "`nChecking user: $Username" -ForegroundColor Yellow

pipenv run python $scriptPath $Username

if ($LASTEXITCODE -ne 0) {
    Write-Host "`nError: Failed to check user" -ForegroundColor Red
    exit 1
}
