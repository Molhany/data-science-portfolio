#!/usr/bin/env python
"""
Quick fix for Render ALLOWED_HOSTS error.
This script provides the correct environment variables for your Render deployment.
"""

def main():
    print("🔧 Render ALLOWED_HOSTS Fix")
    print("=" * 50)
    
    print("\n❌ Error Explanation:")
    print("The DisallowedHost error occurs because Django's ALLOWED_HOSTS setting")
    print("doesn't include your actual Render URL: 'data-science-portfolio-0738.onrender.com'")
    
    print("\n✅ Solution:")
    print("Add the following environment variables to your Render Web Service:")
    
    print("\n📋 Environment Variables to Add/Update:")
    print("=" * 40)
    
    # Your actual Render URL
    render_url = "data-science-portfolio-0738.onrender.com"
    
    print(f"ALLOWED_HOSTS=localhost,127.0.0.1,{render_url}")
    print("RENDER=True")
    print("DEBUG=False")
    
    print("\n🔧 How to Fix in Render Dashboard:")
    print("1. Go to your Render dashboard")
    print("2. Click on your web service 'data-science-portfolio-0738'")
    print("3. Go to 'Environment' tab")
    print("4. Update or add the ALLOWED_HOSTS variable:")
    print(f"   ALLOWED_HOSTS=localhost,127.0.0.1,{render_url}")
    print("5. Add RENDER=True")
    print("6. Save changes")
    print("7. Render will automatically redeploy")
    
    print("\n⚡ Quick Fix (Alternative):")
    print("If you want to allow all .onrender.com domains:")
    print("ALLOWED_HOSTS=localhost,127.0.0.1,*.onrender.com")
    
    print("\n🚀 After the fix:")
    print(f"Your portfolio will be accessible at:")
    print(f"https://{render_url}")
    
    print("\n📝 Note:")
    print("The code has been updated to automatically handle Render URLs,")
    print("but you need to set the environment variables in Render dashboard.")

if __name__ == "__main__":
    main()
