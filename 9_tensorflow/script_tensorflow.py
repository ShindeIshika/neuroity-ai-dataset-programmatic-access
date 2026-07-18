# script_tensorflow.py - TensorFlow Datasets Fetcher
# Platform #9: TensorFlow Datasets

import tensorflow_datasets as tfds
import os
import pandas as pd
import numpy as np

class TensorFlowDatasetFetcher:
    """Complete implementation for TensorFlow Datasets operations"""
    
    def __init__(self):
        """Initialize TensorFlow Datasets"""
        print("🔐 Initializing TensorFlow Datasets...")
        print("✅ Ready!\n")
    
    def search_datasets(self, search_term=None, max_results=5):
        """
        Search for datasets by keyword
        
        Args:
            search_term (str): Keyword to search for
            max_results (int): Number of results to display
        
        Returns:
            list: List of dataset names
        """
        print(f"🔍 Searching for datasets containing: '{search_term}'")
        print("-" * 60)
        
        try:
            # Get list of all available datasets
            print("🔄 Fetching dataset list from TensorFlow Datasets...")
            all_datasets = tfds.list_builders()
            
            # Filter by search term if provided
            if search_term:
                filtered = [ds for ds in all_datasets if search_term.lower() in ds.lower()]
            else:
                filtered = all_datasets
            
            # Limit results
            if len(filtered) > max_results:
                filtered = filtered[:max_results]
            
            if not filtered:
                print("❌ No datasets found")
                print("\n💡 Try: 'mnist', 'cifar10', 'imdb_reviews', 'iris'")
                return []
            
            print(f"\n📊 Found {len(filtered)} datasets:\n")
            for idx, ds_name in enumerate(filtered, 1):
                print(f"  {idx}. {ds_name}")
                # Try to get dataset info
                try:
                    info = tfds.builder(ds_name).info
                    print(f"     Description: {info.description[:100] + '...' if len(info.description) > 100 else info.description}")
                    print(f"     Features: {len(info.features)} features")
                except:
                    pass
                print()
            
            return filtered
            
        except Exception as e:
            print(f"❌ Error searching datasets: {e}")
            return []
    
    def download_dataset(self, dataset_name, split='train', download_path="./datasets/tensorflow/"):
        """
        Download a dataset
        
        Args:
            dataset_name (str): Name of the dataset (e.g., 'mnist')
            split (str): Which split to download ('train', 'test', 'all')
            download_path (str): Directory to save the dataset
        
        Returns:
            bool: True if successful, False otherwise
        """
        print(f"\n⬇️ Downloading dataset: {dataset_name}")
        print("-" * 60)
        
        try:
            # Create directory
            os.makedirs(download_path, exist_ok=True)
            
            # Load dataset
            print(f"🔄 Loading dataset (this may take a moment)...")
            
            if split == 'all':
                ds = tfds.load(dataset_name, split=['train', 'test'], as_supervised=True)
                ds_train = ds[0]
                ds_test = ds[1]
                print(f"✅ Dataset loaded successfully!")
                print(f"📊 Train samples: {len(ds_train)}")
                print(f"📊 Test samples: {len(ds_test)}")
                
                # Save samples as CSV
                self._save_samples(ds_train, f"{dataset_name}_train", download_path)
                self._save_samples(ds_test, f"{dataset_name}_test", download_path)
                
            else:
                ds = tfds.load(dataset_name, split=split, as_supervised=True)
                print(f"✅ Dataset loaded successfully!")
                print(f"📊 Samples: {len(ds)}")
                
                # Save samples as CSV
                self._save_samples(ds, dataset_name, download_path)
            
            return True
            
        except Exception as e:
            print(f"❌ Error downloading dataset: {e}")
            print("💡 Try a different dataset or split")
            return False
    
    def _save_samples(self, dataset, name, path, max_samples=1000):
        """
        Helper to save dataset samples as CSV
        
        Args:
            dataset: TensorFlow dataset
            name (str): Name for the output file
            path (str): Directory to save
            max_samples (int): Maximum samples to save
        """
        try:
            data = []
            for idx, (features, labels) in enumerate(dataset.take(max_samples)):
                # Convert features to flat structure
                if hasattr(features, 'numpy'):
                    features = features.numpy()
                if hasattr(labels, 'numpy'):
                    labels = labels.numpy()
                
                row = {'label': labels}
                if isinstance(features, np.ndarray):
                    # Flatten array data
                    flat_features = features.flatten()
                    for i, val in enumerate(flat_features[:20]):  # Limit columns
                        row[f'feature_{i}'] = val
                else:
                    row['features'] = str(features)
                
                data.append(row)
            
            if data:
                df = pd.DataFrame(data)
                filename = f"{name.replace('/', '_')}.csv"
                filepath = os.path.join(path, filename)
                df.to_csv(filepath, index=False)
                print(f"💾 Saved {len(data)} samples to: {filepath}")
                print(f"📋 Columns: {', '.join(df.columns[:5])}{'...' if len(df.columns) > 5 else ''}")
        
        except Exception as e:
            print(f"⚠️  Could not save as CSV: {e}")
    
    def list_popular_datasets(self):
        """List popular TensorFlow datasets"""
        popular = [
            "mnist",          # Handwritten digits
            "cifar10",        # Image classification
            "cifar100",       # Image classification (100 classes)
            "imdb_reviews",   # Sentiment analysis
            "iris",           # Classic tabular
            "caltech101",     # Object recognition
            "oxford_iiit_pet", # Pet images
            "cats_vs_dogs",   # Binary classification
            "fashion_mnist",  # Fashion items
            "wikitext",       # Text data
        ]
        
        print("\n🌟 Popular TensorFlow Datasets:")
        print("-" * 60)
        for idx, ds in enumerate(popular, 1):
            print(f"  {idx}. {ds}")
        print("\n💡 Some datasets are large. Use 'split=train' for testing.")

def main():
    """Main execution function"""
    print("=" * 60)
    print("📊 TENSORFLOW DATASETS FETCHER")
    print("=" * 60)
    print()
    
    fetcher = TensorFlowDatasetFetcher()
    fetcher.list_popular_datasets()
    
    print("\n" + "=" * 60)
    
    search_term = input("\nEnter search term (press Enter for 'iris'): ").strip()
    if not search_term:
        search_term = "iris"
    
    datasets = fetcher.search_datasets(search_term, max_results=5)
    
    if datasets:
        print("=" * 60)
        choice = input(f"Download dataset {datasets[0]}? (y/n): ").strip().lower()
        
        if choice == 'y':
            fetcher.download_dataset(datasets[0])
        else:
            print("\n💡 To download a specific dataset, use:")
            print(f"  fetcher.download_dataset('{datasets[0]}')")
    # script_tensorflow_native.py - TFDS without TensorFlow
# Platform #9: TensorFlow Datasets

import tensorflow_datasets as tfds
import os
import pandas as pd
import numpy as np

class TensorFlowDatasetFetcher:
    """Complete implementation for TensorFlow Datasets"""
    
    def __init__(self):
        print("🔐 Initializing TensorFlow Datasets (no TensorFlow required)...")
        print("✅ Ready!\n")
    
    def search_datasets(self, search_term=None, max_results=5):
        print(f"🔍 Searching for datasets containing: '{search_term}'")
        print("-" * 60)
        
        try:
            all_datasets = tfds.list_builders()
            
            if search_term:
                filtered = [ds for ds in all_datasets if search_term.lower() in ds.lower()]
            else:
                filtered = all_datasets
            
            if len(filtered) > max_results:
                filtered = filtered[:max_results]
            
            if not filtered:
                print("❌ No datasets found")
                print("\n💡 Try: 'mnist', 'cifar10', 'iris'")
                return []
            
            print(f"\n📊 Found {len(filtered)} datasets:\n")
            for idx, ds_name in enumerate(filtered, 1):
                print(f"  {idx}. {ds_name}")
            return filtered
            
        except Exception as e:
            print(f"❌ Error searching datasets: {e}")
            return []
    
    def download_dataset(self, dataset_name, split='train', download_path="./datasets/tensorflow/"):
        print(f"\n⬇️ Downloading dataset: {dataset_name}")
        print("-" * 60)
        
        try:
            os.makedirs(download_path, exist_ok=True)
            print(f"🔄 Loading dataset (this may take a moment)...")
            
            # Load without TensorFlow
            ds = tfds.load(dataset_name, split=split, as_supervised=True, try_gcs=True)
            
            print(f"✅ Dataset loaded successfully!")
            self._save_samples(ds, dataset_name, download_path)
            return True
            
        except Exception as e:
            print(f"❌ Error downloading dataset: {e}")
            return False
    
    def _save_samples(self, dataset, name, path, max_samples=100):
        try:
            data = []
            for idx, (features, labels) in enumerate(dataset.take(max_samples)):
                if hasattr(features, 'numpy'):
                    features = features.numpy()
                if hasattr(labels, 'numpy'):
                    labels = labels.numpy()
                
                row = {'label': labels}
                if isinstance(features, np.ndarray):
                    flat_features = features.flatten()
                    for i, val in enumerate(flat_features[:20]):
                        row[f'feature_{i}'] = val
                else:
                    row['features'] = str(features)
                data.append(row)
            
            if data:
                df = pd.DataFrame(data)
                filename = f"{name.replace('/', '_')}.csv"
                filepath = os.path.join(path, filename)
                df.to_csv(filepath, index=False)
                print(f"💾 Saved {len(data)} samples to: {filepath}")
        
        except Exception as e:
            print(f"⚠️  Could not save as CSV: {e}")
    
    def list_popular_datasets(self):
        popular = ["mnist", "cifar10", "imdb_reviews", "iris", "fashion_mnist"]
        print("\n🌟 Popular TensorFlow Datasets:")
        for idx, ds in enumerate(popular, 1):
            print(f"  {idx}. {ds}")

def main():
    print("=" * 60)
    print("📊 TENSORFLOW DATASETS FETCHER")
    print("=" * 60)
    print()
    
    fetcher = TensorFlowDatasetFetcher()
    fetcher.list_popular_datasets()
    
    print("\n" + "=" * 60)
    search_term = input("\nEnter search term (press Enter for 'iris'): ").strip()
    if not search_term:
        search_term = "iris"
    
    datasets = fetcher.search_datasets(search_term, max_results=5)
    
    if datasets:
        choice = input(f"Download dataset {datasets[0]}? (y/n): ").strip().lower()
        if choice == 'y':
            fetcher.download_dataset(datasets[0])
    
    print("\n✨ Done!")

if __name__ == "__main__":
    main()
    print("\n✨ Done!")

if __name__ == "__main__":
    main()