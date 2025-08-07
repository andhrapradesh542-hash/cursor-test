# 🚀 Windows 10 Quick Start Guide

## ⚡ Super Quick Setup (5 minutes)

### Step 1: Download & Extract
1. Download all the scraper files to a folder (e.g., `C:\bazaraki-scraper\`)
2. Open that folder

### Step 2: One-Click Setup
**Double-click: `start_windows.bat`**

That's it! The script will:
- ✅ Find your Python installation
- ✅ Install all required packages  
- ✅ Set up Chrome WebDriver
- ✅ Create convenient shortcuts

### Step 3: Run the Scraper
**Double-click: `start_bazaraki.bat`**

Choose option 3 for a quick scan!

---

## 🛠️ If You Don't Have Python

### Install Python (2 minutes):
1. Go to https://www.python.org/downloads/
2. Download the latest Python 3
3. **IMPORTANT**: ✅ Check "Add Python to PATH" during installation
4. Click "Install Now"

Then run `start_windows.bat`

---

## 🌐 If You Don't Have Chrome

### Install Chrome (1 minute):
1. Go to https://www.google.com/chrome/
2. Download and install Chrome
3. The scraper will automatically use it

---

## 🎯 What You'll Get

After setup, you'll have these files:
- **`start_bazaraki.bat`** ← Double-click this to launch
- **`quick_scan.bat`** ← Double-click for instant scan
- **`test_system.bat`** ← Double-click to test setup

## 📊 Example Output

```
🎉 Found 8 great deals!

🏆 TOP DEALS:
1. iPhone 14 Pro Max 256GB
   💰 Price: €750 (Market: €950)
   💚 Save: €200 (21% OFF)
   📍 Nicosia

2. MacBook Air M2 13"
   💰 Price: €950 (Market: €1200)  
   💚 Save: €250 (20% OFF)
   📍 Limassol
```

---

## 🆘 Having Issues?

### "Python not found"
- Reinstall Python with "Add to PATH" checked
- Or try: `py -3 windows_setup.py`

### "Chrome not found"  
- Install Chrome from google.com/chrome
- Restart computer after installation

### Permission errors
- Right-click Command Prompt → "Run as administrator"
- Run `start_windows.bat` as admin

### Package install fails
```cmd
python -m pip install --user requests beautifulsoup4 pandas selenium webdriver-manager lxml openpyxl
```

### Still stuck?
Read the detailed guide: `WINDOWS_TROUBLESHOOTING.md`

---

## 🎉 Ready to Find Deals!

**The scraper will help you find:**
- 📱 iPhone deals (15-25% off market price)
- 💻 MacBook deals (20-30% savings)  
- 🎮 Electronics below market value
- 📊 Beautiful reports with all details

**Just double-click `start_bazaraki.bat` and start saving money!** 💰