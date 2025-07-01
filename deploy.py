#!/usr/bin/env python
"""
Deployment script for Django portfolio project.
This script helps prepare the project for deployment.
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed!")
        print(f"Error: {e.stderr}")
        return False

def collect_static():
    """Collect static files."""
    return run_command("python manage.py collectstatic --noinput", "Collecting static files")

def run_migrations():
    """Run database migrations."""
    return run_command("python manage.py migrate", "Running database migrations")

def create_superuser():
    """Create superuser if it doesn't exist."""
    print("\n🔄 Creating superuser...")
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        if not User.objects.filter(is_superuser=True).exists():
            print("No superuser found. Please create one:")
            subprocess.run([sys.executable, "manage.py", "createsuperuser"], check=True)
        else:
            print("✅ Superuser already exists!")
        return True
    except Exception as e:
        print(f"❌ Error creating superuser: {e}")
        return False

def check_requirements():
    """Check if all requirements are installed."""
    return run_command("pip install -r requirements.txt", "Installing requirements")

def main():
    """Main deployment function."""
    print("🚀 Starting deployment preparation...")
    
    # Change to project directory
    os.chdir(Path(__file__).parent)
    
    steps = [
        ("Installing requirements", check_requirements),
        ("Running migrations", run_migrations),
        ("Collecting static files", collect_static),
        ("Creating superuser", create_superuser),
    ]
    
    failed_steps = []
    
    for step_name, step_function in steps:
        if not step_function():
            failed_steps.append(step_name)
    
    if failed_steps:
        print(f"\n❌ Deployment preparation failed! Failed steps: {', '.join(failed_steps)}")
        sys.exit(1)
    else:
        print("\n🎉 Deployment preparation completed successfully!")
        print("\n📋 Next steps:")
        print("1. Set up your environment variables (.env file)")
        print("2. Configure your database")
        print("3. Deploy to your hosting platform")
        print("4. Set up your domain and SSL certificate")

if __name__ == "__main__":
    main()
