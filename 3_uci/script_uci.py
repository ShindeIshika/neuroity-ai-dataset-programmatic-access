# script_uci.py - UCI Machine Learning Repository Fetcher (SIMPLIFIED)
# Platform #3: UCI Machine Learning Repository

from ucimlrepo import fetch_ucirepo
import pandas as pd
import os

class UCIDatasetFetcher:
    """Complete implementation for UCI Machine Learning Repository dataset operations"""
    
    def __init__(self):
        """Initialize UCI dataset fetcher"""
        print("🔐 Initializing UCI Machine Learning Repository...")
        print("✅ Ready!\n")
    
    def search_datasets(self):
        """
        Display available datasets from the list shown in the library
        """
        print("📋 Available datasets can be found at:")
        print("   https://archive.ics.uci.edu/datasets")
        print("\n💡 For this demo, we'll use known dataset IDs:")
        print("   - Iris: ID 53")
        print("   - Wine: ID 109")
        print("   - Boston Housing: ID 165")
        print("   - Breast Cancer: ID 17")
        print("   - Diabetes: ID 46")
        print("   - Sonar: ID 151")
        print("   - Mushroom: ID 73")
        print("   - Abalone: ID 1")
        
        return [53, 109, 165, 17, 46, 151, 73, 1]  # Return some default IDs
    
    def download_dataset(self, dataset_id, download_path="./datasets/uci/"):
        """
        Download a dataset by ID
        
        Args:
            dataset_id (int): Dataset ID (e.g., 53 for Iris)
            download_path (str): Directory to save the dataset
        
        Returns:
            bool: True if successful, False otherwise
        """
        print(f"\n⬇️ Downloading dataset ID: {dataset_id}")
        print("-" * 60)
        
        try:
            # Create directory if it doesn't exist
            os.makedirs(download_path, exist_ok=True)
            
            # Fetch dataset
            print(f"🔄 Fetching dataset from UCI...")
            dataset = fetch_ucirepo(id=dataset_id)
            
            # Get data
            X = dataset.data.features
            y = dataset.data.targets
            
            # Combine features and targets
            if X is not None and y is not None:
                df = pd.concat([X, y], axis=1)
            elif X is not None:
                df = X
            elif y is not None:
                df = y
            else:
                print("❌ No data found in this dataset")
                return False
            
            # Save as CSV
            output_file = os.path.join(download_path, f"uci_dataset_{dataset_id}.csv")
            df.to_csv(output_file, index=False)
            
            print(f"✅ Dataset saved to: {output_file}")
            print(f"📊 Shape: {df.shape[0]} rows, {df.shape[1]} columns")
            print(f"📋 Columns: {', '.join(df.columns[:10])}{'...' if len(df.columns) > 10 else ''}")
            
            # Show metadata
            if hasattr(dataset, 'metadata'):
                print(f"\n📋 Dataset Info:")
                if hasattr(dataset.metadata, 'name'):
                    print(f"  Name: {dataset.metadata.name}")
                if hasattr(dataset.metadata, 'year'):
                    print(f"  Year: {dataset.metadata.year}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error downloading dataset: {e}")
            return False
    
    def list_popular_datasets(self):
        """List popular UCI datasets with their IDs"""
        popular = [
            {"id": 53, "name": "Iris"},
            {"id": 109, "name": "Wine"},
            {"id": 17, "name": "Breast Cancer Wisconsin"},
            {"id": 46, "name": "Diabetes"},
            {"id": 165, "name": "Boston Housing"},
            {"id": 45, "name": "Heart Disease"},
            {"id": 52, "name": "Ionosphere"},
            {"id": 151, "name": "Sonar"},
            {"id": 73, "name": "Mushroom"},
            {"id": 1, "name": "Abalone"},
        ]
        
        print("\n🌟 Popular UCI Datasets (with IDs):")
        print("-" * 60)
        for item in popular:
            print(f"  ID {item['id']:3d}: {item['name']}")

def main():
    """Main execution function"""
    print("=" * 60)
    print("📊 UCI MACHINE LEARNING REPOSITORY FETCHER")
    print("=" * 60)
    print()
    
    # Initialize the fetcher
    fetcher = UCIDatasetFetcher()
    
    # Show popular datasets
    fetcher.list_popular_datasets()
    
    print("\n" + "=" * 60)
    print("\n📝 Enter a dataset ID to download:")
    print("   Example IDs: 53 (Iris), 109 (Wine), 17 (Breast Cancer)")
    print("   Or enter 'list' to see available datasets online")
    
    choice = input("\nEnter dataset ID (or press Enter for 53/Iris): ").strip()
    
    if choice.lower() == 'list':
        fetcher.search_datasets()
        dataset_id = input("\nEnter dataset ID to download: ").strip()
        if dataset_id:
            fetcher.download_dataset(int(dataset_id))
    elif choice == '':
        fetcher.download_dataset(53)  # Default to Iris
    else:
        try:
            fetcher.download_dataset(int(choice))
        except ValueError:
            print("❌ Please enter a valid number")
    
    print("\n✨ Done!")

if __name__ == "__main__":
    main()