#!/usr/bin/env python3
"""
Bazaraki Electronics Deal Finder
A comprehensive scraper for finding electronics deals on bazaraki.com
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import time
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import logging
from urllib.parse import urljoin, quote
import sqlite3
from dataclasses import dataclass
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bazaraki_scraper.log'),
        logging.StreamHandler()
    ]
)

@dataclass
class ProductListing:
    """Data class for product listings"""
    title: str
    price: float
    currency: str
    location: str
    url: str
    description: str
    posted_date: str
    seller_name: str
    contact_info: str
    images: List[str]
    category: str
    brand: str = ""
    model: str = ""
    condition: str = ""
    
class MarketPriceDatabase:
    """Database for storing and comparing market prices"""
    
    # Market price reference data (in EUR)
    MARKET_PRICES = {
        # iPhones (average used/new prices in EUR)
        'iphone_15_pro_max': {'used': 1100, 'new': 1300, 'keywords': ['iphone 15 pro max', 'iphone15 pro max']},
        'iphone_15_pro': {'used': 900, 'new': 1100, 'keywords': ['iphone 15 pro', 'iphone15 pro']},
        'iphone_15': {'used': 700, 'new': 900, 'keywords': ['iphone 15', 'iphone15']},
        'iphone_14_pro_max': {'used': 800, 'new': 1000, 'keywords': ['iphone 14 pro max', 'iphone14 pro max']},
        'iphone_14_pro': {'used': 650, 'new': 850, 'keywords': ['iphone 14 pro', 'iphone14 pro']},
        'iphone_14': {'used': 500, 'new': 700, 'keywords': ['iphone 14', 'iphone14']},
        'iphone_13_pro_max': {'used': 600, 'new': 800, 'keywords': ['iphone 13 pro max', 'iphone13 pro max']},
        'iphone_13_pro': {'used': 500, 'new': 700, 'keywords': ['iphone 13 pro', 'iphone13 pro']},
        'iphone_13': {'used': 400, 'new': 600, 'keywords': ['iphone 13', 'iphone13']},
        
        # Laptops (average used/new prices in EUR)
        'macbook_pro_16': {'used': 2000, 'new': 2500, 'keywords': ['macbook pro 16', 'macbook pro 16"', 'macbook pro 16 inch']},
        'macbook_pro_14': {'used': 1500, 'new': 2000, 'keywords': ['macbook pro 14', 'macbook pro 14"', 'macbook pro 14 inch']},
        'macbook_air_15': {'used': 1200, 'new': 1500, 'keywords': ['macbook air 15', 'macbook air 15"', 'macbook air 15 inch']},
        'macbook_air_13': {'used': 800, 'new': 1200, 'keywords': ['macbook air 13', 'macbook air 13"', 'macbook air 13 inch']},
        'dell_xps_15': {'used': 1000, 'new': 1500, 'keywords': ['dell xps 15', 'xps 15']},
        'dell_xps_13': {'used': 700, 'new': 1200, 'keywords': ['dell xps 13', 'xps 13']},
        'lenovo_thinkpad_x1': {'used': 800, 'new': 1500, 'keywords': ['thinkpad x1', 'lenovo x1']},
        'surface_laptop': {'used': 600, 'new': 1200, 'keywords': ['surface laptop', 'microsoft surface laptop']},
        'hp_spectre': {'used': 700, 'new': 1300, 'keywords': ['hp spectre', 'spectre laptop']},
        'asus_zenbook': {'used': 500, 'new': 1000, 'keywords': ['asus zenbook', 'zenbook']},
        'gaming_laptop': {'used': 800, 'new': 1500, 'keywords': ['gaming laptop', 'rog laptop', 'msi gaming']},
    }
    
    def identify_product(self, title: str, description: str) -> Optional[Tuple[str, str]]:
        """Identify product type and condition from title and description"""
        text = f"{title} {description}".lower()
        
        # Determine condition
        condition = "used"
        if any(word in text for word in ["new", "brand new", "unopened", "sealed"]):
            condition = "new"
        elif any(word in text for word in ["refurbished", "renewed", "certified"]):
            condition = "used"  # Treat refurbished as used for price comparison
            
        # Find matching product
        for product_id, data in self.MARKET_PRICES.items():
            for keyword in data['keywords']:
                if keyword in text:
                    return product_id, condition
                    
        return None, condition
    
    def get_market_price(self, product_id: str, condition: str) -> Optional[float]:
        """Get market price for a product"""
        if product_id in self.MARKET_PRICES:
            return self.MARKET_PRICES[product_id].get(condition)
        return None
    
    def calculate_deal_score(self, listing_price: float, market_price: float) -> float:
        """Calculate deal score (percentage below market price)"""
        if market_price <= 0:
            return 0
        return ((market_price - listing_price) / market_price) * 100

class BazarakiScraper:
    """Main scraper class for bazaraki.com"""
    
    def __init__(self, headless: bool = True):
        self.base_url = "https://www.bazaraki.com"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.market_db = MarketPriceDatabase()
        self.setup_selenium(headless)
        self.setup_database()
        
    def setup_selenium(self, headless: bool):
        """Setup Selenium WebDriver"""
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            logging.info("Chrome WebDriver initialized successfully")
        except Exception as e:
            logging.error(f"Failed to initialize Chrome WebDriver: {e}")
            raise
    
    def setup_database(self):
        """Setup SQLite database for storing listings"""
        self.conn = sqlite3.connect('bazaraki_deals.db')
        cursor = self.conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS listings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                price REAL,
                currency TEXT,
                location TEXT,
                url TEXT UNIQUE,
                description TEXT,
                posted_date TEXT,
                seller_name TEXT,
                contact_info TEXT,
                category TEXT,
                brand TEXT,
                model TEXT,
                condition TEXT,
                market_price REAL,
                deal_score REAL,
                scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conn.commit()
        logging.info("Database setup completed")
    
    def get_electronics_categories(self) -> List[str]:
        """Get electronics category URLs"""
        categories = [
            "/en/search/electronics/mobile-phones/",
            "/en/search/electronics/computers-laptops/",
            "/en/search/electronics/tablets/",
            "/en/search/electronics/audio-video/",
            "/en/search/electronics/cameras/",
            "/en/search/electronics/gaming/",
            "/en/search/electronics/smartwatches-wearables/",
        ]
        return [urljoin(self.base_url, cat) for cat in categories]
    
    def extract_price(self, price_text: str) -> Tuple[float, str]:
        """Extract price and currency from text"""
        if not price_text:
            return 0.0, "EUR"
            
        # Remove common non-numeric characters
        price_text = price_text.replace(",", "").replace(" ", "")
        
        # Extract currency
        currency = "EUR"
        if "€" in price_text:
            currency = "EUR"
        elif "$" in price_text:
            currency = "USD"
        elif "£" in price_text:
            currency = "GBP"
        
        # Extract numeric price
        price_match = re.search(r'[\d.]+', price_text)
        if price_match:
            try:
                price = float(price_match.group())
                # Convert to EUR if needed (approximate rates)
                if currency == "USD":
                    price *= 0.92
                elif currency == "GBP":
                    price *= 1.17
                return price, "EUR"  # Always return EUR for consistency
            except ValueError:
                pass
                
        return 0.0, currency
    
    def scrape_listing_details(self, listing_url: str) -> Optional[ProductListing]:
        """Scrape detailed information from a single listing"""
        try:
            self.driver.get(listing_url)
            time.sleep(2)
            
            # Extract title
            title_element = self.driver.find_element(By.CSS_SELECTOR, "h1, .item-title, .listing-title")
            title = title_element.text.strip() if title_element else "N/A"
            
            # Extract price
            price_element = self.driver.find_element(By.CSS_SELECTOR, ".price, .item-price, .listing-price")
            price_text = price_element.text.strip() if price_element else "0"
            price, currency = self.extract_price(price_text)
            
            # Extract location
            try:
                location_element = self.driver.find_element(By.CSS_SELECTOR, ".location, .item-location")
                location = location_element.text.strip()
            except NoSuchElementException:
                location = "Cyprus"
            
            # Extract description
            try:
                desc_element = self.driver.find_element(By.CSS_SELECTOR, ".description, .item-description, .listing-description")
                description = desc_element.text.strip()
            except NoSuchElementException:
                description = ""
            
            # Extract seller info
            try:
                seller_element = self.driver.find_element(By.CSS_SELECTOR, ".seller-name, .contact-name")
                seller_name = seller_element.text.strip()
            except NoSuchElementException:
                seller_name = "N/A"
            
            # Extract contact info
            try:
                contact_element = self.driver.find_element(By.CSS_SELECTOR, ".contact-info, .phone-number")
                contact_info = contact_element.text.strip()
            except NoSuchElementException:
                contact_info = "N/A"
            
            # Extract images
            images = []
            try:
                img_elements = self.driver.find_elements(By.CSS_SELECTOR, ".gallery img, .listing-images img")
                images = [img.get_attribute("src") for img in img_elements if img.get_attribute("src")]
            except NoSuchElementException:
                pass
            
            # Extract posted date
            try:
                date_element = self.driver.find_element(By.CSS_SELECTOR, ".date-posted, .posting-date")
                posted_date = date_element.text.strip()
            except NoSuchElementException:
                posted_date = datetime.now().strftime("%Y-%m-%d")
            
            return ProductListing(
                title=title,
                price=price,
                currency=currency,
                location=location,
                url=listing_url,
                description=description,
                posted_date=posted_date,
                seller_name=seller_name,
                contact_info=contact_info,
                images=images,
                category="Electronics"
            )
            
        except Exception as e:
            logging.error(f"Error scraping listing {listing_url}: {e}")
            return None
    
    def scrape_category(self, category_url: str, max_pages: int = 5) -> List[ProductListing]:
        """Scrape listings from a category"""
        listings = []
        
        for page in range(1, max_pages + 1):
            try:
                page_url = f"{category_url}?page={page}"
                logging.info(f"Scraping page {page}: {page_url}")
                
                self.driver.get(page_url)
                time.sleep(3)
                
                # Find listing links
                listing_links = self.driver.find_elements(By.CSS_SELECTOR, "a[href*='/en/item/']")
                
                if not listing_links:
                    logging.info(f"No more listings found on page {page}")
                    break
                
                # Extract listing URLs
                urls = []
                for link in listing_links:
                    href = link.get_attribute("href")
                    if href and "/en/item/" in href:
                        urls.append(href)
                
                # Remove duplicates
                urls = list(set(urls))
                logging.info(f"Found {len(urls)} unique listings on page {page}")
                
                # Scrape each listing
                for url in urls[:20]:  # Limit to 20 per page to avoid overloading
                    listing = self.scrape_listing_details(url)
                    if listing and listing.price > 0:  # Only include listings with valid prices
                        listings.append(listing)
                        time.sleep(1)  # Rate limiting
                
                time.sleep(2)  # Rate limiting between pages
                
            except Exception as e:
                logging.error(f"Error scraping category page {page}: {e}")
                continue
        
        return listings
    
    def analyze_deals(self, listings: List[ProductListing]) -> List[Dict]:
        """Analyze listings for good deals"""
        deals = []
        
        for listing in listings:
            try:
                # Identify product and condition
                product_id, condition = self.market_db.identify_product(
                    listing.title, listing.description
                )
                
                if not product_id:
                    continue
                
                # Get market price
                market_price = self.market_db.get_market_price(product_id, condition)
                if not market_price:
                    continue
                
                # Calculate deal score
                deal_score = self.market_db.calculate_deal_score(listing.price, market_price)
                
                # Only include if it's a good deal (at least 15% below market price)
                if deal_score >= 15:
                    deal_info = {
                        'title': listing.title,
                        'price': listing.price,
                        'market_price': market_price,
                        'deal_score': deal_score,
                        'savings': market_price - listing.price,
                        'location': listing.location,
                        'url': listing.url,
                        'description': listing.description[:200] + "..." if len(listing.description) > 200 else listing.description,
                        'seller': listing.seller_name,
                        'posted_date': listing.posted_date,
                        'product_type': product_id.replace('_', ' ').title(),
                        'condition': condition.title()
                    }
                    deals.append(deal_info)
                    
                    # Store in database
                    self.store_listing(listing, market_price, deal_score)
                    
            except Exception as e:
                logging.error(f"Error analyzing listing: {e}")
                continue
        
        # Sort by deal score (highest savings first)
        deals.sort(key=lambda x: x['deal_score'], reverse=True)
        return deals
    
    def store_listing(self, listing: ProductListing, market_price: float, deal_score: float):
        """Store listing in database"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO listings 
                (title, price, currency, location, url, description, posted_date, 
                 seller_name, contact_info, category, market_price, deal_score)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                listing.title, listing.price, listing.currency, listing.location,
                listing.url, listing.description, listing.posted_date,
                listing.seller_name, listing.contact_info, listing.category,
                market_price, deal_score
            ))
            self.conn.commit()
        except Exception as e:
            logging.error(f"Error storing listing: {e}")
    
    def export_deals(self, deals: List[Dict], filename: str = None):
        """Export deals to various formats"""
        if not deals:
            logging.info("No deals found to export")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Export to CSV
        csv_filename = filename or f"bazaraki_deals_{timestamp}.csv"
        df = pd.DataFrame(deals)
        df.to_csv(csv_filename, index=False)
        logging.info(f"Deals exported to {csv_filename}")
        
        # Export to JSON
        json_filename = f"bazaraki_deals_{timestamp}.json"
        with open(json_filename, 'w') as f:
            json.dump(deals, f, indent=2, ensure_ascii=False)
        logging.info(f"Deals exported to {json_filename}")
        
        # Create HTML report
        html_filename = f"bazaraki_deals_report_{timestamp}.html"
        self.create_html_report(deals, html_filename)
        
        return csv_filename, json_filename, html_filename
    
    def create_html_report(self, deals: List[Dict], filename: str):
        """Create an HTML report of deals"""
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Bazaraki Electronics Deals Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .deal {{ border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px; }}
                .deal-header {{ color: #d9534f; font-size: 18px; font-weight: bold; }}
                .deal-score {{ background: #5cb85c; color: white; padding: 5px 10px; border-radius: 3px; display: inline-block; }}
                .price {{ font-size: 20px; color: #337ab7; }}
                .savings {{ color: #5cb85c; font-weight: bold; }}
                .table {{ width: 100%; border-collapse: collapse; }}
                .table th, .table td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                .table th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            <h1>Bazaraki Electronics Deals Report</h1>
            <p>Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
            <p>Total deals found: {len(deals)}</p>
            
            <h2>Top Deals Summary</h2>
            <table class="table">
                <tr>
                    <th>Product</th>
                    <th>Price</th>
                    <th>Market Price</th>
                    <th>Savings</th>
                    <th>Deal Score</th>
                    <th>Location</th>
                </tr>
        """
        
        for deal in deals[:10]:  # Top 10 deals in table
            html_content += f"""
                <tr>
                    <td>{deal['title'][:50]}...</td>
                    <td>€{deal['price']:.2f}</td>
                    <td>€{deal['market_price']:.2f}</td>
                    <td class="savings">€{deal['savings']:.2f}</td>
                    <td><span class="deal-score">{deal['deal_score']:.1f}%</span></td>
                    <td>{deal['location']}</td>
                </tr>
            """
        
        html_content += """
            </table>
            
            <h2>Detailed Deals</h2>
        """
        
        for deal in deals:
            html_content += f"""
            <div class="deal">
                <div class="deal-header">{deal['title']}</div>
                <div class="price">€{deal['price']:.2f} 
                    <span class="deal-score">{deal['deal_score']:.1f}% OFF</span>
                </div>
                <p><strong>Market Price:</strong> €{deal['market_price']:.2f}</p>
                <p><strong>You Save:</strong> <span class="savings">€{deal['savings']:.2f}</span></p>
                <p><strong>Type:</strong> {deal['product_type']} ({deal['condition']})</p>
                <p><strong>Location:</strong> {deal['location']}</p>
                <p><strong>Seller:</strong> {deal['seller']}</p>
                <p><strong>Posted:</strong> {deal['posted_date']}</p>
                <p><strong>Description:</strong> {deal['description']}</p>
                <p><a href="{deal['url']}" target="_blank">View Listing</a></p>
            </div>
            """
        
        html_content += """
        </body>
        </html>
        """
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        logging.info(f"HTML report created: {filename}")
    
    def run_full_scan(self, max_pages_per_category: int = 3) -> List[Dict]:
        """Run a full scan of electronics categories"""
        logging.info("Starting full scan of Bazaraki electronics categories")
        
        all_listings = []
        categories = self.get_electronics_categories()
        
        for category_url in categories:
            logging.info(f"Scraping category: {category_url}")
            try:
                listings = self.scrape_category(category_url, max_pages_per_category)
                all_listings.extend(listings)
                logging.info(f"Found {len(listings)} listings in category")
                time.sleep(3)  # Rate limiting between categories
            except Exception as e:
                logging.error(f"Error scraping category {category_url}: {e}")
                continue
        
        logging.info(f"Total listings collected: {len(all_listings)}")
        
        # Analyze for deals
        deals = self.analyze_deals(all_listings)
        logging.info(f"Found {len(deals)} good deals")
        
        return deals
    
    def close(self):
        """Clean up resources"""
        if hasattr(self, 'driver'):
            self.driver.quit()
        if hasattr(self, 'conn'):
            self.conn.close()

def main():
    """Main function to run the scraper"""
    print("🔍 Bazaraki Electronics Deal Finder")
    print("=" * 50)
    
    scraper = None
    try:
        # Initialize scraper
        scraper = BazarakiScraper(headless=True)
        
        # Run scan
        deals = scraper.run_full_scan(max_pages_per_category=2)
        
        if deals:
            print(f"\n🎉 Found {len(deals)} great deals!")
            
            # Export results
            csv_file, json_file, html_file = scraper.export_deals(deals)
            
            # Display top deals
            print("\n🏆 TOP 5 DEALS:")
            print("-" * 80)
            for i, deal in enumerate(deals[:5], 1):
                print(f"{i}. {deal['title'][:60]}")
                print(f"   💰 Price: €{deal['price']:.2f} (Market: €{deal['market_price']:.2f})")
                print(f"   💚 Deal Score: {deal['deal_score']:.1f}% OFF (Save €{deal['savings']:.2f})")
                print(f"   📍 Location: {deal['location']}")
                print(f"   🔗 URL: {deal['url']}")
                print()
            
            print(f"\n📊 Reports generated:")
            print(f"   📋 CSV: {csv_file}")
            print(f"   📄 JSON: {json_file}")
            print(f"   🌐 HTML: {html_file}")
            
        else:
            print("❌ No deals found that meet the criteria.")
            print("Try adjusting the deal threshold or checking more categories.")
    
    except Exception as e:
        logging.error(f"Error in main execution: {e}")
        print(f"❌ Error occurred: {e}")
    
    finally:
        if scraper:
            scraper.close()

if __name__ == "__main__":
    main()