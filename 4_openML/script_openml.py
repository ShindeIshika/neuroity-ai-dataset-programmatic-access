# script_openml.py - OpenML Dataset Fetcher (FIXED)
# Platform #4: OpenML

import openml
import pandas as pd
import os

class OpenMLDatasetFetcher:
    """Complete implementation for OpenML dataset operations"""
    
    def __init__(self):
        """Initialize OpenML"""
        print("🔐 Initializing OpenML...")
        print("✅ Ready!\n")
    
    def search_datasets(self, search_term=None, max_results=5):
        """
        Search for datasets by keyword (using data_name filter)
        
        Args:
            search_term (str): Keyword to search for
            max_results (int): Number of results to display
        
        Returns:
            list: List of dataset IDs
        """
        print(f"🔍 Searching for datasets containing: '{search_term}'")
        print("-" * 60)
        
        try:
            print("🔄 Fetching dataset list from OpenML...")
            
            # Use data_name parameter for searching
            datasets = openml.datasets.list_datasets(
                output_format='dataframe',
                data_name=search_term if search_term else None
            )
            
            if datasets.empty:
                print("❌ No datasets found")
                print("\n💡 Try using a known dataset ID:")
                print("   - ID 61: iris")
                print("   - ID 151: diabetes")
                print("   - ID 53: breast-wisconsin")
                return []
            
            # Limit results
            if len(datasets) > max_results:
                datasets = datasets.head(max_results)
            
            print(f"\n📊 Found {len(datasets)} datasets:\n")
            dataset_ids = []
            for idx, (did, row) in enumerate(datasets.iterrows(), 1):
                name = row['name'] if 'name' in row else 'Unknown'
                desc = row['description'] if 'description' in row and pd.notna(row['description']) else 'No description'
                desc_short = desc[:100] + '...' if len(str(desc)) > 100 else desc
                
                print(f"  {idx}. {name} (ID: {did})")
                print(f"     Description: {desc_short}")
                print(f"     Instances: {row['NumberOfInstances'] if 'NumberOfInstances' in row else 'N/A'}")
                print(f"     Features: {row['NumberOfFeatures'] if 'NumberOfFeatures' in row else 'N/A'}")
                print(f"     Classes: {row['NumberOfClasses'] if 'NumberOfClasses' in row else 'N/A'}")
                dataset_ids.append(did)
                print()
            
            return dataset_ids
            
        except Exception as e:
            print(f"❌ Error searching datasets: {e}")
            print("\n💡 Try using a known dataset ID instead:")
            print("   - ID 61: iris")
            print("   - ID 151: diabetes")
            print("   - ID 53: breast-wisconsin")
            print("   - ID 40978: wine")
            return []
    
    def download_dataset(self, dataset_id, download_path="./datasets/openml/"):
        """
        Download a dataset by ID
        
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
            
            print(f"🔄 Fetching dataset from OpenML...")
            dataset = openml.datasets.get_dataset(dataset_id)
            
            # Get data
            X, y, categorical_indicator, attribute_names = dataset.get_data(
                dataset_format='dataframe',
                target=dataset.default_target_attribute
            )
            
            # Combine features and target
            if y is not None:
                df = X.copy()
                df['target'] = y
            else:
                df = X
            
            # Save as CSV
            output_file = os.path.join(download_path, f"openml_dataset_{dataset_id}.csv")
            df.to_csv(output_file, index=False)
            
            print(f"✅ Dataset saved to: {output_file}")
            print(f"📊 Shape: {df.shape[0]} rows, {df.shape[1]} columns")
            print(f"📋 Columns: {', '.join(df.columns[:10])}{'...' if len(df.columns) > 10 else ''}")
            
            print(f"\n📋 Dataset Info:")
            print(f"  Name: {dataset.name}")
            if dataset.description:
                desc = dataset.description[:200] + '...' if len(dataset.description) > 200 else dataset.description
                print(f"  Description: {desc}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error downloading dataset: {e}")
            return False
    
    def list_popular_datasets(self):
        """List popular OpenML datasets"""
        popular = [
            {"id": 61, "name": "iris"},
            {"id": 151, "name": "diabetes"},
            {"id": 53, "name": "breast-wisconsin"},
            {"id": 40978, "name": "wine"},
            {"id": 40927, "name": "adult"},
            {"id": 40981, "name": "credit-g"},
            {"id": 40966, "name": "boston"},
        ]
        
        print("\n🌟 Popular OpenML Datasets (with IDs):")
        print("-" * 60)
        for item in popular:
            print(f"  ID {item['id']:5d}: {item['name']}")

def main():
    """Main execution function"""
    print("=" * 60)
    print("📊 OPENML DATASET FETCHER")
    print("=" * 60)
    print()
    
    fetcher = OpenMLDatasetFetcher()
    fetcher.list_popular_datasets()
    
    print("\n" + "=" * 60)
    print("\n📝 Enter a dataset ID to download:")
    print("   Example: 61 (iris), 151 (diabetes), 53 (breast-wisconsin)")
    
    choice = input("\nEnter dataset ID (or press Enter for 61/iris): ").strip()
    
    if choice == '':
        fetcher.download_dataset(61)  # Default to iris
    else:
        try:
            fetcher.download_dataset(int(choice))
        except ValueError:
            print("❌ Please enter a valid number")
    
    print("\n✨ Done!")

if __name__ == "__main__":
    main()