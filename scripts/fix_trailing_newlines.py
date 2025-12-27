#!/usr/bin/env python3
"""
Fix trailing newlines in files according to .editorconfig
- Remove all trailing newlines
- Add exactly one trailing newline (if insert_final_newline = true)
"""
import os
import sys
from pathlib import Path

# Directories to skip
SKIP_DIRS = {'.git', 'node_modules', '__pycache__', '.pytest_cache', 'venv', 'env', '.venv', 'media', 'static', 'playwright-report', 'test-results'}

# File extensions to process
EXTENSIONS = {'.py', '.ps1', '.sh', '.js', '.ts', '.html', '.md', '.json', '.css', '.txt', '.yaml', '.yml', '.config', '.toml'}

def should_process_file(file_path):
    """Check if file should be processed"""
    # Skip hidden files
    if file_path.name.startswith('.'):
        return False
    
    # Check extension
    if file_path.suffix not in EXTENSIONS:
        return False
    
    # Check if in skip directory
    parts = file_path.parts
    if any(part in SKIP_DIRS for part in parts):
        return False
    
    return True

def fix_trailing_newlines(file_path):
    """Fix trailing newlines in a file"""
    try:
        # Read file with binary mode to preserve line endings
        with open(file_path, 'rb') as f:
            content = f.read()
        
        # Decode content
        try:
            text = content.decode('utf-8')
        except UnicodeDecodeError:
            # Skip binary files
            return False
        
        # Remove all trailing newlines
        text = text.rstrip('\n\r')
        
        # Add exactly one newline at the end (LF as per .editorconfig)
        text += '\n'
        
        # Encode back
        new_content = text.encode('utf-8')
        
        # Only write if content changed
        if new_content != content:
            with open(file_path, 'wb') as f:
                f.write(new_content)
            return True
        
        return False
    except Exception as e:
        print(f"Error processing {file_path}: {e}", file=sys.stderr)
        return False

def main():
    """Main function"""
    base_dir = Path(__file__).parent.parent
    changed_files = []
    
    # Walk through all files
    for root, dirs, files in os.walk(base_dir):
        # Skip directories
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        
        for file in files:
            file_path = Path(root) / file
            
            if should_process_file(file_path):
                if fix_trailing_newlines(file_path):
                    changed_files.append(str(file_path.relative_to(base_dir)))
    
    if changed_files:
        print(f"Fixed trailing newlines in {len(changed_files)} files:")
        for f in sorted(changed_files):
            print(f"  {f}")
    else:
        print("No files needed fixing.")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
