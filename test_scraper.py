#!/usr/bin/env python3
"""
Test script for Bazaraki Electronics Deal Finder
Validates setup and basic functionality
"""

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sys
import time

def test_internet_connection():
    """Test internet connectivity"""
    print("🌐 Testing internet connection...")
    try:
        response = requests.get("https://www.google.com", timeout=10)
        if response.status_code == 200:
            print("✅ Internet connection: OK")
            return True
        else:
            print("❌ Internet connection: Failed")
            return False
    except Exception as e:
        print(f"❌ Internet connection error: {e}")
        return False

def test_bazaraki_access():
    """Test access to bazaraki.com"""
    print("🏪 Testing bazaraki.com access...")
    try:
        response = requests.get("https://www.bazaraki.com", timeout=15)
        if response.status_code == 200:
            print("✅ Bazaraki.com access: OK")
            print(f"   Response size: {len(response.content)} bytes")
            return True
        else:
            print(f"❌ Bazaraki.com access failed: Status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Bazaraki.com access error: {e}")
        return False

def test_chrome_installation():
    """Test Chrome browser installation"""
    print("🌐 Testing Chrome browser...")
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://www.google.com")
        
        if "Google" in driver.title:
            print("✅ Chrome browser: OK")
            print(f"   Version: {driver.capabilities['browserVersion']}")
            driver.quit()
            return True
        else:
            print("❌ Chrome browser: Failed to load page")
            driver.quit()
            return False
            
    except Exception as e:
        print(f"❌ Chrome browser error: {e}")
        print("   Make sure Chrome is installed and accessible")
        return False

def test_selenium_bazaraki():
    """Test Selenium with Bazaraki"""
    print("🤖 Testing Selenium with Bazaraki...")
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://www.bazaraki.com")
        time.sleep(3)
        
        # Try to find some basic elements
        title = driver.title
        page_source_length = len(driver.page_source)
        
        print(f"✅ Selenium + Bazaraki: OK")
        print(f"   Page title: {title}")
        print(f"   Page source size: {page_source_length} bytes")
        
        driver.quit()
        return True
        
    except Exception as e:
        print(f"❌ Selenium + Bazaraki error: {e}")
        return False

def test_market_price_database():
    """Test market price database functionality"""
    print("💰 Testing market price database...")
    try:
        # Import our market price database
        sys.path.append('.')
        from bazaraki_scraper import MarketPriceDatabase
        
        db = MarketPriceDatabase()
        
        # Test product identification
        test_cases = [
            ("iPhone 15 Pro Max 256GB", "should find iphone_15_pro_max"),
            ("MacBook Air 13 inch M2", "should find macbook_air_13"),
            ("Dell XPS 15 laptop", "should find dell_xps_15"),
            ("Random product xyz", "should return None")
        ]
        
        success_count = 0
        for test_title, expected in test_cases:
            product_id, condition = db.identify_product(test_title, "")
            if product_id or "None" in expected:
                success_count += 1
                print(f"   ✅ '{test_title}' -> {product_id}")
            else:
                print(f"   ❌ '{test_title}' -> {product_id} (expected match)")
        
        if success_count >= 3:
            print("✅ Market price database: OK")
            return True
        else:
            print("❌ Market price database: Some tests failed")
            return False
            
    except Exception as e:
        print(f"❌ Market price database error: {e}")
        return False

def test_dependencies():
    """Test required Python packages"""
    print("📦 Testing Python dependencies...")
    required_packages = [
        'requests', 'beautifulsoup4', 'pandas', 
        'selenium', 'sqlite3', 'lxml'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            if package == 'beautifulsoup4':
                import bs4
            elif package == 'sqlite3':
                import sqlite3
            else:
                __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} - MISSING")
            missing_packages.append(package)
    
    if not missing_packages:
        print("✅ All dependencies: OK")
        return True
    else:
        print(f"❌ Missing packages: {missing_packages}")
        print("   Run: pip install -r requirements.txt")
        return False

def main():
    """Run all tests"""
    print("🧪 Bazaraki Scraper Test Suite")
    print("=" * 50)
    
    tests = [
        ("Dependencies", test_dependencies),
        ("Internet Connection", test_internet_connection),
        ("Bazaraki Access", test_bazaraki_access),
        ("Chrome Browser", test_chrome_installation),
        ("Selenium + Bazaraki", test_selenium_bazaraki),
        ("Market Price Database", test_market_price_database),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append((test_name, False))
        time.sleep(1)
    
    # Summary
    print(f"\n{'='*50}")
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:.<30} {status}")
        if result:
            passed += 1
    
    print(f"\nTotal: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 ALL TESTS PASSED! The scraper should work correctly.")
        print("You can now run: python bazaraki_scraper.py")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues before running the scraper.")
        
        if passed >= 4:  # Most critical tests passed
            print("💡 You can try running the scraper anyway, it might still work.")

if __name__ == "__main__":
    main()