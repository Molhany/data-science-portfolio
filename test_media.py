#!/usr/bin/env python
"""
Test script to check media file configuration and serving.
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

from django.conf import settings
from django.core.files.storage import default_storage

def test_media_configuration():
    """Test media file configuration."""
    print("🧪 Testing Media File Configuration")
    print("=" * 50)
    
    # Check media settings
    print(f"📁 MEDIA_URL: {settings.MEDIA_URL}")
    print(f"📂 MEDIA_ROOT: {settings.MEDIA_ROOT}")
    
    # Check if media directory exists
    media_exists = os.path.exists(settings.MEDIA_ROOT)
    print(f"📁 Media directory exists: {'✅' if media_exists else '❌'}")
    
    # Check storage backend
    storage_class = default_storage.__class__.__name__
    print(f"💾 Storage backend: {storage_class}")
    
    # Check Cloudinary configuration
    if hasattr(settings, 'CLOUDINARY_STORAGE'):
        cloudinary_config = settings.CLOUDINARY_STORAGE
        cloud_name = cloudinary_config.get('CLOUD_NAME', '')
        has_cloudinary = bool(cloud_name)
        print(f"☁️ Cloudinary configured: {'✅' if has_cloudinary else '❌'}")
        if has_cloudinary:
            print(f"☁️ Cloud name: {cloud_name}")
    
    # Check if using Cloudinary
    using_cloudinary = 'cloudinary' in storage_class.lower()
    print(f"☁️ Using Cloudinary: {'✅' if using_cloudinary else '❌'}")
    
    print("\n" + "=" * 50)
    
    if using_cloudinary:
        print("✅ RECOMMENDED: Using cloud storage (Cloudinary)")
        print("   - Images will be permanently stored")
        print("   - Fast global delivery")
        print("   - No storage limitations")
    else:
        print("⚠️ WARNING: Using local storage")
        print("   - Images may disappear on Render restarts")
        print("   - Consider setting up Cloudinary for production")
    
    return using_cloudinary

def test_profile_images():
    """Test if profile images exist and are accessible."""
    print("\n🖼️ Testing Profile Images")
    print("=" * 30)
    
    try:
        from apps.portfolio.models import Profile
        
        profiles = Profile.objects.all()
        if not profiles.exists():
            print("❌ No profiles found")
            print("   Create a profile in admin panel first")
            return False
        
        profile = profiles.first()
        print(f"👤 Profile found: {profile.name or 'Unnamed'}")
        
        # Check profile images
        if hasattr(profile, 'profile_images') and profile.profile_images.exists():
            images = profile.profile_images.all()
            print(f"🖼️ Profile images: {images.count()}")
            
            for i, img in enumerate(images[:3], 1):  # Check first 3 images
                if img.image:
                    print(f"   {i}. {img.image.name} - {'✅' if img.image else '❌'}")
                    if img.image:
                        try:
                            # Try to get the URL
                            url = img.image.url
                            print(f"      URL: {url}")
                        except Exception as e:
                            print(f"      URL Error: {e}")
        else:
            print("❌ No profile images found")
            print("   Upload images in admin panel: Portfolio → Profiles")
        
        return True
        
    except Exception as e:
        print(f"❌ Error checking profile images: {e}")
        return False

def main():
    """Main test function."""
    print("🔍 Media Files Diagnostic Test")
    print("=" * 50)
    
    # Test configuration
    using_cloudinary = test_media_configuration()
    
    # Test profile images
    test_profile_images()
    
    print("\n" + "=" * 50)
    print("📋 RECOMMENDATIONS:")
    
    if not using_cloudinary:
        print("1. ☁️ Set up Cloudinary for permanent image storage:")
        print("   - Sign up at https://cloudinary.com")
        print("   - Add environment variables to Render:")
        print("     USE_CLOUDINARY=True")
        print("     CLOUDINARY_CLOUD_NAME=your-cloud-name")
        print("     CLOUDINARY_API_KEY=your-api-key")
        print("     CLOUDINARY_API_SECRET=your-api-secret")
    
    print("2. 🖼️ Upload profile images:")
    print("   - Go to admin panel")
    print("   - Portfolio → Profiles → Edit")
    print("   - Upload multiple images for auto-rotation")
    
    print("3. 🧪 Test after upload:")
    print("   - Check homepage for image display")
    print("   - Verify auto-rotation works")
    print("   - Test on mobile devices")
    
    print("\n🎯 Your portfolio will look professional with working images!")

if __name__ == "__main__":
    main()
