#!/bin/bash

# Bash script to create Django superuser
# Usage: ./create_superuser.sh [--auto]
# In auto mode, reads credentials from .dot/sudo_user file
# In interactive mode, prompts for credentials and saves them

AUTO_MODE=false
if [[ "$1" == "--auto" ]]; then
    AUTO_MODE=true
fi

DOT_DIR=".dot"
SUDO_USER_FILE="$DOT_DIR/sudo_user"

# Check if pipenv is available
if ! command -v pipenv &> /dev/null; then
    echo "Error: pipenv is not installed or not in PATH"
    echo "Install it with: pip install pipenv"
    exit 1
fi

# Function to read credentials from file
read_credentials_from_file() {
    local file_path="$1"
    
    if [[ ! -f "$file_path" ]]; then
        return 1
    fi
    
    local username=""
    local email=""
    local password=""
    
    while IFS= read -r line || [[ -n "$line" ]]; do
        if [[ $line =~ ^username:[[:space:]]*(.+)$ ]]; then
            username="${BASH_REMATCH[1]}"
        elif [[ $line =~ ^email:[[:space:]]*(.+)$ ]]; then
            email="${BASH_REMATCH[1]}"
        elif [[ $line =~ ^password:[[:space:]]*(.+)$ ]]; then
            password="${BASH_REMATCH[1]}"
        fi
    done < "$file_path"
    
    if [[ -z "$username" ]] || [[ -z "$email" ]] || [[ -z "$password" ]]; then
        return 1
    fi
    
    CREDENTIALS_USERNAME="$username"
    CREDENTIALS_EMAIL="$email"
    CREDENTIALS_PASSWORD="$password"
    return 0
}

# Function to save credentials to file
save_credentials_to_file() {
    local file_path="$1"
    local username="$2"
    local email="$3"
    local password="$4"
    
    local dir=$(dirname "$file_path")
    mkdir -p "$dir"
    
    cat > "$file_path" <<EOF
username: $username
email: $email
password: $password
EOF
    
    echo "Credentials saved to $file_path"
}

# Function to prompt for credentials
get_credentials_from_user() {
    echo ""
    echo "Enter superuser credentials:"
    read -p "Username: " username
    read -p "Email: " email
    read -sp "Password: " password
    echo ""
    
    CREDENTIALS_USERNAME="$username"
    CREDENTIALS_EMAIL="$email"
    CREDENTIALS_PASSWORD="$password"
}

# Main logic
if [[ "$AUTO_MODE" == true ]]; then
    # Auto mode: read from file
    if [[ -f "$SUDO_USER_FILE" ]]; then
        echo "Reading credentials from $SUDO_USER_FILE..."
        if ! read_credentials_from_file "$SUDO_USER_FILE"; then
            echo "Error: Invalid credentials file format"
            echo "Please run without --auto flag to create credentials file"
            exit 1
        fi
    else
        echo "Error: Credentials file not found: $SUDO_USER_FILE"
        echo "Please run without --auto flag to create credentials file first"
        exit 1
    fi
else
    # Interactive mode: prompt or read from file
    if [[ -f "$SUDO_USER_FILE" ]]; then
        echo "Found existing credentials file: $SUDO_USER_FILE"
        read -p "Use existing credentials? (y/n): " use_existing
        
        if [[ "$use_existing" == "y" ]] || [[ "$use_existing" == "Y" ]]; then
            if ! read_credentials_from_file "$SUDO_USER_FILE"; then
                echo "Error: Failed to read credentials file"
                exit 1
            fi
        else
            get_credentials_from_user
            save_credentials_to_file "$SUDO_USER_FILE" \
                "$CREDENTIALS_USERNAME" \
                "$CREDENTIALS_EMAIL" \
                "$CREDENTIALS_PASSWORD"
        fi
    else
        # First time: prompt and save
        get_credentials_from_user
        save_credentials_to_file "$SUDO_USER_FILE" \
            "$CREDENTIALS_USERNAME" \
            "$CREDENTIALS_EMAIL" \
            "$CREDENTIALS_PASSWORD"
    fi
fi

# Create superuser using Python script
echo ""
echo "Creating superuser..."

# Get script directory (where this script is located)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT_PATH="$SCRIPT_DIR/scripts/create_superuser.py"

if [[ ! -f "$SCRIPT_PATH" ]]; then
    # Try relative to current directory
    SCRIPT_PATH="scripts/create_superuser.py"
    if [[ ! -f "$SCRIPT_PATH" ]]; then
        SCRIPT_PATH="./scripts/create_superuser.py"
    fi
fi

pipenv run python "$SCRIPT_PATH" \
    "$CREDENTIALS_USERNAME" \
    "$CREDENTIALS_EMAIL" \
    "$CREDENTIALS_PASSWORD"

if [[ $? -eq 0 ]]; then
    echo ""
    echo "Superuser creation completed!"
else
    echo ""
    echo "Error: Failed to create superuser"
    exit 1
fi

