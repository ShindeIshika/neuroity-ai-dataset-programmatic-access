# script.py - Updated for latest Kaggle API
from kaggle.api.kaggle_api_extended import KaggleApi
import os
import sys

class KaggleDatasetFetcher:
    """Complete implementation for Kaggle dataset operations"""
    
    def __init__(self):
        """Initialize and authenticate Kaggle API"""
        print("🔐 Initializing Kaggle API...")
        try:
            self.api = KaggleApi()
            self.api.authenticate()
            print("✅ Authentication successful!\n")
        except Exception as e:
            print(f"❌ Authentication failed: {e}")
            print("\nTroubleshooting:")
            print("1. Make sure kaggle.json is in: C:\\Users\\Ishika Shinde\\.kaggle\\")
            print("2. Check if the file is valid (download a new one from Kaggle)")
            sys.exit(1)
    
    def search_datasets(self, search_term, max_results=5):
        """
        Search for datasets by keyword
        
        Args:
            search_term (str): Keyword to search for
            max_results (int): Number of results to display
        
        Returns:
            list: List of dataset objects
        """
        print(f"🔍 Searching for: '{search_term}'")
        print("-" * 60)
        
        try:
            # Updated: Removed 'size' parameter, use pagination with 'page'
            # Get first page of results
            datasets = self.api.dataset_list(search=search_term, page=1)
            
            # Limit to max_results
            if len(datasets) > max_results:
                datasets = datasets[:max_results]
            
            if not datasets:
                print("❌ No datasets found")
                return []
            
            print(f"\n📊 Found {len(datasets)} datasets:\n")
            for idx, dataset in enumerate(datasets, 1):
                print(f"  {idx}. {dataset.ref}")
                print(f"     Title: {dataset.title}")
                print(f"     Size: {dataset.size if hasattr(dataset, 'size') else 'Unknown'}")
                print(f"     Downloads: {dataset.downloadCount if hasattr(dataset, 'downloadCount') else 'Unknown'}")
                print()
            
            return datasets
            
        except Exception as e:
            print(f"❌ Error searching datasets: {e}")
            return []
    
    def download_dataset(self, dataset_ref, download_path="./datasets/kaggle/"):
        """
        Download and extract a dataset
        
        Args:
            dataset_ref (str): Dataset reference (e.g., 'uciml/iris')
            download_path (str): Directory to save the dataset
        
        Returns:
            bool: True if successful, False otherwise
        """
        print(f"\n⬇️ Downloading dataset: {dataset_ref}")
        print("-" * 60)
        
        try:
            # Create directory if it doesn't exist
            os.makedirs(download_path, exist_ok=True)
            
            # Download and unzip
            self.api.dataset_download_files(
                dataset=dataset_ref,
                path=download_path,
                unzip=True,
                quiet=False
            )
            
            print(f"✅ Dataset successfully downloaded to: {download_path}")
            
            # List downloaded files
            print("\n📁 Downloaded files:")
            for file in os.listdir(download_path):
                file_path = os.path.join(download_path, file)
                if os.path.isfile(file_path):
                    size = os.path.getsize(file_path)
                    print(f"  - {file} ({size:,} bytes)")
            
            return True
            
        except Exception as e:
            print(f"❌ Error downloading dataset: {e}")
            return False
    
    def list_popular_datasets(self):
        """List some popular/predefined datasets to try"""
        popular = [
            "uciml/iris",
            "uciml/breast-cancer-wisconsin",
            "uciml/house-prices-advanced-regression-techniques",
            "mlg-ulb/creditcardfraud",
            "kaggle/titanic",
            "uciml/pima-indians-diabetes-database"
        ]
        
        print("\n🌟 Popular Kaggle Datasets to Try:")
        print("-" * 60)
        for idx, dataset in enumerate(popular, 1):
            print(f"  {idx}. {dataset}")
        
        return popular

def main():
    """Main execution function"""
    print("=" * 60)
    print("🗄️  KAGGLE DATASET FETCHER")
    print("=" * 60)
    print()
    
    # Initialize the fetcher
    fetcher = KaggleDatasetFetcher()
    
    # Show popular datasets
    fetcher.list_popular_datasets()
    
    print("\n" + "=" * 60)
    
    # Search for datasets
    search_term = input("\nEnter search term (press Enter to use 'iris'): ").strip()
    if not search_term:
        search_term = "iris"
    
    datasets = fetcher.search_datasets(search_term, max_results=5)
    
    if datasets:
        print("\n" + "=" * 60)
        print("Dataset found! To download:")
        print(f"  - Use reference: {datasets[0].ref}")
        print("  - Or try one of the popular datasets above")
        
        choice = input(f"\nDownload {datasets[0].ref}? (y/n): ").strip().lower()
        
        if choice == 'y':
            fetcher.download_dataset(datasets[0].ref)
        else:
            print("\n💡 Tip: To download a specific dataset, call:")
            print(f"  fetcher.download_dataset('uciml/iris')")
    
    print("\n✨ Done!")

if __name__ == "__main__":
    main()