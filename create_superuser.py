#!/usr/bin/env python
"""
Script to create a superuser programmatically.
Use this if you can't access Render shell.
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'datasci_portfolio.settings')

# Setup Django
django.setup()

from django.contrib.auth import get_user_model

def create_superuser():
    """Create a superuser if one doesn't exist."""
    User = get_user_model()
    
    # Check if any superuser exists
    if User.objects.filter(is_superuser=True).exists():
        print("✅ Superuser already exists!")
        superuser = User.objects.filter(is_superuser=True).first()
        print(f"Username: {superuser.username}")
        print(f"Email: {superuser.email}")
        return
    
    # Create superuser
    print("🔧 Creating superuser...")
    
    # Default values (you can change these)
    username = "adrian_molhany"
    email = "adrian.molhany@example.com"  # Change this to your real email
    password = "AdminPass123!"  # Change this to a secure password
    
    try:
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        
        print("🎉 Superuser created successfully!")
        print(f"Username: {username}")
        print(f"Email: {email}")
        print(f"Password: {password}")
        print("\n⚠️ IMPORTANT: Change the password after first login!")
        print(f"Login at: https://data-science-portfolio-0738.onrender.com/admin/")
        
    except Exception as e:
        print(f"❌ Error creating superuser: {e}")

if __name__ == "__main__":
    create_superuser()
