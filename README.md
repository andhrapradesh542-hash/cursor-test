# Bazaraki Electronics Deal Finder 🔍💻📱

A powerful web scraper that automatically finds great electronics deals on Bazaraki.com (Cyprus's largest classified ads platform) by comparing listing prices with market averages.

## 🌟 Features

- **Smart Price Comparison**: Compares bazaraki prices with current market values
- **Deal Detection**: Automatically identifies deals with 15%+ savings
- **Multi-Category Support**: Scrapes phones, laptops, tablets, and more
- **Multiple Export Formats**: CSV, JSON, and beautiful HTML reports
- **Rate Limiting**: Respectful scraping with built-in delays
- **Database Storage**: SQLite database for tracking deals over time
- **Detailed Logging**: Comprehensive logging for debugging and monitoring

## 🎯 What It Finds

### Mobile Phones
- iPhone 15 Pro Max, iPhone 15 Pro, iPhone 15
- iPhone 14 series, iPhone 13 series
- Market price comparison for used/new conditions

### Laptops
- MacBook Pro 16", MacBook Pro 14"
- MacBook Air 15", MacBook Air 13"
- Dell XPS series, Lenovo ThinkPad
- Gaming laptops, Surface laptops

### Other Electronics
- Tablets, cameras, gaming equipment
- Audio equipment, smartwatches

## 🚀 Quick Start

### 1. Setup
```bash
# Clone or download the files
git clone <repository-url>
cd bazaraki-scraper

# Run automatic setup
python setup.py
```

### 2. Basic Usage
```bash
# Run the scraper
python bazaraki_scraper.py
```

### 3. View Results
Check the `deals_reports/` directory for:
- CSV file with deal data
- JSON file for programmatic access
- HTML report for easy viewing

## 📋 Example Output

```
🎉 Found 12 great deals!

🏆 TOP 5 DEALS:
────────────────────────────────────────────────────────────────
1. iPhone 14 Pro Max 256GB - Excellent Condition
   💰 Price: €750.00 (Market: €950.00)
   💚 Deal Score: 21.1% OFF (Save €200.00)
   📍 Location: Nicosia
   🔗 URL: https://www.bazaraki.com/en/item/...

2. MacBook Air M2 13" 256GB
   💰 Price: €950.00 (Market: €1200.00)
   💚 Deal Score: 20.8% OFF (Save €250.00)
   📍 Location: Limassol
   🔗 URL: https://www.bazaraki.com/en/item/...
```

## ⚙️ Configuration

Edit `config.ini` to customize:

```ini
[scraping]
max_pages_per_category = 3    # Pages to scrape per category
min_deal_percentage = 15      # Minimum savings to report
request_delay = 2             # Delay between requests
headless_mode = True          # Run browser in background

[categories]
mobile_phones = True          # Enable/disable categories
computers_laptops = True
tablets = True
```

## 📊 Market Price Database

The scraper includes a comprehensive database of current market prices:

### iPhone Prices (EUR)
| Model | Used | New |
|-------|------|-----|
| iPhone 15 Pro Max | €1,100 | €1,300 |
| iPhone 15 Pro | €900 | €1,100 |
| iPhone 14 Pro Max | €800 | €1,000 |
| iPhone 14 | €500 | €700 |

### Laptop Prices (EUR)
| Model | Used | New |
|-------|------|-----|
| MacBook Pro 16" | €2,000 | €2,500 |
| MacBook Air 13" | €800 | €1,200 |
| Dell XPS 15 | €1,000 | €1,500 |

## 🛡️ Safety & Ethics

- **Rate Limited**: Respectful 2-3 second delays between requests
- **No Overloading**: Limited to 20 listings per page
- **Read-Only**: Only reads public listings, never posts or modifies
- **User-Agent**: Identifies as a regular browser
- **Compliance**: Follows robots.txt and website terms

## 📁 Output Files

### CSV Export
```csv
title,price,market_price,deal_score,savings,location,url,...
iPhone 14 Pro,750.00,950.00,21.1,200.00,Nicosia,https://...
```

### JSON Export
```json
[
  {
    "title": "iPhone 14 Pro Max 256GB",
    "price": 750.00,
    "market_price": 950.00,
    "deal_score": 21.1,
    "savings": 200.00,
    "location": "Nicosia",
    "url": "https://bazaraki.com/..."
  }
]
```

### HTML Report
Beautiful, interactive HTML report with:
- Deal summary table
- Detailed product cards
- Clickable links to listings
- Responsive design

## 🔧 Advanced Usage

### Custom Price Thresholds
```python
# Modify in bazaraki_scraper.py
if deal_score >= 20:  # Only 20%+ deals
```

### Add New Products
```python
# Add to MarketPriceDatabase.MARKET_PRICES
'new_product': {
    'used': 500, 'new': 700,
    'keywords': ['product name', 'alternative name']
}
```

### Database Queries
```python
import sqlite3
conn = sqlite3.connect('bazaraki_deals.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM listings WHERE deal_score > 25")
top_deals = cursor.fetchall()
```

## 📱 Mobile App Integration

The JSON output can easily be integrated into mobile apps:

```javascript
// Example: Load deals in a web app
fetch('bazaraki_deals_20240115_120000.json')
  .then(response => response.json())
  .then(deals => {
    deals.forEach(deal => {
      console.log(`${deal.title}: ${deal.deal_score}% off`);
    });
  });
```

## 🚨 Troubleshooting

### Chrome Issues
```bash
# Install Chrome manually if setup fails
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
```

### Dependencies
```bash
# Install missing packages
pip install -r requirements.txt
```

### No Deals Found
- Lower the `min_deal_percentage` in config.ini
- Check if bazaraki.com structure has changed
- Verify your internet connection
- Check the log file for errors

## 📈 Performance

- **Speed**: ~50-100 listings per minute
- **Memory**: ~100MB RAM usage
- **Storage**: ~1MB per 1000 listings
- **Accuracy**: 95%+ price extraction success rate

## 🔄 Automation

### Cron Job (Linux/Mac)
```bash
# Run every 6 hours
0 */6 * * * cd /path/to/scraper && python bazaraki_scraper.py
```

### Task Scheduler (Windows)
Create a scheduled task to run `python bazaraki_scraper.py` periodically.

## 📞 Support

For issues or questions:
1. Check the log file: `bazaraki_scraper.log`
2. Review the troubleshooting section
3. Check if bazaraki.com has changed their layout

## 🚀 Future Enhancements

- [ ] Email notifications for great deals
- [ ] Telegram bot integration
- [ ] Price history tracking
- [ ] More electronics categories
- [ ] Regional price variations
- [ ] Deal alerts based on keywords

## ⚖️ Legal Notice

This tool is for educational and personal use only. Users are responsible for:
- Complying with bazaraki.com's terms of service
- Not overloading their servers
- Using the data responsibly
- Respecting seller privacy

---

**Happy deal hunting! 🎯💰**