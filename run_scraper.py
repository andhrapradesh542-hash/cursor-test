#!/usr/bin/env python3
"""
Bazaraki Electronics Deal Finder - Launcher Script
Simple menu-driven interface for running the scraper
"""

import os
import sys
import subprocess
from datetime import datetime

def print_banner():
    """Print application banner"""
    print("🔍💻📱 BAZARAKI ELECTRONICS DEAL FINDER 💰🎯")
    print("=" * 60)
    print("Find amazing electronics deals on Cyprus's largest marketplace!")
    print("=" * 60)

def run_command(cmd):
    """Run a system command"""
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def check_setup():
    """Check if the system is properly set up"""
    print("🔧 Checking system setup...")
    
    # Check if required files exist
    required_files = ['bazaraki_scraper.py', 'requirements.txt']
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    
    # Try importing required modules
    try:
        import requests
        import selenium
        import pandas
        print("✅ Required packages available")
        return True
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("Run option 1 (Setup) first")
        return False

def main_menu():
    """Display main menu and handle user choice"""
    while True:
        print("\n📋 MAIN MENU")
        print("-" * 30)
        print("1. 🛠️  Setup & Install Dependencies")
        print("2. 🧪 Run System Tests")
        print("3. 🚀 Run Deal Finder (Quick Scan)")
        print("4. 🔍 Run Deal Finder (Full Scan)")
        print("5. 📊 View Previous Results")
        print("6. ⚙️  Configuration")
        print("7. 📖 Help & Documentation")
        print("8. 🚪 Exit")
        
        choice = input("\nEnter your choice (1-8): ").strip()
        
        if choice == '1':
            setup_system()
        elif choice == '2':
            run_tests()
        elif choice == '3':
            run_quick_scan()
        elif choice == '4':
            run_full_scan()
        elif choice == '5':
            view_results()
        elif choice == '6':
            configure_system()
        elif choice == '7':
            show_help()
        elif choice == '8':
            print("👋 Goodbye! Happy deal hunting!")
            sys.exit(0)
        else:
            print("❌ Invalid choice. Please enter 1-8.")

def setup_system():
    """Run system setup"""
    print("\n🛠️ SYSTEM SETUP")
    print("-" * 20)
    
    if os.path.exists('setup.py'):
        print("Running setup script...")
        success, output = run_command("python setup.py")
        if success:
            print("✅ Setup completed successfully!")
        else:
            print(f"❌ Setup failed: {output}")
    else:
        print("❌ setup.py not found!")
        print("Installing dependencies manually...")
        success, output = run_command("pip install -r requirements.txt")
        if success:
            print("✅ Dependencies installed!")
        else:
            print(f"❌ Failed to install dependencies: {output}")

def run_tests():
    """Run system tests"""
    print("\n🧪 RUNNING TESTS")
    print("-" * 20)
    
    if os.path.exists('test_scraper.py'):
        success, output = run_command("python test_scraper.py")
        print(output)
    else:
        print("❌ test_scraper.py not found!")

def run_quick_scan():
    """Run quick scan (1 page per category)"""
    print("\n🚀 QUICK SCAN")
    print("-" * 15)
    print("Scanning 1 page per category (faster, fewer results)")
    
    if not check_setup():
        return
    
    print("Starting quick scan...")
    # Modify the scraper to run with limited pages
    cmd = "python -c \"from bazaraki_scraper import BazarakiScraper; s = BazarakiScraper(); deals = s.run_full_scan(1); s.export_deals(deals); s.close(); print(f'Found {len(deals)} deals!')\""
    success, output = run_command(cmd)
    print(output)

def run_full_scan():
    """Run full scan"""
    print("\n🔍 FULL SCAN")
    print("-" * 15)
    print("Scanning multiple pages per category (slower, more results)")
    
    if not check_setup():
        return
    
    print("Starting full scan...")
    success, output = run_command("python bazaraki_scraper.py")
    print(output)

def view_results():
    """View previous results"""
    print("\n📊 PREVIOUS RESULTS")
    print("-" * 20)
    
    # Look for result files
    html_files = [f for f in os.listdir('.') if f.startswith('bazaraki_deals_report_') and f.endswith('.html')]
    csv_files = [f for f in os.listdir('.') if f.startswith('bazaraki_deals_') and f.endswith('.csv')]
    
    if not html_files and not csv_files:
        print("❌ No previous results found.")
        print("Run a scan first (options 3 or 4)")
        return
    
    print("📄 Available reports:")
    
    all_files = []
    if html_files:
        print("\n🌐 HTML Reports:")
        for i, f in enumerate(sorted(html_files, reverse=True), 1):
            print(f"  {i}. {f}")
            all_files.append(f)
    
    if csv_files:
        print("\n📋 CSV Files:")
        for i, f in enumerate(sorted(csv_files, reverse=True), len(all_files) + 1):
            print(f"  {i}. {f}")
            all_files.append(f)
    
    if all_files:
        choice = input(f"\nOpen file (1-{len(all_files)}) or Enter to return: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(all_files):
            filename = all_files[int(choice) - 1]
            if filename.endswith('.html'):
                # Try to open in browser
                import webbrowser
                webbrowser.open(f'file://{os.path.abspath(filename)}')
                print(f"📖 Opened {filename} in browser")
            else:
                print(f"📂 File location: {os.path.abspath(filename)}")

def configure_system():
    """Configure system settings"""
    print("\n⚙️ CONFIGURATION")
    print("-" * 20)
    
    if os.path.exists('config.ini'):
        print("Current configuration file exists.")
        print("Edit config.ini manually or recreate it.")
        
        recreate = input("Recreate config.ini? (y/n): ").lower().strip()
        if recreate == 'y':
            # Recreate config
            success, output = run_command("python -c \"from setup import create_config_file; create_config_file()\"")
            if success:
                print("✅ Configuration file recreated!")
            else:
                print("❌ Failed to recreate configuration")
    else:
        print("Creating configuration file...")
        success, output = run_command("python -c \"from setup import create_config_file; create_config_file()\"")
        if success:
            print("✅ Configuration file created!")
        else:
            print("❌ Failed to create configuration")

def show_help():
    """Show help and documentation"""
    print("\n📖 HELP & DOCUMENTATION")
    print("-" * 30)
    
    help_text = """
🎯 WHAT THIS TOOL DOES:
   Finds electronics deals on bazaraki.com by comparing prices
   with market averages and identifying items priced below market value.

🔍 WHAT IT FINDS:
   • iPhones (13, 14, 15 series)
   • MacBooks (Air, Pro)
   • Laptops (Dell XPS, ThinkPad, etc.)
   • Other electronics

📊 HOW IT WORKS:
   1. Scrapes bazaraki.com electronics listings
   2. Extracts prices and product details
   3. Compares with built-in market price database
   4. Identifies deals with 15%+ savings
   5. Exports results to CSV, JSON, and HTML

🚀 QUICK START:
   1. Run Setup (option 1)
   2. Run Tests (option 2) 
   3. Run Quick Scan (option 3)
   4. View Results (option 5)

📁 OUTPUT FILES:
   • CSV: Data for spreadsheets
   • JSON: Data for programming
   • HTML: Beautiful reports for viewing

⚡ TIPS:
   • Quick scan: Faster, fewer results
   • Full scan: Slower, more comprehensive
   • Check config.ini to adjust settings
   • Results saved in deals_reports/ folder
    """
    
    print(help_text)
    
    # Check if README exists
    if os.path.exists('README.md'):
        view_readme = input("\nView detailed README? (y/n): ").lower().strip()
        if view_readme == 'y':
            with open('README.md', 'r') as f:
                print("\n" + "="*60)
                print(f.read())

def main():
    """Main application entry point"""
    print_banner()
    
    # Quick system check
    if not os.path.exists('bazaraki_scraper.py'):
        print("❌ bazaraki_scraper.py not found!")
        print("Make sure you're in the correct directory.")
        sys.exit(1)
    
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye! Happy deal hunting!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()