import os

def print_colored(message, color):
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "reset": "\033[0m"
    }
    print(f"{colors.get(color, colors['reset'])}{message}{colors['reset']}")

def create_pre_commit_hook():
    print_colored("This script will set up a Git pre-commit hook to prevent commits if:", "yellow")
    print_colored("1. 'DEBUG = True' is found in any settings.py file", "yellow")
    print_colored("2. Any .env file is being committed", "yellow")
    confirmation = input("Are you sure you want to proceed? (yes/no): ").strip().lower()

    if confirmation not in ["yes", "y"]:
        print_colored("Operation canceled by user.", "red")
        return

    git_hooks_dir = os.path.join(".git", "hooks")
    pre_commit_path = os.path.join(git_hooks_dir, "pre-commit")

    if not os.path.exists(git_hooks_dir):
        print_colored("ERROR: No Git repository found in the current directory.", "red")
        return

    pre_commit_content = """#!/bin/bash

# Check for .env files in staged changes
if git diff --cached --name-only | grep -q "\.env$"; then
    echo "ERROR: Attempting to commit .env file. Please remove it from staging area."
    echo "You can use: git reset -- .env"
    exit 1
fi

# Find all settings.py files but exclude virtual environments and directories without the required project files
SETTINGS_FILE=$(find . -name "settings.py" ! -path "*/pyvenv.cfg" ! -path "*/env/*" ! -path "*/.venv/*" ! -path "*/.git/*")

# Now loop through the found directories and check for urls.py, wsgi.py, or asgi.py
for file in $SETTINGS_FILE; do
    DIR=$(dirname "$file")
    echo "Checking directory: $DIR"
    if [ -f "$DIR/urls.py" ] || [ -f "$DIR/wsgi.py" ] || [ -f "$DIR/asgi.py" ]; then
        echo "Valid settings found in: $file"
        SETTINGS_FILE=$file
        break
    fi
done

if [ -z "$SETTINGS_FILE" ]; then
    echo "ERROR: No valid settings.py file found in the expected project directories."
    exit 1
fi

if grep -q '^[^#]*DEBUG = True' "$SETTINGS_FILE"; then
    echo "ERROR: DEBUG is True in $SETTINGS_FILE. Please set it to False before committing."
    exit 1
fi
"""

    with open(pre_commit_path, "w") as hook_file:
        hook_file.write(pre_commit_content)

    os.chmod(pre_commit_path, 0o775)

    print_colored(f"Pre-commit hook created successfully at {pre_commit_path}.", "green")
    print_colored("The hook will:", "blue")
    print_colored("1. Block commits if 'DEBUG = True' is found in the valid settings.py file", "blue")
    print_colored("2. Prevent committing any .env files", "blue")

if __name__ == "__main__":
    create_pre_commit_hook()