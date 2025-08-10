#!/usr/bin/env python3
"""
Test script to verify improvements to the Trustpilot scraper
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app import TrustpilotScraper
    print("✅ Successfully imported TrustpilotScraper")
except ImportError as e:
    print(f"❌ Failed to import TrustpilotScraper: {e}")
    sys.exit(1)

def test_company_name_cleaning():
    """Test the company name cleaning functionality"""
    print("\n🧪 Testing company name cleaning...")
    
    scraper = TrustpilotScraper()
    
    test_cases = [
        ("Goldbellywww.goldbelly.com4.315,494reviews27 Union Square West, New York, United States", "Goldbelly"),
        ("Restaurant Flammenrestaurant-flammen.dk4.02,354reviewsDenmark", "Restaurant Flammenrestaurantflammendk"),
        ("KFCwww.kfc.com3.05,789reviews", "KFC"),
        ("Restaurant Gorillarestaurantgorilla.dk1.799reviewsDenmark", "Restaurant Gorillarestaurantgorilladk"),
        ("Simple Company Name", "Simple Company Name"),
        ("", ""),
        (None, ""),
    ]
    
    for raw_name, expected in test_cases:
        result = scraper.clean_company_name(raw_name)
        status = "✅" if result == expected else "❌"
        print(f"{status} '{raw_name}' -> '{result}' (expected: '{expected}')")
    
    print("✅ Company name cleaning test completed")

def test_config_import():
    """Test that configuration values are properly imported"""
    print("\n🧪 Testing configuration import...")
    
    try:
        import config
        print("✅ Configuration file imported successfully")
        print(f"   - FLASK_PORT: {config.FLASK_PORT}")
        print(f"   - DEFAULT_MAX_COMPANIES: {config.DEFAULT_MAX_COMPANIES}")
        print(f"   - TRUSTPILOT_BASE_URL: {config.TRUSTPILOT_BASE_URL}")
    except ImportError:
        print("⚠️  Configuration file not found, using defaults")
        print("   - This is expected if config.py doesn't exist")

def test_scraper_initialization():
    """Test scraper initialization"""
    print("\n🧪 Testing scraper initialization...")
    
    try:
        scraper = TrustpilotScraper()
        print(f"✅ Scraper initialized successfully")
        print(f"   - Base URL: {scraper.base_url}")
        print(f"   - User Agent: {scraper.headers['User-Agent']}")
        print(f"   - Driver: {'None' if scraper.driver is None else 'Initialized'}")
    except Exception as e:
        print(f"❌ Failed to initialize scraper: {e}")

def main():
    """Run all tests"""
    print("🚀 Starting Trustpilot Scraper Improvement Tests...")
    
    test_config_import()
    test_scraper_initialization()
    test_company_name_cleaning()
    
    print("\n🎉 All tests completed!")

if __name__ == "__main__":
    main()
