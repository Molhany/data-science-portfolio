# 🔑 Default Admin Login Credentials

Your Django portfolio automatically creates a default superuser for easy admin access.

## 🌐 Admin Panel URL

```
https://data-science-portfolio-0738.onrender.com/admin/
```

## 👤 Default Login Credentials

**Username:** `adrian_molhany`
**Password:** `Portfolio2024!`
**Email:** `adrian.molhany@gmail.com`

## ⚠️ IMPORTANT SECURITY NOTICE

**CHANGE THE PASSWORD IMMEDIATELY AFTER FIRST LOGIN!**

### How to Change Password:

1. **Login to admin panel** with default credentials
2. **Click your username** (top right corner)
3. **Click "Change password"**
4. **Enter new secure password**
5. **Save changes**

## 🔧 How It Works

The default superuser is automatically created:

1. **During deployment** - Build script runs `create_admin` command
2. **After migrations** - Django signal creates superuser if none exists
3. **Always available** - No need for shell access or manual commands

## 📝 What to Do After Login

### 1. Change Password (FIRST!)
- Use a strong, unique password
- Don't use the default password in production

### 2. Update Profile Information
- Go to **Portfolio → Profiles**
- Add your real information:
  - Name: Adrian Molhany / Adrian Mahanyamba
  - Bio, skills, contact info
  - Social media links

### 3. Upload Content
- **Profile images** (multiple for auto-rotation)
- **Projects** with descriptions and images
- **Skills and achievements**
- **Contact information**

### 4. Test Everything
- Check all pages load correctly
- Test contact forms
- Verify live chat works
- Ensure social links function

## 🛡️ Security Features

- **Automatic creation** only if no superuser exists
- **Strong default password** with mixed characters
- **Real email format** for notifications
- **First/Last name** set for professional appearance

## 🔄 If You Need to Reset

If you forget your password or need to recreate the superuser:

1. **Redeploy on Render** (triggers automatic creation)
2. **Use management command** via Render shell:
   ```bash
   python manage.py create_admin --force
   ```

## 📱 Mobile Admin Access

The admin panel works perfectly on mobile devices:
- Responsive design
- Touch-friendly interface
- Full functionality on phones/tablets

## 🎯 Ready to Go!

Your portfolio is now ready with:
- ✅ **Automatic superuser creation**
- ✅ **No shell access needed**
- ✅ **Immediate admin access**
- ✅ **Professional default settings**
- ✅ **Security best practices**

**Login now and start building your professional online presence!** 🚀

---

**Admin URL**: https://data-science-portfolio-0738.onrender.com/admin/
**Username**: adrian_molhany
**Password**: Portfolio2024!
