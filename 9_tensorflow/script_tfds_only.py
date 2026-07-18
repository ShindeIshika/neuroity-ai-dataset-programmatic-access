# script_tfds_only.py - TFDS Without TensorFlow
# Platform #9: TensorFlow Datasets

import tensorflow_datasets as tfds
import os
import pandas as pd
import numpy as np

class TFDSFetcher:
    """Fetch datasets using only TFDS (no TensorFlow)"""
    
    def __init__(self):
        print("🔐 Initializing TFDS (without TensorFlow)...")
        print("✅ Ready!\n")
    
    def search_datasets(self, search_term=None, max_results=5):
        """Search for datasets"""
        print(f"🔍 Searching for: '{search_term}'")
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
                return []
            
            print(f"\n📊 Found {len(filtered)} datasets:\n")
            for idx, ds_name in enumerate(filtered, 1):
                try:
                    info = tfds.builder(ds_name).info
                    print(f"  {idx}. {ds_name}")
                    print(f"     Description: {info.description[:80] + '...' if len(info.description) > 80 else info.description}")
                    print(f"     Features: {len(info.features)}")
                except:
                    print(f"  {idx}. {ds_name}")
                print()
            
            return filtered
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return []
    
    def download_dataset(self, dataset_name, download_path="./datasets/tensorflow/"):
        """Download and save dataset samples"""
        print(f"\n⬇️ Downloading: {dataset_name}")
        print("-" * 60)
        
        try:
            os.makedirs(download_path, exist_ok=True)
            print(f"🔄 Loading dataset...")
            
            # Try to load with different splits
            try:
                ds = tfds.load(dataset_name, split='train', as_supervised=True, try_gcs=True)
            except:
                try:
                    ds = tfds.load(dataset_name, split='all', as_supervised=True, try_gcs=True)
                except:
                    ds = tfds.load(dataset_name, split='full', as_supervised=True, try_gcs=True)
            
            print(f"✅ Dataset loaded!")
            
            # Save samples
            data = []
            for idx, (features, labels) in enumerate(ds.take(100)):
                try:
                    if hasattr(features, 'numpy'):
                        features = features.numpy()
                    if hasattr(labels, 'numpy'):
                        labels = labels.numpy()
                    
                    row = {'label': labels}
                    
                    # Handle numpy arrays
                    if isinstance(features, np.ndarray):
                        flat = features.flatten()
                        for i, val in enumerate(flat[:20]):
                            row[f'feature_{i}'] = val
                    else:
                        row['features'] = str(features)
                    
                    data.append(row)
                except:
                    continue
            
            if data:
                df = pd.DataFrame(data)
                filename = f"{dataset_name.replace('/', '_')}.csv"
                filepath = os.path.join(download_path, filename)
                df.to_csv(filepath, index=False)
                print(f"💾 Saved {len(data)} samples to: {filepath}")
                print(f"📋 Columns: {', '.join(df.columns[:5])}{'...' if len(df.columns) > 5 else ''}")
            else:
                print("❌ Could not extract data samples")
            
            return True
            
        except Exception as e:
            print(f"❌ Error: {e}")
            print("💡 Try: 'iris', 'mnist', 'fashion_mnist'")
            return False
    
    def list_popular_datasets(self):
        """List popular datasets"""
        popular = ["iris", "mnist", "cifar10", "imdb_reviews", "fashion_mnist"]
        print("\n🌟 Popular TFDS Datasets:")
        for idx, ds in enumerate(popular, 1):
            print(f"  {idx}. {ds}")

def main():
    print("=" * 60)
    print("📊 TENSORFLOW DATASETS (TFDS Only)")
    print("=" * 60)
    print()
    
    fetcher = TFDSFetcher()
    fetcher.list_popular_datasets()
    
    print("\n" + "=" * 60)
    search_term = input("\nEnter search term (press Enter for 'iris'): ").strip()
    if not search_term:
        search_term = "iris"
    
    datasets = fetcher.search_datasets(search_term, max_results=3)
    
    if datasets:
        choice = input(f"\nDownload {datasets[0]}? (y/n): ").strip().lower()
        if choice == 'y':
            fetcher.download_dataset(datasets[0])
    
    print("\n✨ Done!")

if __name__ == "__main__":
    main()