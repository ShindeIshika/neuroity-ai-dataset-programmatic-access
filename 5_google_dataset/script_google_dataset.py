# script_google_dataset.py - Google Dataset Search Fetcher
# Platform #5: Google Dataset Search
# Note: No official API exists - this uses web scraping

import requests
from bs4 import BeautifulSoup
import time
import os
import json
import re

class GoogleDatasetFetcher:
    """Complete implementation for Google Dataset Search using web scraping"""
    
    def __init__(self):
        """Initialize Google Dataset Search fetcher"""
        print("🔐 Initializing Google Dataset Search...")
        print("⚠️  Note: No official API exists. Using web scraping.")
        print("✅ Ready!\n")
    
    def search_datasets(self, search_term, max_results=5):
        """
        Search for datasets using Google Dataset Search
        
        Args:
            search_term (str): Keyword to search for
            max_results (int): Number of results to display
        
        Returns:
            list: List of dataset information
        """
        print(f"🔍 Searching for: '{search_term}'")
        print("-" * 60)
        
        try:
            # Build search URL
            from urllib.parse import quote
            encoded_term = quote(search_term)
            url = f"https://datasetsearch.research.google.com/search?src=0&query={encoded_term}"
            
            print(f"🌐 Fetching results from: {url}")
            
            # Headers to avoid detection
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            
            # Make request
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find dataset entries - Google's structure varies, try common patterns
            datasets = []
            
            # Look for dataset cards
            dataset_cards = soup.find_all('div', class_=re.compile(r'VAt4|gsc|result'))
            
            if not dataset_cards:
                # Try alternative selectors
                dataset_cards = soup.find_all('li', class_=re.compile(r'result|dataset'))
            
            for card in dataset_cards[:max_results]:
                try:
                    # Extract title
                    title_elem = card.find('h1') or card.find('h2') or card.find('h3') or card.find('a')
                    title = title_elem.get_text(strip=True) if title_elem else "Unknown"
                    
                    # Extract description
                    desc_elem = card.find('div', class_=re.compile(r'description|snippet'))
                    description = desc_elem.get_text(strip=True) if desc_elem else "No description"
                    
                    # Extract link
                    link_elem = card.find('a', href=True)
                    link = link_elem['href'] if link_elem else "#"
                    
                    # Extract provider
                    provider_elem = card.find('span', class_=re.compile(r'provider|source'))
                    provider = provider_elem.get_text(strip=True) if provider_elem else "Unknown"
                    
                    datasets.append({
                        'title': title[:100],
                        'description': description[:150],
                        'link': link,
                        'provider': provider
                    })
                    
                except Exception as e:
                    continue
            
            # If scraping didn't work, display manual search instructions
            if not datasets:
                print("\n⚠️  Web scraping limited. Please use the manual search method:")
                print(f"   🔗 {url}")
                print("\n📋 Recommended alternative: Use DataForSEO API")
                print("   https://docs.dataforseo.com/v3/serp/google/dataset_search/")
                return []
            
            print(f"\n📊 Found {len(datasets)} datasets:\n")
            for idx, ds in enumerate(datasets, 1):
                print(f"  {idx}. {ds['title']}")
                print(f"     Provider: {ds['provider']}")
                print(f"     Description: {ds['description']}")
                print(f"     Link: {ds['link']}")
                print()
            
            return datasets
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching results: {e}")
            print("\n💡 Recommendation: Use manual search via web browser")
            print("   https://datasetsearch.research.google.com/")
            return []
    
    def list_google_dataset_search_features(self):
        """List features of Google Dataset Search"""
        print("\n🌟 Google Dataset Search Features:")
        print("-" * 60)
        print("  • Searches 45+ million datasets from 13,000+ sources [citation:3]")
        print("  • Uses schema.org structured data markup [citation:7]")
        print("  • Filters: Last updated, Format, Usage rights, Topics")
        print("  • Free to use via web interface")
        print("  • Citation tool built-in")

def main():
    """Main execution function"""
    print("=" * 60)
    print("🔍 GOOGLE DATASET SEARCH FETCHER")
    print("=" * 60)
    print()
    
    fetcher = GoogleDatasetFetcher()
    fetcher.list_google_dataset_search_features()
    
    print("\n" + "=" * 60)
    print("\n📝 Options:")
    print("  1. Web scraping search (limited)")
    print("  2. Open in browser for full access")
    print("  3. Use DataForSEO API (paid)")
    
    choice = input("\nEnter choice (1-3, or press Enter for option 2): ").strip()
    
    if choice == '1':
        search_term = input("Enter search term: ").strip()
        if search_term:
            fetcher.search_datasets(search_term)
    else:
        print("\n🌐 Opening Google Dataset Search in browser...")
        import webbrowser
        webbrowser.open("https://datasetsearch.research.google.com/")
        print("✅ Browser opened! Search for your dataset there.")
    
    print("\n✨ Done!")

if __name__ == "__main__":
    main()