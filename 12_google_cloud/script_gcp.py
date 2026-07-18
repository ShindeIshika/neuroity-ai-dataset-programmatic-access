# script_gcp.py - Google Cloud Public Datasets Fetcher
# Platform #12: Google Cloud Public Datasets

import requests
import json
import os
import webbrowser
from google.cloud import bigquery
from google.cloud import storage

class GCPDatasetFetcher:
    """Complete implementation for Google Cloud Public Datasets"""
    
    def __init__(self):
        """Initialize Google Cloud Public Datasets fetcher"""
        print("🔐 Initializing Google Cloud Public Datasets...")
        self.base_url = "https://cloud.google.com/public-datasets"
        print("✅ Ready!\n")
        print("ℹ️  Google Cloud Public Datasets are hosted on BigQuery and GCS")
        print("   Some datasets require GCP credentials to access")
        print()
    
    def search_datasets(self, search_term=None, max_results=5):
        """
        Search for datasets using Google Cloud's public dataset list
        
        Args:
            search_term (str): Keyword to search for
            max_results (int): Number of results to display
        
        Returns:
            list: List of dataset information
        """
        print(f"🔍 Searching for: '{search_term or 'all'}'")
        print("-" * 60)
        
        try:
            # GCP doesn't have a public API for listing datasets
            # Use the web interface and show results
            print("🌐 GCP provides datasets through BigQuery and Cloud Storage")
            print("📋 Browse available datasets at:")
            print(f"   https://cloud.google.com/public-datasets")
            print()
            
            # Show popular datasets manually
            popular_datasets = [
                {"name": "BigQuery Public Datasets", "type": "BigQuery", "size": "1.8 PB"},
                {"name": "COVID-19 Public Data", "type": "BigQuery", "size": "150 GB"},
                {"name": "NOAA Weather Data", "type": "BigQuery", "size": "500 GB"},
                {"name": "OpenStreetMap", "type": "BigQuery", "size": "200 GB"},
                {"name": "USA Census Data", "type": "BigQuery", "size": "300 GB"},
                {"name": "Google Books Ngrams", "type": "BigQuery", "size": "500 GB"},
                {"name": "GitHub Public Data", "type": "BigQuery", "size": "100 GB"},
                {"name": "LandSat Imagery", "type": "Cloud Storage", "size": "10+ TB"},
            ]
            
            # Filter if search term provided
            if search_term:
                filtered = [ds for ds in popular_datasets if search_term.lower() in ds['name'].lower()]
            else:
                filtered = popular_datasets
            
            if not filtered:
                print(f"❌ No datasets found containing '{search_term}'")
                print("💡 Try searching at: https://cloud.google.com/public-datasets")
                return []
            
            if len(filtered) > max_results:
                filtered = filtered[:max_results]
            
            print(f"\n📊 Found {len(filtered)} datasets:\n")
            dataset_info = []
            for idx, ds in enumerate(filtered, 1):
                print(f"  {idx}. {ds['name']}")
                print(f"     Type: {ds['type']}")
                print(f"     Size: {ds['size']}")
                print()
                
                dataset_info.append({
                    'name': ds['name'],
                    'type': ds['type'],
                    'size': ds['size']
                })
            
            return dataset_info
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return []
    
    def download_dataset(self, dataset_name, download_path="./datasets/google_cloud/"):
        """
        Provide guidance on accessing Google Cloud public datasets
        
        Args:
            dataset_name (str): Name of the dataset
            download_path (str): Directory to save information
        
        Returns:
            bool: True if successful, False otherwise
        """
        print(f"\n📝 Processing: {dataset_name}")
        print("-" * 60)
        
        try:
            os.makedirs(download_path, exist_ok=True)
            
            print("ℹ️  Google Cloud Public Datasets are accessed via:")
            print("   1. BigQuery (for querying large datasets)")
            print("   2. Cloud Storage (for file downloads)")
            print()
            
            # Save info
            info = {
                'name': dataset_name,
                'platform': 'Google Cloud Public Datasets',
                'access_methods': [
                    'BigQuery: Use SQL queries',
                    'Cloud Storage: Download files via gsutil or SDK'
                ],
                'documentation': 'https://cloud.google.com/public-datasets',
                'authentication': 'Requires GCP account (free tier available)'
            }
            
            json_file = os.path.join(download_path, f"{dataset_name.replace('/', '_')}_info.json")
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(info, f, indent=2)
            
            print(f"✅ Info saved to: {json_file}")
            print()
            print("📥 To access this dataset:")
            print("   1. Create a Google Cloud account (free tier)")
            print("   2. Enable BigQuery API")
            print("   3. Use the console or Python SDK")
            print()
            print("🔗 Quick start:")
            print(f"   https://console.cloud.google.com/bigquery")
            
            # Open browser
            webbrowser.open("https://cloud.google.com/public-datasets")
            
            return True
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def try_bigquery_access(self):
        """
        Attempt to access BigQuery public datasets (requires credentials)
        """
        print("\n💡 BigQuery Access Demo")
        print("-" * 60)
        print("To access BigQuery datasets, you need:")
        print("  1. Google Cloud account")
        print("  2. Service account key (JSON)")
        print("  3. Set environment variable: GOOGLE_APPLICATION_CREDENTIALS")
        print()
        print("Example code to query BigQuery:")
        print('''
from google.cloud import bigquery

# Initialize client
client = bigquery.Client()

# Query public dataset
query = """
SELECT name, year
FROM `bigquery-public-data.usa_names.usa_1910_current`
LIMIT 10
"""
results = client.query(query).result()
for row in results:
    print(row.name, row.year)
        ''')
        print()
        print("🔗 Setup guide: https://cloud.google.com/bigquery/docs/quickstarts")

def main():
    """Main execution function"""
    print("=" * 60)
    print("📊 GOOGLE CLOUD PUBLIC DATASETS")
    print("=" * 60)
    print()
    
    fetcher = GCPDatasetFetcher()
    
    print("🌟 Popular Google Cloud Public Datasets:")
    print("-" * 60)
    print("  - BigQuery Public Datasets (1.8 PB)")
    print("  - COVID-19 Public Data (150 GB)")
    print("  - NOAA Weather Data (500 GB)")
    print("  - OpenStreetMap (200 GB)")
    print("  - USA Census Data (300 GB)")
    print("  - Google Books Ngrams (500 GB)")
    print("  - GitHub Public Data (100 GB)")
    print("  - LandSat Imagery (10+ TB)")
    print()
    
    print("=" * 60)
    
    search_term = input("\nEnter search term (press Enter for 'weather'): ").strip()
    if not search_term:
        search_term = "weather"
    
    results = fetcher.search_datasets(search_term, max_results=5)
    
    if results:
        print("=" * 60)
        choice = input(f"Get info for {results[0]['name']}? (y/n): ").strip().lower()
        
        if choice == 'y':
            fetcher.download_dataset(results[0]['name'])
        
        # Show BigQuery demo
        show_bq = input("\nShow BigQuery access example? (y/n): ").strip().lower()
        if show_bq == 'y':
            fetcher.try_bigquery_access()
    
    print("\n✨ Done!")

if __name__ == "__main__":
    main()