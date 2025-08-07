#!/usr/bin/env python3
"""
Setup script for Bazaraki Electronics Deal Finder
Installs required dependencies and Chrome browser
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, check=True):
    """Run a shell command"""
    print(f"Running: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, check=check, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        if e.stderr:
            print(f"Error output: {e.stderr}")
        return False

def install_chrome():
    """Install Google Chrome"""
    print("🌐 Installing Google Chrome...")
    
    # Detect OS
    if sys.platform.startswith('linux'):
        commands = [
            "wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -",
            "echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | sudo tee /etc/apt/sources.list.d/google-chrome.list",
            "sudo apt update",
            "sudo apt install -y google-chrome-stable"
        ]
        for cmd in commands:
            if not run_command(cmd):
                print("❌ Failed to install Chrome")
                return False
    elif sys.platform == 'darwin':  # macOS
        if not run_command("brew install --cask google-chrome", check=False):
            print("Please install Chrome manually from https://www.google.com/chrome/")
    else:  # Windows
        print("Please install Chrome manually from https://www.google.com/chrome/")
    
    print("✅ Chrome installation completed")
    return True

def install_python_packages():
    """Install Python packages"""
    print("📦 Installing Python packages...")
    
    # Upgrade pip first
    run_command(f"{sys.executable} -m pip install --upgrade pip")
    
    # Install packages
    if not run_command(f"{sys.executable} -m pip install -r requirements.txt"):
        print("❌ Failed to install Python packages")
        return False
    
    print("✅ Python packages installed successfully")
    return True

def create_config_file():
    """Create configuration file"""
    config_content = """# Bazaraki Scraper Configuration
# Adjust these settings based on your preferences

[scraping]
# Maximum pages to scrape per category (1-10)
max_pages_per_category = 3

# Minimum deal percentage to report (e.g., 15 = 15% off market price)
min_deal_percentage = 15

# Rate limiting delay between requests (seconds)
request_delay = 2

# Headless browser mode (True/False)
headless_mode = True

[categories]
# Electronics categories to scrape
mobile_phones = True
computers_laptops = True
tablets = True
audio_video = True
cameras = True
gaming = True
smartwatches = True

[output]
# Export formats
export_csv = True
export_json = True
export_html = True

# Output directory
output_dir = ./deals_reports/
"""
    
    with open('config.ini', 'w') as f:
        f.write(config_content)
    
    print("✅ Configuration file created: config.ini")

def main():
    """Main setup function"""
    print("🚀 Bazaraki Electronics Deal Finder Setup")
    print("=" * 50)
    
    # Check if requirements.txt exists
    if not Path("requirements.txt").exists():
        print("❌ requirements.txt not found!")
        return
    
    # Install Chrome
    install_chrome()
    
    # Install Python packages
    install_python_packages()
    
    # Create config file
    create_config_file()
    
    # Create output directory
    os.makedirs("deals_reports", exist_ok=True)
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Review config.ini and adjust settings if needed")
    print("2. Run: python bazaraki_scraper.py")
    print("3. Check the deals_reports/ directory for results")
    
    # Test run option
    test = input("\nWould you like to run a quick test? (y/n): ").lower().strip()
    if test == 'y':
        print("\n🧪 Running quick test...")
        run_command("python bazaraki_scraper.py --test", check=False)

if __name__ == "__main__":
    main()