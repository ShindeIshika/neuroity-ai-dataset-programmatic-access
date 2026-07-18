# script_zenodo.py - Zenodo Dataset Fetcher (FULLY FIXED)
# Platform #8: Zenodo

import requests
import os
import json
import pandas as pd
from datetime import datetime

class ZenodoFetcher:
    """Complete implementation for Zenodo dataset operations"""
    
    def __init__(self):
        """Initialize Zenodo fetcher"""
        print("🔐 Initializing Zenodo...")
        self.base_url = "https://zenodo.org/api"
        print("✅ Ready!\n")
    
    def search_datasets(self, search_term, max_results=5):
        """
        Search for datasets using Zenodo API
        
        Args:
            search_term (str): Keyword to search for
            max_results (int): Number of results to display
        
        Returns:
            list: List of dataset IDs
        """
        print(f"🔍 Searching for: '{search_term}'")
        print("-" * 60)
        
        try:
            url = f"{self.base_url}/records"
            params = {
                'q': search_term,
                'size': max_results,
                'sort': 'mostviewed'
            }
            
            print(f"🌐 Fetching results from Zenodo API...")
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            results = data.get('hits', {}).get('hits', [])
            
            if not results:
                print("❌ No datasets found")
                return []
            
            print(f"\n📊 Found {len(results)} datasets:\n")
            dataset_ids = []
            for idx, record in enumerate(results, 1):
                dataset_id = record.get('id')
                metadata = record.get('metadata', {})
                title = metadata.get('title', 'Untitled')
                description = metadata.get('description', 'No description')
                if description and len(description) > 150:
                    description = description[:150] + '...'
                creators = metadata.get('creators', [])
                creator_names = [c.get('name', '') for c in creators[:2]]
                creators_str = ', '.join(creator_names) if creator_names else 'Unknown'
                
                has_files = bool(record.get('files', []))
                
                print(f"  {idx}. {title}")
                print(f"     ID: {dataset_id}")
                print(f"     Creators: {creators_str}")
                print(f"     Has Files: {'Yes' if has_files else 'No'}")
                print(f"     Description: {description}")
                print()
                dataset_ids.append(dataset_id)
            
            return dataset_ids
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching results: {e}")
            return []
    
    def download_dataset(self, dataset_id, download_path="./datasets/zenodo/"):
        """
        Download a dataset by ID using the Zenodo API and manual fallback
        
        Args:
            dataset_id (int): Dataset ID
            download_path (str): Directory to save the dataset
        
        Returns:
            bool: True if successful, False otherwise
        """
        print(f"\n⬇️ Downloading dataset ID: {dataset_id}")
        print("-" * 60)
        
        try:
            os.makedirs(download_path, exist_ok=True)
            
            # Try API method first
            url = f"{self.base_url}/records/{dataset_id}"
            print(f"🔄 Fetching dataset metadata...")
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # Get files - handle different API response structures
            files = []
            
            # Try the new Zenodo API structure
            if 'files' in data:
                files = data.get('files', [])
            
            # If files is a dict with 'entries' (older structure)
            if not files and 'files' in data:
                file_entries = data.get('files', {})
                if isinstance(file_entries, dict) and 'entries' in file_entries:
                    files = [{'key': k, 'size': v.get('size', 'N/A'), 
                             'links': {'download': f"https://zenodo.org/record/{dataset_id}/files/{k}"}} 
                             for k, v in file_entries.get('entries', {}).items()]
            
            # If still no files, try the metadata files
            if not files and 'metadata' in data and 'files' in data['metadata']:
                files = data['metadata'].get('files', [])
            
            if not files:
                print("❌ No files found in this dataset via API")
                print("💡 Trying manual download method...")
                return self.download_manual(dataset_id, download_path)
            
            print(f"📁 Found {len(files)} file(s):")
            for i, file_info in enumerate(files, 1):
                filename = file_info.get('key') or file_info.get('filename') or file_info.get('name', 'Unknown')
                size = file_info.get('size', 'N/A')
                print(f"  {i}. {filename} ({size} bytes)")
            
            # Find first downloadable file
            download_file = None
            for file_info in files:
                # Try different ways to get download URL
                download_url = None
                filename = None
                
                # New Zenodo API
                if 'links' in file_info and 'download' in file_info['links']:
                    download_url = file_info['links']['download']
                    filename = file_info.get('key') or file_info.get('filename', 'zenodo_file')
                
                # Direct download link
                elif 'download' in file_info:
                    download_url = file_info['download']
                    filename = file_info.get('filename', 'zenodo_file')
                
                # Manual construction
                else:
                    filename = file_info.get('key') or file_info.get('filename') or file_info.get('name')
                    if filename:
                        download_url = f"https://zenodo.org/record/{dataset_id}/files/{filename}"
                
                if download_url and filename:
                    download_file = {'url': download_url, 'filename': filename}
                    break
            
            if not download_file:
                print("❌ No download URL found, trying manual download...")
                return self.download_manual(dataset_id, download_path)
            
            print(f"\n🔄 Downloading: {download_file['filename']}")
            
            # Download the file
            file_response = requests.get(download_file['url'], stream=True, timeout=60)
            file_response.raise_for_status()
            
            filepath = os.path.join(download_path, download_file['filename'])
            with open(filepath, 'wb') as f:
                for chunk in file_response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            print(f"✅ Dataset saved to: {filepath}")
            self._preview_file(filepath)
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"❌ API download failed: {e}")
            return self.download_manual(dataset_id, download_path)
        except Exception as e:
            print(f"❌ Error: {e}")
            return self.download_manual(dataset_id, download_path)
    
    def download_manual(self, dataset_id, download_path):
        """
        Manual download fallback for Zenodo datasets
        
        Args:
            dataset_id (int): Dataset ID
            download_path (str): Directory to save the dataset
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            print("💡 Manual download method:")
            print(f"   1. Open in browser: https://zenodo.org/record/{dataset_id}")
            print(f"   2. Click the download button for the file you want")
            print(f"   3. Save to: {download_path}")
            
            # Try to open in browser automatically
            import webbrowser
            print("\n🌐 Opening dataset in browser...")
            webbrowser.open(f"https://zenodo.org/record/{dataset_id}")
            
            print("✅ Browser opened. Please download the file manually.")
            return False
            
        except Exception as e:
            print(f"❌ Manual download failed: {e}")
            return False
    
    def _preview_file(self, filepath):
        """Helper to preview a downloaded file"""
        try:
            if filepath.endswith('.csv'):
                df = pd.read_csv(filepath)
                print(f"📊 Shape: {df.shape[0]} rows, {df.shape[1]} columns")
                print(f"📋 Columns: {', '.join(df.columns[:5])}{'...' if len(df.columns) > 5 else ''}")
                print(f"\n📄 First 5 rows:")
                print(df.head())
        except:
            pass
    
    def list_popular_datasets(self):
        """List popular Zenodo datasets"""
        print("\n🌟 Popular Zenodo Datasets (by ID):")
        print("-" * 60)
        popular = [
            {"id": 3736457, "name": "COVID-19 Dataset"},
            {"id": 254799, "name": "Twitter Sentiment Dataset"},
            {"id": 3907400, "name": "Climate Change Data"},
            {"id": 4686430, "name": "Medical Imaging Dataset"},
        ]
        for item in popular:
            print(f"  ID {item['id']:7d}: {item['name']}")

def main():
    """Main execution function"""
    print("=" * 60)
    print("📊 ZENODO DATASET FETCHER")
    print("=" * 60)
    print()
    
    fetcher = ZenodoFetcher()
    fetcher.list_popular_datasets()
    
    print("\n" + "=" * 60)
    
    search_term = input("\nEnter search term (press Enter for 'covid'): ").strip()
    if not search_term:
        search_term = "covid"
    
    dataset_ids = fetcher.search_datasets(search_term, max_results=5)
    
    if dataset_ids:
        print("=" * 60)
        choice = input(f"Download dataset ID {dataset_ids[0]}? (y/n): ").strip().lower()
        
        if choice == 'y':
            fetcher.download_dataset(dataset_ids[0])
        else:
            print("\n💡 To download a specific dataset, use:")
            print(f"  fetcher.download_dataset({dataset_ids[0]})")
    
    print("\n✨ Done!")

if __name__ == "__main__":
    main()