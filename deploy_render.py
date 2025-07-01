#!/usr/bin/env python
"""
Render deployment preparation script.
This script helps prepare your Django portfolio for Render deployment.
"""

import os
import sys
import subprocess
import secrets
from pathlib import Path

def generate_secret_key():
    """Generate a secure Django secret key."""
    return secrets.token_urlsafe(50)

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        if result.stdout.strip():
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed!")
        print(f"Error: {e.stderr}")
        return False

def check_git_status():
    """Check if there are uncommitted changes."""
    try:
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True, check=True)
        if result.stdout.strip():
            print("⚠️ You have uncommitted changes:")
            print(result.stdout)
            return False
        return True
    except subprocess.CalledProcessError:
        print("❌ Git repository not found or not initialized")
        return False

def commit_and_push():
    """Commit changes and push to GitHub."""
    commands = [
        ("git add .", "Adding files to Git"),
        ('git commit -m "Prepare for Render deployment"', "Committing changes"),
        ("git push origin main", "Pushing to GitHub")
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    
    return True

def main():
    """Main deployment preparation function."""
    print("🚀 Render Deployment Preparation")
    print("=" * 50)
    
    # Change to project directory
    os.chdir(Path(__file__).parent)
    
    # Generate secret key
    secret_key = generate_secret_key()
    
    print(f"\n🔑 Generated Secret Key:")
    print(f"SECRET_KEY={secret_key}")
    
    print(f"\n📋 Environment Variables for Render:")
    print(f"SECRET_KEY={secret_key}")
    print(f"DEBUG=False")
    print(f"ALLOWED_HOSTS=adrian-molhany-portfolio.onrender.com,localhost,127.0.0.1")
    
    print(f"\n📝 Next Steps:")
    print(f"1. Copy the environment variables above")
    print(f"2. Go to https://render.com and create account")
    print(f"3. Create PostgreSQL database first")
    print(f"4. Create Web Service and paste environment variables")
    print(f"5. Add DATABASE_URL from your PostgreSQL database")
    
    # Check git status
    if not check_git_status():
        commit_now = input("\nWould you like to commit and push changes now? (y/N): ").strip().lower()
        if commit_now in ['y', 'yes']:
            if commit_and_push():
                print("\n✅ Changes pushed to GitHub!")
            else:
                print("\n❌ Failed to push changes. Please commit manually.")
                return False
        else:
            print("\n⚠️ Please commit and push your changes before deploying to Render.")
            return False
    
    print(f"\n🌐 Your portfolio will be live at:")
    print(f"https://adrian-molhany-portfolio.onrender.com")
    
    print(f"\n📖 For detailed instructions, see:")
    print(f"RENDER_DEPLOYMENT.md")
    
    print(f"\n🎉 Ready for Render deployment!")

if __name__ == "__main__":
    main()
