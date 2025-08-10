#!/usr/bin/env python3
"""
Test script for Trustpilot search functionality
"""

import requests
from bs4 import BeautifulSoup
import re

def test_trustpilot_search():
    base_url = "https://www.trustpilot.com"
    search_term = "restaurant"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Try different search URLs
    search_urls = [
        f"{base_url}/search?query={search_term}",
        f"{base_url}/search/companies?query={search_term}",
        f"{base_url}/search/businesses?query={search_term}",
        f"{base_url}/search/reviews?query={search_term}"
    ]
    
    for i, search_url in enumerate(search_urls):
        print(f"\n--- Testing URL {i+1}: {search_url} ---")
        try:
            response = requests.get(search_url, headers=headers)
            print(f"Status Code: {response.status_code}")
            print(f"Content Length: {len(response.content)}")
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Look for various link patterns
                all_links = soup.find_all('a', href=True)
                company_links = []
                
                for link in all_links:
                    href = link['href']
                    text = link.get_text(strip=True)
                    
                    # Look for potential company links
                    if any(pattern in href for pattern in ['/review/', '/reviews/', '/company/', '/business/']):
                        company_links.append({
                            'href': href,
                            'text': text,
                            'full_url': base_url + href if href.startswith('/') else href
                        })
                
                print(f"Found {len(company_links)} potential company links:")
                for link in company_links[:5]:  # Show first 5
                    print(f"  - {link['text']} -> {link['full_url']}")
                
                # Also check for any forms or search elements
                forms = soup.find_all('form')
                print(f"Found {len(forms)} forms")
                
                # Check page title
                title = soup.find('title')
                if title:
                    print(f"Page Title: {title.get_text()}")
                
            else:
                print(f"Error: {response.status_code}")
                
        except Exception as e:
            print(f"Exception: {e}")

if __name__ == "__main__":
    test_trustpilot_search()
