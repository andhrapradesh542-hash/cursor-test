# 🪟 Windows 10 Troubleshooting Guide

## 🚀 Quick Fix for Windows 10

### Step 1: Use the Windows Setup Script
```cmd
python windows_setup.py
```

This will automatically fix most Windows-specific issues!

## 🔧 Common Windows Errors & Solutions

### Error 1: "python is not recognized as internal or external command"

**Problem**: Python not in PATH or not installed properly

**Solutions**:
1. **Reinstall Python with PATH option**:
   - Download from https://www.python.org/downloads/
   - ✅ **CHECK "Add Python to PATH"** during installation
   - Choose "Install for all users"

2. **Add Python to PATH manually**:
   ```cmd
   # Find your Python installation (usually one of these):
   C:\Python39\
   C:\Users\YourName\AppData\Local\Programs\Python\Python39\
   C:\Program Files\Python39\
   
   # Add to System PATH:
   # Windows key + R → sysdm.cpl → Advanced → Environment Variables
   # Edit PATH and add your Python directory
   ```

3. **Use Python Launcher**:
   ```cmd
   py -3 windows_setup.py
   py -3 run_scraper.py
   ```

### Error 2: "pip is not recognized" or pip install fails

**Solutions**:
```cmd
# Method 1: Use python -m pip
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# Method 2: Use py launcher
py -3 -m pip install --upgrade pip
py -3 -m pip install -r requirements.txt

# Method 3: Install to user directory
python -m pip install --user -r requirements.txt
```

### Error 3: ChromeDriver or Chrome issues

**Problem**: Chrome not found or ChromeDriver incompatible

**Solutions**:
1. **Install Chrome**:
   - Download from https://www.google.com/chrome/
   - Install normally

2. **Use WebDriver Manager** (automatic):
   ```cmd
   python -m pip install webdriver-manager
   ```

3. **Manual ChromeDriver setup**:
   - Check Chrome version: chrome://version/
   - Download matching ChromeDriver from https://chromedriver.chromium.org/
   - Extract to a folder (e.g., C:\chromedriver\)
   - Add folder to PATH

4. **Alternative: Use Edge browser**:
   ```python
   # Modify bazaraki_scraper.py to use Edge instead
   from selenium.webdriver import Edge
   driver = Edge()
   ```

### Error 4: Permission Denied / Access Denied

**Solutions**:
1. **Run as Administrator**:
   - Right-click Command Prompt → "Run as administrator"
   - Run the setup script again

2. **Install to user directory**:
   ```cmd
   python -m pip install --user -r requirements.txt
   ```

3. **Check antivirus software**:
   - Temporarily disable real-time protection
   - Add project folder to antivirus exclusions

### Error 5: SSL Certificate errors

**Problem**: Corporate firewalls or outdated certificates

**Solutions**:
```cmd
# Upgrade certificates
python -m pip install --upgrade certifi

# Use trusted hosts
python -m pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt

# Corporate networks
python -m pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --proxy http://your-proxy:port -r requirements.txt
```

### Error 6: ModuleNotFoundError

**Problem**: Package not installed or wrong Python environment

**Solutions**:
```cmd
# Check which Python you're using
python --version
where python

# Install missing packages
python -m pip install requests beautifulsoup4 pandas selenium lxml

# Check installed packages
python -m pip list

# Verify installation
python -c "import requests; import selenium; import pandas; print('All packages OK')"
```

### Error 7: Encoding errors (UnicodeDecodeError)

**Solutions**:
```cmd
# Set UTF-8 encoding
set PYTHONIOENCODING=utf-8

# Or add to script
import os
os.environ['PYTHONIOENCODING'] = 'utf-8'
```

### Error 8: Firewall/Network issues

**Solutions**:
1. **Windows Firewall**:
   - Allow Python through Windows Firewall
   - Windows Security → Firewall → Allow app through firewall

2. **Corporate networks**:
   - Configure proxy settings
   - Ask IT for Python/pip proxy configuration

3. **Test network connectivity**:
   ```cmd
   ping google.com
   python -c "import requests; print(requests.get('https://google.com').status_code)"
   ```

## 🛠️ Windows-Specific Setup Commands

### Complete Windows Setup (run these in order):

```cmd
# 1. Check Python
python --version
py -3 --version

# 2. Upgrade pip
python -m pip install --upgrade pip

# 3. Install packages
python -m pip install requests beautifulsoup4 pandas selenium webdriver-manager lxml openpyxl

# 4. Run Windows setup
python windows_setup.py

# 5. Test system
python test_scraper.py

# 6. Launch scraper
python run_scraper.py
```

### Alternative: One-line setup
```cmd
python -m pip install requests beautifulsoup4 pandas selenium webdriver-manager lxml openpyxl && python windows_setup.py
```

## 🚀 Easy Windows Launch Options

After setup, you can use these convenient methods:

### Method 1: Batch Files (Double-click)
- **start_bazaraki.bat** - Main launcher
- **quick_scan.bat** - Quick scan
- **test_system.bat** - Test system

### Method 2: Command Line
```cmd
# Main launcher
python run_scraper.py

# Direct scraper
python bazaraki_scraper.py

# Quick test
python test_scraper.py
```

### Method 3: PowerShell
```powershell
# Set execution policy (one time)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Run scraper
python run_scraper.py
```

## 📁 Windows File Locations

### Default locations:
- **Project files**: Current directory
- **Python**: `C:\Users\YourName\AppData\Local\Programs\Python\`
- **ChromeDriver**: `C:\Users\YourName\.wdm\` (auto-downloaded)
- **Output files**: `.\deals_reports\`

### Log files:
- **bazaraki_scraper.log** - Scraper execution log
- **chromedriver.log** - WebDriver log

## 🎯 Windows Performance Tips

### 1. Disable Windows Defender (temporarily)
```
Windows Security → Virus & threat protection → Real-time protection → OFF
```

### 2. Close unnecessary programs
- Close browser tabs
- Close resource-heavy applications
- Check Task Manager for CPU/Memory usage

### 3. Use SSD drive
- Run from SSD if available
- Faster file operations

### 4. Increase virtual memory
- Control Panel → System → Advanced → Performance Settings → Advanced → Virtual Memory

## 🆘 Still Having Issues?

### 1. Clean installation
```cmd
# Uninstall all packages
python -m pip uninstall requests beautifulsoup4 pandas selenium webdriver-manager lxml openpyxl -y

# Clear pip cache
python -m pip cache purge

# Reinstall
python windows_setup.py
```

### 2. Use virtual environment
```cmd
# Create virtual environment
python -m venv bazaraki_env

# Activate it
bazaraki_env\Scripts\activate

# Install packages
python -m pip install -r requirements.txt

# Run scraper
python run_scraper.py
```

### 3. Alternative Python distributions
- **Anaconda**: https://www.anaconda.com/products/distribution
- **Miniconda**: https://docs.conda.io/en/latest/miniconda.html

### 4. Get specific error details
```cmd
# Run with verbose output
python -v bazaraki_scraper.py

# Check Python path
python -c "import sys; print('\n'.join(sys.path))"

# Check installed packages
python -m pip show selenium requests pandas
```

### 5. Windows-specific debugging
```cmd
# Check Windows version
systeminfo | findstr /B /C:"OS Name" /C:"OS Version"

# Check Python installation
py -0
py -3 -c "import sys; print(sys.executable)"

# Check PATH
echo %PATH%
```

## 📞 Last Resort Solutions

If nothing works:

1. **Use WSL (Windows Subsystem for Linux)**:
   ```cmd
   wsl --install
   # Then run the scraper in Ubuntu
   ```

2. **Use Docker**:
   ```cmd
   docker run -it python:3.9 bash
   # Install and run inside container
   ```

3. **Use online Python environment**:
   - Replit.com
   - Google Colab
   - CodePen

---

**💡 Tip**: Run `python windows_setup.py` first - it fixes 90% of Windows issues automatically!