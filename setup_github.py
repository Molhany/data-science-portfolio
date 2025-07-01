#!/usr/bin/env python
"""
GitHub setup script for Django portfolio project.
This script helps initialize Git repository and upload to GitHub for live access.
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(command, description, check=True):
    """Run a command and handle errors."""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully!")
            if result.stdout.strip():
                print(result.stdout)
        else:
            print(f"⚠️ {description} completed with warnings.")
            if result.stderr.strip():
                print(result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed!")
        print(f"Error: {e.stderr}")
        return False

def check_git_installed():
    """Check if Git is installed."""
    try:
        subprocess.run(['git', '--version'], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Git is not installed. Please install Git first.")
        print("Download from: https://git-scm.com/downloads")
        return False

def initialize_git():
    """Initialize Git repository."""
    if os.path.exists('.git'):
        print("✅ Git repository already initialized!")
        return True
    
    return run_command("git init", "Initializing Git repository")

def create_gitignore():
    """Ensure .gitignore exists."""
    if os.path.exists('.gitignore'):
        print("✅ .gitignore already exists!")
        return True
    
    print("⚠️ .gitignore not found. Creating basic .gitignore...")
    gitignore_content = """
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Django
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal
media/
staticfiles/

# Environment
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
"""
    
    with open('.gitignore', 'w') as f:
        f.write(gitignore_content.strip())
    
    print("✅ .gitignore created!")
    return True

def add_and_commit():
    """Add files and create initial commit."""
    commands = [
        ("git add .", "Adding files to Git"),
        ('git commit -m "Initial commit: Django Data Science Portfolio"', "Creating initial commit")
    ]
    
    for command, description in commands:
        if not run_command(command, description, check=False):
            return False
    
    return True

def get_github_info():
    """Get GitHub repository information from user."""
    print("\n📝 GitHub Repository Setup")
    print("Please provide your GitHub repository information:")
    
    username = input("GitHub username: ").strip()
    repo_name = input("Repository name (e.g., data-science-portfolio): ").strip()
    
    if not username or not repo_name:
        print("❌ Username and repository name are required!")
        return None, None
    
    return username, repo_name

def add_remote_origin(username, repo_name):
    """Add GitHub remote origin."""
    remote_url = f"https://github.com/{username}/{repo_name}.git"
    
    # Check if remote already exists
    result = subprocess.run(['git', 'remote', 'get-url', 'origin'], 
                          capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ Remote origin already exists: {result.stdout.strip()}")
        return True
    
    return run_command(f"git remote add origin {remote_url}", 
                      f"Adding remote origin: {remote_url}")

def push_to_github():
    """Push to GitHub."""
    commands = [
        ("git branch -M main", "Setting main branch"),
        ("git push -u origin main", "Pushing to GitHub")
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    
    return True

def main():
    """Main setup function."""
    print("🚀 GitHub Setup for Django Data Science Portfolio")
    print("=" * 50)
    
    # Change to project directory
    os.chdir(Path(__file__).parent)
    
    # Check prerequisites
    if not check_git_installed():
        sys.exit(1)
    
    # Setup steps
    steps = [
        ("Initializing Git repository", initialize_git),
        ("Creating .gitignore", create_gitignore),
        ("Adding files and committing", add_and_commit),
    ]
    
    for step_name, step_function in steps:
        if not step_function():
            print(f"\n❌ Setup failed at: {step_name}")
            sys.exit(1)
    
    # GitHub setup
    print("\n" + "=" * 50)
    print("🐙 GitHub Repository Setup")
    
    username, repo_name = get_github_info()
    if not username or not repo_name:
        sys.exit(1)
    
    if not add_remote_origin(username, repo_name):
        print("\n❌ Failed to add remote origin!")
        sys.exit(1)
    
    print(f"\n📋 Next Steps:")
    print(f"1. Create repository on GitHub: https://github.com/{username}/{repo_name}")
    print(f"2. Make sure the repository is PUBLIC and empty (no README, .gitignore, or license)")
    print(f"3. Run: git push -u origin main")
    print(f"4. Your portfolio code will be live at: https://github.com/{username}/{repo_name}")

    push_now = input("\nWould you like to push to GitHub now? (y/N): ").strip().lower()

    if push_now in ['y', 'yes']:
        if push_to_github():
            print(f"\n🎉 Successfully pushed to GitHub!")
            print(f"📍 Repository URL: https://github.com/{username}/{repo_name}")
            print(f"\n🌐 Your Portfolio is Now Live Online!")
            print(f"✅ Code Repository: https://github.com/{username}/{repo_name}")
            print(f"✅ Anyone can view your portfolio code")
            print(f"✅ Use GitHub Codespaces to run it live:")
            print(f"   1. Go to your repository")
            print(f"   2. Click 'Code' → 'Codespaces' → 'Create codespace'")
            print(f"   3. Run: python manage.py migrate && python manage.py runserver 0.0.0.0:8000")
            print(f"   4. Share the Codespace URL with others!")
        else:
            print(f"\n❌ Failed to push to GitHub. You can try manually:")
            print(f"git push -u origin main")
    else:
        print(f"\n📝 Manual push command:")
        print(f"git push -u origin main")

    print(f"\n🚀 What's Next:")
    print(f"📖 Your portfolio is now on GitHub and accessible online!")
    print(f"🔄 To update: make changes, then run 'git add . && git commit -m \"Update\" && git push'")
    print(f"🌐 For permanent hosting, consider: Railway, Render, or PythonAnywhere (all have free tiers)")

if __name__ == "__main__":
    main()
