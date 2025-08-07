#!/usr/bin/env python3
"""
Windows 10 Setup Script for Bazaraki Electronics Deal Finder
Handles Windows-specific issues and dependencies
"""

import subprocess
import sys
import os
import platform
import urllib.request
import zipfile
from pathlib import Path

def check_windows_version():
    """Check Windows version"""
    print("🪟 Checking Windows version...")
    version = platform.platform()
    print(f"   System: {version}")
    
    if "Windows-10" not in version and "Windows-11" not in version:
        print("⚠️  Warning: This script is optimized for Windows 10/11")
    else:
        print("✅ Windows version: Compatible")
    return True

def check_python_version():
    """Check Python version"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    print(f"   Python: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Python 3.7+ required. Please upgrade Python.")
        print("   Download from: https://www.python.org/downloads/")
        return False
    else:
        print("✅ Python version: Compatible")
    return True

def install_pip_packages():
    """Install Python packages with Windows-specific handling"""
    print("📦 Installing Python packages...")
    
    packages = [
        "requests==2.31.0",
        "beautifulsoup4==4.12.2", 
        "pandas==2.0.3",
        "selenium==4.15.2",
        "webdriver-manager==4.0.1",
        "lxml==4.9.3",
        "openpyxl==3.1.2"
    ]
    
    for package in packages:
        print(f"   Installing {package}...")
        try:
            subprocess.run([
                sys.executable, "-m", "pip", "install", 
                package, "--user", "--no-warn-script-location"
            ], check=True, capture_output=True)
            print(f"   ✅ {package}")
        except subprocess.CalledProcessError as e:
            print(f"   ❌ Failed to install {package}")
            print(f"   Error: {e}")
            return False
    
    print("✅ All packages installed successfully!")
    return True

def download_chromedriver():
    """Download ChromeDriver for Windows"""
    print("🌐 Setting up ChromeDriver...")
    
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager
        
        print("   Using webdriver-manager to get ChromeDriver...")
        driver_path = ChromeDriverManager().install()
        print(f"   ✅ ChromeDriver installed at: {driver_path}")
        return True
        
    except Exception as e:
        print(f"   ❌ Error setting up ChromeDriver: {e}")
        print("   Trying manual download...")
        
        # Manual ChromeDriver download
        try:
            driver_dir = Path.home() / "chromedriver"
            driver_dir.mkdir(exist_ok=True)
            
            # Download latest ChromeDriver for Windows
            url = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
            response = urllib.request.urlopen(url)
            version = response.read().decode('utf-8').strip()
            
            driver_url = f"https://chromedriver.storage.googleapis.com/{version}/chromedriver_win32.zip"
            zip_path = driver_dir / "chromedriver.zip"
            
            print(f"   Downloading ChromeDriver {version}...")
            urllib.request.urlretrieve(driver_url, zip_path)
            
            # Extract
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(driver_dir)
            
            os.remove(zip_path)
            
            # Add to PATH
            driver_exe = driver_dir / "chromedriver.exe"
            if driver_exe.exists():
                print(f"   ✅ ChromeDriver downloaded to: {driver_exe}")
                
                # Add to system PATH
                current_path = os.environ.get('PATH', '')
                if str(driver_dir) not in current_path:
                    os.environ['PATH'] = f"{driver_dir};{current_path}"
                
                return True
            else:
                print("   ❌ ChromeDriver extraction failed")
                return False
                
        except Exception as e2:
            print(f"   ❌ Manual download failed: {e2}")
            return False

def check_chrome_browser():
    """Check if Chrome browser is installed"""
    print("🌐 Checking Chrome browser...")
    
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
        os.path.expandvars(r"%PROGRAMFILES%\Google\Chrome\Application\chrome.exe"),
        os.path.expandvars(r"%PROGRAMFILES(X86)%\Google\Chrome\Application\chrome.exe")
    ]
    
    for path in chrome_paths:
        if os.path.exists(path):
            print(f"   ✅ Chrome found at: {path}")
            return True
    
    print("   ❌ Chrome not found!")
    print("   Please install Chrome from: https://www.google.com/chrome/")
    print("   Or install Edge WebDriver as alternative")
    return False

def create_windows_batch_files():
    """Create convenient batch files for Windows"""
    print("📝 Creating Windows batch files...")
    
    # Main launcher batch file
    launcher_content = """@echo off
echo Starting Bazaraki Deal Finder...
python "%~dp0run_scraper.py"
pause
"""
    
    with open("start_bazaraki.bat", "w") as f:
        f.write(launcher_content)
    print("   ✅ Created start_bazaraki.bat")
    
    # Quick scan batch file
    quick_scan_content = """@echo off
echo Running Quick Scan...
python "%~dp0bazaraki_scraper.py" --quick
pause
"""
    
    with open("quick_scan.bat", "w") as f:
        f.write(quick_scan_content)
    print("   ✅ Created quick_scan.bat")
    
    # Test batch file
    test_content = """@echo off
echo Running System Tests...
python "%~dp0test_scraper.py"
pause
"""
    
    with open("test_system.bat", "w") as f:
        f.write(test_content)
    print("   ✅ Created test_system.bat")

def fix_common_windows_issues():
    """Fix common Windows-specific issues"""
    print("🔧 Fixing common Windows issues...")
    
    # Set UTF-8 encoding
    try:
        os.environ['PYTHONIOENCODING'] = 'utf-8'
        print("   ✅ Set UTF-8 encoding")
    except:
        pass
    
    # Disable Windows Defender real-time scanning warning
    print("   💡 Tip: If Windows Defender blocks the scraper:")
    print("      1. Open Windows Security")
    print("      2. Go to Virus & threat protection")
    print("      3. Add folder exclusion for this directory")
    
    # Create output directory
    os.makedirs("deals_reports", exist_ok=True)
    print("   ✅ Created deals_reports directory")
    
    # Fix PATH issues
    current_dir = os.getcwd()
    python_scripts = os.path.join(os.path.dirname(sys.executable), "Scripts")
    
    if python_scripts not in os.environ.get('PATH', ''):
        print(f"   💡 Consider adding to PATH: {python_scripts}")

def test_installation():
    """Test the installation"""
    print("🧪 Testing installation...")
    
    # Test imports
    test_modules = [
        ('requests', 'Requests library'),
        ('selenium', 'Selenium WebDriver'),
        ('pandas', 'Pandas data analysis'),
        ('bs4', 'BeautifulSoup HTML parser')
    ]
    
    failed_imports = []
    for module, name in test_modules:
        try:
            __import__(module)
            print(f"   ✅ {name}")
        except ImportError:
            print(f"   ❌ {name}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"   ❌ Failed imports: {failed_imports}")
        return False
    
    # Test Chrome WebDriver
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        driver = webdriver.Chrome(options=options)
        driver.get("https://www.google.com")
        
        if "Google" in driver.title:
            print("   ✅ Chrome WebDriver working")
            driver.quit()
            return True
        else:
            print("   ❌ Chrome WebDriver test failed")
            driver.quit()
            return False
            
    except Exception as e:
        print(f"   ❌ Chrome WebDriver error: {e}")
        return False

def main():
    """Main setup function for Windows"""
    print("🪟 Bazaraki Deal Finder - Windows 10 Setup")
    print("=" * 50)
    
    # Run checks and setup
    steps = [
        ("Windows Version", check_windows_version),
        ("Python Version", check_python_version),
        ("Chrome Browser", check_chrome_browser),
        ("Python Packages", install_pip_packages),
        ("ChromeDriver", download_chromedriver),
        ("Windows Batch Files", create_windows_batch_files),
        ("Common Issues", fix_common_windows_issues),
        ("Installation Test", test_installation)
    ]
    
    results = []
    for step_name, step_func in steps:
        print(f"\n{'='*20} {step_name} {'='*20}")
        try:
            result = step_func()
            results.append((step_name, result))
        except Exception as e:
            print(f"❌ Error in {step_name}: {e}")
            results.append((step_name, False))
    
    # Summary
    print(f"\n{'='*50}")
    print("📊 SETUP RESULTS")
    print("=" * 50)
    
    passed = 0
    for step_name, result in results:
        status = "✅ SUCCESS" if result else "❌ FAILED"
        print(f"{step_name:.<25} {status}")
        if result:
            passed += 1
    
    print(f"\nCompleted: {passed}/{len(results)} steps")
    
    if passed >= len(results) - 1:  # Allow 1 failure
        print("\n🎉 SETUP SUCCESSFUL!")
        print("\n🚀 Next steps:")
        print("1. Double-click 'start_bazaraki.bat' to launch")
        print("2. Or run: python run_scraper.py")
        print("3. Choose option 3 for Quick Scan")
        
        print("\n📁 Created files:")
        print("• start_bazaraki.bat - Main launcher")
        print("• quick_scan.bat - Run quick scan")
        print("• test_system.bat - Test system")
        
    else:
        print("\n⚠️ SETUP INCOMPLETE")
        print("Please fix the failed steps above.")
        
        print("\n🔧 Common fixes:")
        print("• Install Chrome: https://www.google.com/chrome/")
        print("• Update Python: https://www.python.org/downloads/")
        print("• Run as Administrator if permission errors")
        print("• Disable antivirus temporarily during setup")

if __name__ == "__main__":
    main()