# script_datagov.py - Data.gov Dataset Fetcher (Web Scraping Fallback)
# Platform #6: Data.gov

import requests
from bs4 import BeautifulSoup
import os
import time
import re
import pandas as pd

class DataGovFetcher:
    """Complete implementation for Data.gov using web scraping fallback"""
    
    def __init__(self):
        """Initialize Data.gov fetcher"""
        print("🔐 Initializing Data.gov...")
        print("⚠️  API unavailable - using web scraping fallback")
        self.base_url = "https://catalog.data.gov"
        self.search_url = "https://catalog.data.gov/dataset"
        print("✅ Ready!\n")
    
    def search_datasets(self, search_term, max_results=5):
        """
        Search for datasets by scraping Data.gov search page
        
        Args:
            search_term (str): Keyword to search for
            max_results (int): Number of results to display
        
        Returns:
            list: List of dataset URLs and titles
        """
        print(f"🔍 Searching for: '{search_term}'")
        print("-" * 60)
        
        try:
            # Build search URL
            params = {'q': search_term}
            
            print(f"🌐 Fetching results from: {self.search_url}")
            print(f"📡 URL: {self.search_url}?q={search_term}")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(self.search_url, params=params, headers=headers, timeout=30)
            
            if response.status_code != 200:
                print(f"❌ Failed to fetch page: Status {response.status_code}")
                print("\n💡 You can manually search at:")
                print(f"   {self.search_url}?q={search_term}")
                return []
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find dataset results
            # Common patterns in Data.gov search results
            datasets = []
            
            # Look for dataset cards or list items
            results = soup.find_all('li', class_=re.compile(r'result|dataset|item'))
            
            if not results:
                # Try alternative selectors
                results = soup.find_all('div', class_=re.compile(r'search-result|dataset-item|result-item'))
            
            if not results:
                # Try looking for h3 tags with links
                headers = soup.find_all('h3')
                for h3 in headers[:max_results*2]:
                    link = h3.find('a', href=True)
                    if link:
                        title = link.get_text(strip=True)
                        url = link['href']
                        if not url.startswith('http'):
                            url = self.base_url + url
                        datasets.append({
                            'title': title,
                            'url': url
                        })
            
            # If still no results, extract from any link
            if not datasets:
                links = soup.find_all('a', href=True)
                for link in links[:max_results*3]:
                    href = link['href']
                    if '/dataset/' in href and len(link.get_text(strip=True)) > 10:
                        title = link.get_text(strip=True)
                        if not href.startswith('http'):
                            href = self.base_url + href
                        datasets.append({
                            'title': title[:100],
                            'url': href
                        })
            
            if not datasets:
                print("❌ No datasets found via scraping")
                print("\n💡 Try searching manually at:")
                print(f"   {self.search_url}?q={search_term}")
                return []
            
            # Remove duplicates
            seen = set()
            unique_datasets = []
            for ds in datasets:
                if ds['url'] not in seen:
                    seen.add(ds['url'])
                    unique_datasets.append(ds)
            
            datasets = unique_datasets[:max_results]
            
            print(f"\n📊 Found {len(datasets)} datasets:\n")
            for idx, ds in enumerate(datasets, 1):
                print(f"  {idx}. {ds['title']}")
                print(f"     URL: {ds['url']}")
                print()
            
            return datasets
            
        except Exception as e:
            print(f"❌ Error fetching results: {e}")
            print("\n💡 Try searching manually at:")
            print(f"   {self.search_url}?q={search_term}")
            return []
    
    def download_dataset(self, dataset_url, download_path="./datasets/datagov/"):
        """
        Download a dataset from its page (scrapes for download links)
        
        Args:
            dataset_url (str): URL of the dataset page
            download_path (str): Directory to save the dataset
        
        Returns:
            bool: True if successful, False otherwise
        """
        print(f"\n⬇️ Processing dataset: {dataset_url}")
        print("-" * 60)
        
        try:
            os.makedirs(download_path, exist_ok=True)
            
            print(f"🔄 Fetching dataset page...")
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            response = requests.get(dataset_url, headers=headers, timeout=30)
            
            if response.status_code != 200:
                print(f"❌ Failed to fetch page: Status {response.status_code}")
                return False
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find download links (common patterns on Data.gov)
            download_links = []
            
            # Look for CSV, Excel, JSON links
            for ext in ['csv', 'xlsx', 'json', 'xml']:
                for link in soup.find_all('a', href=True):
                    href = link['href'].lower()
                    if ext in href and 'download' in href:
                        full_url = link['href']
                        if not full_url.startswith('http'):
                            full_url = self.base_url + full_url
                        download_links.append({
                            'url': full_url,
                            'format': ext.upper(),
                            'text': link.get_text(strip=True)
                        })
            
            if not download_links:
                print("❌ No downloadable resources found on this page")
                print("💡 You may need to download manually from the page")
                return False
            
            # Download first resource
            selected = download_links[0]
            print(f"🔄 Downloading: {selected['format']} file")
            
            file_response = requests.get(selected['url'], stream=True, timeout=60)
            file_response.raise_for_status()
            
            # Save file
            filename = f"datagov_dataset_{int(time.time())}.{selected['format'].lower()}"
            filepath = os.path.join(download_path, filename)
            
            with open(filepath, 'wb') as f:
                for chunk in file_response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            print(f"✅ Dataset saved to: {filepath}")
            
            # Try to read if CSV
            if selected['format'].lower() == 'csv':
                try:
                    df = pd.read_csv(filepath)
                    print(f"📊 Shape: {df.shape[0]} rows, {df.shape[1]} columns")
                except:
                    pass
            
            return True
            
        except Exception as e:
            print(f"❌ Error downloading dataset: {e}")
            return False
    
    def list_popular_datasets(self):
        """List popular datasets on Data.gov"""
        print("\n🌟 Popular Data.gov Datasets:")
        print("-" * 60)
        print("  Search for datasets at: https://catalog.data.gov/dataset")
        print("  Popular topics: Education, Climate, Health, Transportation")
        print()

def main():
    """Main execution function"""
    print("=" * 60)
    print("📊 DATA.GOV DATASET FETCHER")
    print("=" * 60)
    print()
    
    fetcher = DataGovFetcher()
    fetcher.list_popular_datasets()
    
    print("=" * 60)
    
    search_term = input("\nEnter search term (press Enter for 'covid'): ").strip()
    if not search_term:
        search_term = "covid"
    
    datasets = fetcher.search_datasets(search_term, max_results=5)
    
    if datasets:
        print("=" * 60)
        choice = input(f"Process dataset 1: {datasets[0]['title']}? (y/n): ").strip().lower()
        
        if choice == 'y':
            fetcher.download_dataset(datasets[0]['url'])
        else:
            print("\n💡 To download, use the URL:")
            print(f"  {datasets[0]['url']}")
    
    print("\n✨ Done!")

if __name__ == "__main__":
    main()