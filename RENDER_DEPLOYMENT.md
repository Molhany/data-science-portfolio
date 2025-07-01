# 🚀 Deploy to Render - Free Permanent Hosting

Deploy your Django Data Science Portfolio to Render's free tier for permanent online hosting.

## 🌟 Why Render?

- ✅ **Free Tier Available** - Perfect for portfolios
- ✅ **Automatic Deployments** - Updates when you push to GitHub
- ✅ **Free PostgreSQL Database** - 90 days free, then $7/month
- ✅ **Custom Domains** - Use your own domain name
- ✅ **SSL Certificates** - Automatic HTTPS
- ✅ **Professional URLs** - yourname.onrender.com

## 📋 Prerequisites

- ✅ GitHub repository with your portfolio (already done!)
- ✅ Render account (free at https://render.com)

## 🚀 Step-by-Step Deployment

### Step 1: Push Latest Changes to GitHub

Make sure your latest changes are on GitHub:

```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### Step 2: Create Render Account

1. Go to https://render.com
2. Click **"Get Started for Free"**
3. Sign up with GitHub (recommended)
4. Connect your GitHub account

### Step 3: Create PostgreSQL Database

1. In Render dashboard, click **"New +"**
2. Select **"PostgreSQL"**
3. Configure database:
   - **Name**: `adrian-portfolio-db`
   - **Database**: `adrian_portfolio`
   - **User**: `adrian_portfolio_user`
   - **Region**: Choose closest to your location
   - **Plan**: **Free** (90 days free)
4. Click **"Create Database"**
5. **Save the Database URL** - you'll need it for the web service

### Step 4: Create Web Service

1. In Render dashboard, click **"New +"**
2. Select **"Web Service"**
3. Connect your GitHub repository:
   - Select your portfolio repository
   - Click **"Connect"**

### Step 5: Configure Web Service

Fill in the configuration:

#### **Basic Settings:**
- **Name**: `adrian-molhany-portfolio` (this will be your URL)
- **Region**: Same as your database
- **Branch**: `main`
- **Root Directory**: Leave empty
- **Runtime**: `Python 3`

#### **Build & Deploy:**
- **Build Command**: `./build.sh`
- **Start Command**: `gunicorn datasci_portfolio.wsgi:application`

#### **Advanced Settings:**
Click **"Advanced"** and add these environment variables:

| Key | Value |
|-----|-------|
| `SECRET_KEY` | Generate a secure key (use Django's get_random_secret_key()) |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `adrian-molhany-portfolio.onrender.com,localhost,127.0.0.1` |
| `DATABASE_URL` | Paste the database URL from Step 3 |

### Step 6: Deploy

1. Click **"Create Web Service"**
2. Render will automatically:
   - Clone your repository
   - Install dependencies
   - Run migrations
   - Start your application
3. Wait for deployment (5-10 minutes)

### Step 7: Create Superuser

After successful deployment:

1. Go to your service dashboard
2. Click **"Shell"** tab
3. Run:
   ```bash
   python manage.py createsuperuser
   ```
4. Follow prompts to create admin account

## 🌐 Your Live Portfolio

Your portfolio will be live at:
```
https://adrian-molhany-portfolio.onrender.com
```

Admin panel:
```
https://adrian-molhany-portfolio.onrender.com/admin/
```

## 🔧 Post-Deployment Setup

### 1. Upload Content

1. Go to admin panel
2. Login with superuser account
3. Upload:
   - Profile information
   - Profile images
   - Project details
   - Skills and achievements
   - Social media links

### 2. Test Everything

- ✅ Homepage loads correctly
- ✅ All pages work
- ✅ Images display properly
- ✅ Contact forms work
- ✅ Live chat functions
- ✅ Social links work

### 3. SEO Optimization

Update your profile with:
- **Full Name**: Adrian Molhany / Adrian Mahanyamba
- **Professional Title**: Data Science & Informatics Student
- **Bio**: Include keywords people might search for
- **Skills**: List all your technical skills
- **Projects**: Detailed descriptions with keywords

## 🔄 Automatic Updates

Every time you push to GitHub:
1. Render automatically detects changes
2. Rebuilds your application
3. Deploys the new version
4. Zero downtime deployment

To update:
```bash
git add .
git commit -m "Update portfolio content"
git push origin main
```

## 🌍 Custom Domain (Optional)

To use your own domain:

1. Purchase domain from any registrar
2. In Render dashboard:
   - Go to your service
   - Click "Settings"
   - Add custom domain
3. Update DNS records as instructed
4. SSL certificate automatically provisioned

## 💰 Costs

- **Web Service**: Free tier (750 hours/month)
- **PostgreSQL**: Free for 90 days, then $7/month
- **Custom Domain**: Free on Render (domain cost separate)

## 🆘 Troubleshooting

### Build Fails
- Check build logs in Render dashboard
- Ensure all dependencies in requirements.txt
- Verify build.sh has correct permissions

### Database Connection Issues
- Verify DATABASE_URL is correct
- Check database is running
- Ensure database and web service in same region

### Static Files Not Loading
- Check STATIC_ROOT setting
- Verify WhiteNoise is installed
- Run collectstatic in build script

### Application Won't Start
- Check start command is correct
- Verify WSGI application path
- Check environment variables

## 📞 Support

- **Render Docs**: https://render.com/docs
- **Community**: https://community.render.com
- **Status**: https://status.render.com

## 🎉 Success!

Your Django Data Science Portfolio is now:
- ✅ **Live and accessible worldwide**
- ✅ **Professionally hosted**
- ✅ **Automatically updated**
- ✅ **SEO optimized**
- ✅ **Searchable online**

People searching for "Adrian Molhany" or "Adrian Mahanyamba" will find your professional portfolio!

---

**Your portfolio URL**: `https://adrian-molhany-portfolio.onrender.com`
