#!/usr/bin/env python
"""
Test script to check if WSGI application can be loaded properly.
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

def test_django_setup():
    """Test if Django can be set up properly."""
    try:
        django.setup()
        print("✅ Django setup successful!")
        return True
    except Exception as e:
        print(f"❌ Django setup failed: {e}")
        return False

def test_settings_import():
    """Test if settings can be imported."""
    try:
        import datasci_portfolio.settings
        print("✅ Settings import successful!")
        return True
    except Exception as e:
        print(f"❌ Settings import failed: {e}")
        return False

def test_wsgi_import():
    """Test if WSGI application can be imported."""
    try:
        from datasci_portfolio.wsgi import application
        print("✅ WSGI application import successful!")
        return True
    except Exception as e:
        print(f"❌ WSGI application import failed: {e}")
        return False

def test_urls_import():
    """Test if URLs can be imported."""
    try:
        import datasci_portfolio.urls
        print("✅ URLs import successful!")
        return True
    except Exception as e:
        print(f"❌ URLs import failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🔍 Testing Django Configuration...")
    print("=" * 50)
    
    tests = [
        ("Settings Import", test_settings_import),
        ("Django Setup", test_django_setup),
        ("URLs Import", test_urls_import),
        ("WSGI Application", test_wsgi_import),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 Testing {test_name}...")
        if test_func():
            passed += 1
        else:
            print(f"   ⚠️ {test_name} failed!")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your Django application is ready for deployment.")
        return True
    else:
        print("❌ Some tests failed. Please fix the issues before deploying.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
