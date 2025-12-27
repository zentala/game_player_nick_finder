# PowerShell script to create Django superuser
# Usage: .\create_superuser.ps1 [--auto]
# In auto mode, reads credentials from .dot/sudo_user file
# In interactive mode, prompts for credentials and saves them

param(
    [switch]$Auto
)

$DotDir = ".dot"
$SudoUserFile = Join-Path $DotDir "sudo_user"

# Check if pipenv is available
if (-not (Get-Command pipenv -ErrorAction SilentlyContinue)) {
    Write-Host "Error: pipenv is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Install it with: pip install pipenv" -ForegroundColor Yellow
    exit 1
}

# Function to read credentials from file
function Read-CredentialsFromFile {
    param([string]$FilePath)
    
    if (-not (Test-Path $FilePath)) {
        return $null
    }
    
    $content = Get-Content $FilePath -Raw
    $lines = $content -split "`n" | Where-Object { $_.Trim() -ne "" }
    
    $credentials = @{}
    foreach ($line in $lines) {
        if ($line -match "^(\w+):\s*(.+)$") {
            $key = $matches[1].ToLower()
            $value = $matches[2].Trim()
            $credentials[$key] = $value
        }
    }
    
    if ($credentials.Count -eq 0) {
        return $null
    }
    
    return $credentials
}

# Function to save credentials to file
function Save-CredentialsToFile {
    param(
        [string]$FilePath,
        [string]$Username,
        [string]$Email,
        [string]$Password
    )
    
    $dir = Split-Path $FilePath -Parent
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
    
    $content = @"
username: $Username
email: $Email
password: $Password
"@
    
    $content | Out-File -FilePath $FilePath -Encoding utf8 -NoNewline
    Write-Host "Credentials saved to $FilePath" -ForegroundColor Green
}

# Function to prompt for credentials
function Get-CredentialsFromUser {
    Write-Host "`nEnter superuser credentials:" -ForegroundColor Cyan
    
    $username = Read-Host "Username"
    $email = Read-Host "Email"
    
    # Secure password input
    $securePassword = Read-Host "Password" -AsSecureString
    $password = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
        [Runtime.InteropServices.Marshal]::SecureStringToBSTR($securePassword)
    )
    
    return @{
        Username = $username
        Email = $email
        Password = $password
    }
}

# Main logic
$credentials = $null

if ($Auto) {
    # Auto mode: read from file
    if (Test-Path $SudoUserFile) {
        Write-Host "Reading credentials from $SudoUserFile..." -ForegroundColor Yellow
        $credentials = Read-CredentialsFromFile -FilePath $SudoUserFile
        
        if ($null -eq $credentials -or -not $credentials.ContainsKey('username')) {
            Write-Host "Error: Invalid credentials file format" -ForegroundColor Red
            Write-Host "Please run without --auto flag to create credentials file" -ForegroundColor Yellow
            exit 1
        }
    } else {
        Write-Host "Error: Credentials file not found: $SudoUserFile" -ForegroundColor Red
        Write-Host "Please run without --auto flag to create credentials file first" -ForegroundColor Yellow
        exit 1
    }
} else {
    # Interactive mode: prompt or read from file
    if (Test-Path $SudoUserFile) {
        Write-Host "Found existing credentials file: $SudoUserFile" -ForegroundColor Cyan
        $useExisting = Read-Host "Use existing credentials? (y/n)"
        
        if ($useExisting -eq 'y' -or $useExisting -eq 'Y') {
            $credentials = Read-CredentialsFromFile -FilePath $SudoUserFile
        } else {
            $credentials = Get-CredentialsFromUser
            Save-CredentialsToFile -FilePath $SudoUserFile `
                -Username $credentials.Username `
                -Email $credentials.Email `
                -Password $credentials.Password
        }
    } else {
        # First time: prompt and save
        $credentials = Get-CredentialsFromUser
        Save-CredentialsToFile -FilePath $SudoUserFile `
            -Username $credentials.Username `
            -Email $credentials.Email `
            -Password $credentials.Password
    }
}

# Create superuser using Python script
Write-Host "`nCreating superuser..." -ForegroundColor Yellow

# Get script directory (where this script is located)
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not $scriptDir) {
    $scriptDir = Get-Location
}

$scriptPath = Join-Path $scriptDir "scripts\create_superuser.py"
if (-not (Test-Path $scriptPath)) {
    # Try relative to current directory
    $scriptPath = Join-Path (Get-Location) "scripts\create_superuser.py"
}

$username = $credentials.Username
$email = $credentials.Email
$password = $credentials.Password

# Escape special characters in password for PowerShell
$passwordEscaped = $password -replace '"', '`"'

pipenv run python $scriptPath "$username" "$email" "$passwordEscaped"

if ($LASTEXITCODE -eq 0) {
    Write-Host "`nSuperuser creation completed!" -ForegroundColor Green
} else {
    Write-Host "`nError: Failed to create superuser" -ForegroundColor Red
    exit 1
}
