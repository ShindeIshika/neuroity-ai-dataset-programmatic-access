# script_aws.py - AWS Open Data Registry Fetcher
# Platform #11: AWS Open Data Registry

import requests
import json
import os
import boto3
import pandas as pd

class AWSOpenDataFetcher:
    """Complete implementation for AWS Open Data Registry"""
    
    def __init__(self):
        """Initialize AWS Open Data Registry fetcher"""
        print("🔐 Initializing AWS Open Data Registry...")
        self.registry_url = "https://registry.opendata.aws"
        self.api_url = "https://api.opendata.aws/v1"
        print("✅ Ready!\n")
    
    def search_datasets(self, search_term=None, max_results=5):
        """
        Search for datasets in AWS Open Data Registry
        
        Args:
            search_term (str): Keyword to search for
            max_results (int): Number of results to display
        
        Returns:
            list: List of dataset information
        """
        print(f"🔍 Searching for: '{search_term or 'all'}'")
        print("-" * 60)
        
        try:
            # Fetch all datasets from registry
            print(f"🌐 Fetching datasets from AWS Open Data Registry...")
            url = f"{self.api_url}/datasets"
            
            response = requests.get(url, timeout=30)
            
            if response.status_code != 200:
                print(f"⚠️  API returned status {response.status_code}")
                print(f"🌐 Using web fallback: {self.registry_url}")
                return []
            
            data = response.json()
            datasets = data.get('datasets', [])
            
            # Filter by search term if provided
            if search_term:
                filtered = []
                for ds in datasets:
                    name = ds.get('name', '').lower()
                    description = ds.get('description', '').lower()
                    if search_term.lower() in name or search_term.lower() in description:
                        filtered.append(ds)
                datasets = filtered
            
            if not datasets:
                print("❌ No datasets found")
                return []
            
            # Limit results
            if len(datasets) > max_results:
                datasets = datasets[:max_results]
            
            print(f"\n📊 Found {len(datasets)} datasets:\n")
            dataset_info = []
            for idx, dataset in enumerate(datasets, 1):
                name = dataset.get('name', 'Untitled')
                dataset_id = dataset.get('id', 'N/A')
                description = dataset.get('description', 'No description')
                if description and len(description) > 150:
                    description = description[:150] + '...'
                provider = dataset.get('provider', 'Unknown')
                tags = dataset.get('tags', [])
                tags_str = ', '.join(tags[:3]) if tags else 'No tags'
                
                # Check if S3 bucket info available
                has_s3 = bool(dataset.get('s3_bucket'))
                
                print(f"  {idx}. {name}")
                print(f"     ID: {dataset_id}")
                print(f"     Provider: {provider}")
                print(f"     Tags: {tags_str}")
                print(f"     S3 Access: {'Yes' if has_s3 else 'No'}")
                print(f"     Description: {description}")
                print()
                
                dataset_info.append({
                    'id': dataset_id,
                    'name': name,
                    'provider': provider,
                    'description': description,
                    's3_bucket': dataset.get('s3_bucket'),
                    's3_prefix': dataset.get('s3_prefix'),
                    'url': dataset.get('url', '')
                })
            
            return dataset_info
            
        except Exception as e:
            print(f"❌ Error: {e}")
            print(f"\n🌐 Try searching manually at: {self.registry_url}")
            return []
    
    def download_dataset(self, dataset_info, download_path="./datasets/aws/"):
        """
        Download dataset from S3 (if accessible)
        
        Args:
            dataset_info (dict): Dataset information from search
            download_path (str): Directory to save the dataset
        
        Returns:
            bool: True if successful, False otherwise
        """
        print(f"\n⬇️ Processing: {dataset_info['name']}")
        print("-" * 60)
        
        try:
            os.makedirs(download_path, exist_ok=True)
            
            # Save metadata
            info = {
                'name': dataset_info['name'],
                'provider': dataset_info['provider'],
                'description': dataset_info['description'],
                'url': dataset_info['url'],
                's3_bucket': dataset_info.get('s3_bucket'),
                's3_prefix': dataset_info.get('s3_prefix')
            }
            
            json_file = os.path.join(download_path, f"{dataset_info['name'].replace('/', '_')}_metadata.json")
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(info, f, indent=2)
            print(f"✅ Metadata saved to: {json_file}")
            
            # Check if S3 bucket info is available
            if info['s3_bucket']:
                print(f"\n📦 S3 Bucket: {info['s3_bucket']}")
                if info['s3_prefix']:
                    print(f"   Prefix: {info['s3_prefix']}")
                
                print("\n💡 To access this dataset, you can:")
                print(f"   1. Visit: https://{info['s3_bucket']}.s3.amazonaws.com/")
                print(f"   2. Use AWS CLI: aws s3 ls s3://{info['s3_bucket']}/{info['s3_prefix'] or ''}")
                
                # Try to list files using boto3 (no credentials required for public buckets)
                try:
                    s3 = boto3.client('s3', config=boto3.Config(signature_version=boto3.UNSIGNED))
                    prefix = info['s3_prefix'] or ''
                    
                    response = s3.list_objects_v2(
                        Bucket=info['s3_bucket'],
                        Prefix=prefix,
                        MaxKeys=10
                    )
                    
                    if 'Contents' in response:
                        print(f"\n📁 Sample files in this dataset:")
                        for obj in response['Contents'][:5]:
                            print(f"   - {obj['Key']} ({obj['Size']} bytes)")
                    else:
                        print("\n⚠️  No files listed (may require specific prefix)")
                        
                except Exception as e:
                    print(f"\n⚠️  Could not list files: {e}")
                    print("   (This bucket may require specific credentials)")
            
            # Open in browser if URL available
            if info['url']:
                print(f"\n🌐 Dataset URL: {info['url']}")
                import webbrowser
                webbrowser.open(info['url'])
            
            return True
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def list_popular_datasets(self):
        """List popular AWS Open Data datasets"""
        popular = [
            {"name": "Common Crawl", "description": "Web crawl data"},
            {"name": "OpenStreetMap", "description": "Geospatial data"},
            {"name": "NOAA GOES", "description": "Weather satellite imagery"},
            {"name": "NASA Earth Data", "description": "Earth science data"},
            {"name": "Amazon Reviews", "description": "Product review data"},
            {"name": "PubMed Central", "description": "Medical research papers"},
            {"name": "Climate Data", "description": "Climate and weather data"},
        ]
        
        print("\n🌟 Popular AWS Open Data Datasets:")
        print("-" * 60)
        for item in popular:
            print(f"  {item['name']} - {item['description']}")

def main():
    """Main execution function"""
    print("=" * 60)
    print("📊 AWS OPEN DATA REGISTRY FETCHER")
    print("=" * 60)
    print()
    
    fetcher = AWSOpenDataFetcher()
    fetcher.list_popular_datasets()
    
    print("\n" + "=" * 60)
    
    search_term = input("\nEnter search term (press Enter for 'climate'): ").strip()
    if not search_term:
        search_term = "climate"
    
    results = fetcher.search_datasets(search_term, max_results=5)
    
    if results:
        print("=" * 60)
        choice = input(f"Process dataset {results[0]['name']}? (y/n): ").strip().lower()
        
        if choice == 'y':
            fetcher.download_dataset(results[0])
        else:
            print("\n💡 To process a specific dataset, use:")
            print(f"  fetcher.download_dataset(dataset_info)")
    
    print("\n✨ Done!")

if __name__ == "__main__":
    main()