# 🚀 Quick Start - Upload to GitHub

Get your Django Data Science Portfolio live on GitHub in 5 minutes!

## ⚡ Super Quick Setup

### 1. Run the Setup Script
```bash
python setup_github.py
```

### 2. Create GitHub Repository
- Go to https://github.com
- Click "New Repository"
- Name: `data-science-portfolio`
- Make it **PUBLIC**
- Don't initialize with README

### 3. Push to GitHub
```bash
git push -u origin main
```

## 🎉 Done! Your Portfolio is Live

**Your portfolio is now online at:**
```
https://github.com/yourusername/data-science-portfolio
```

## 🌐 Run Your Portfolio Live

### Option 1: GitHub Codespaces (Free)
1. Go to your GitHub repository
2. Click **"Code"** → **"Codespaces"** → **"Create codespace"**
3. In terminal:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver 0.0.0.0:8000
   ```
4. Share the live URL!

### Option 2: Others Can Clone & Run
```bash
git clone https://github.com/yourusername/data-science-portfolio.git
cd data-science-portfolio
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## 🔄 Update Your Portfolio

Make changes, then:
```bash
git add .
git commit -m "Update portfolio"
git push origin main
```

## 📞 Need Help?

- Check [GITHUB_SETUP.md](GITHUB_SETUP.md) for detailed instructions
- Check [DEPLOYMENT.md](DEPLOYMENT.md) for comprehensive guide

---

**Your portfolio is now live and accessible to the world! 🌍**
