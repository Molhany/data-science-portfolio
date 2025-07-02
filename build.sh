#!/usr/bin/env bash
# Build script for Render deployment

set -o errexit  # exit on error

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate

# Create default superuser for easy access
echo "🔧 Creating default superuser..."
python manage.py create_admin --username=adrian_molhany --email=adrian.molhany@gmail.com --password=Portfolio2024!

# Display login credentials
echo ""
echo "🔑 ADMIN LOGIN READY!"
echo "================================"
echo "Admin URL: https://data-science-portfolio-0738.onrender.com/admin/"
echo "Username: adrian_molhany"
echo "Password: Portfolio2024!"
echo "⚠️ Change password after first login!"
echo "================================"
