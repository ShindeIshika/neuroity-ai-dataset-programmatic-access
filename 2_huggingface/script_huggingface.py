# script_huggingface.py - Hugging Face Datasets Fetcher (Updated)
# Platform #2: Hugging Face Datasets

from datasets import load_dataset, get_dataset_config_names, get_dataset_split_names
import os
import pandas as pd

class HuggingFaceDatasetFetcher:
    """Complete implementation for Hugging Face dataset operations"""
    
    def __init__(self):
        """Initialize Hugging Face datasets"""
        print("🔐 Initializing Hugging Face Datasets...")
        print("✅ Ready!\n")
    
    def search_datasets(self, search_term, max_results=5):
        """
        Search for datasets by keyword using Hugging Face Hub API
        
        Args:
            search_term (str): Keyword to search for
            max_results (int): Number of results to display
        
        Returns:
            list: List of dataset names
        """
        print(f"🔍 Searching for datasets containing: '{search_term}'")
        print("-" * 60)
        
        try:
            # Use huggingface_hub to search
            from huggingface_hub import HfApi
            api = HfApi()
            
            # Search for datasets
            results = api.list_datasets(search=search_term, limit=max_results)
            
            datasets = []
            for dataset in results:
                datasets.append(dataset.id)
                print(f"  {len(datasets)}. {dataset.id}")
                print(f"     Downloads: {dataset.downloads if hasattr(dataset, 'downloads') else 'N/A'}")
                print()
            
            return datasets
            
        except ImportError:
            print("❌ huggingface_hub not installed. Installing...")
            import subprocess
            subprocess.check_call(['pip', 'install', 'huggingface_hub'])
            print("✅ Please run the script again.")
            return []
        except Exception as e:
            print(f"❌ Error searching datasets: {e}")
            return []
    
    def download_dataset(self, dataset_name, download_path="./datasets/huggingface/"):
        """
        Download a dataset
        
        Args:
            dataset_name (str): Name of the dataset (e.g., 'imdb')
            download_path (str): Directory to save the dataset
        
        Returns:
            bool: True if successful, False otherwise
        """
        print(f"\n⬇️ Downloading dataset: {dataset_name}")
        print("-" * 60)
        
        try:
            # Create directory if it doesn't exist
            os.makedirs(download_path, exist_ok=True)
            
            # Load dataset
            print(f"🔄 Loading dataset (this may take a moment)...")
            dataset = load_dataset(dataset_name, split="train", streaming=True)
            
            # Save first 100 examples as CSV
            output_file = os.path.join(download_path, f"{dataset_name.replace('/', '_')}.csv")
            print(f"💾 Saving to: {output_file}")
            
            # Convert to pandas and save
            df = pd.DataFrame(dataset.take(100))
            df.to_csv(output_file, index=False)
            
            print(f"✅ Dataset saved to: {output_file}")
            print(f"📊 Saved {len(df)} rows")
            print(f"📋 Columns: {', '.join(df.columns)}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error downloading dataset: {e}")
            print("💡 Tip: Try a simpler dataset like 'imdb' or 'sst2' first")
            return False
    
    def list_popular_datasets(self):
        """List popular Hugging Face datasets"""
        popular = [
            "imdb",           # Movie reviews (NLP)
            "sst2",           # Sentiment analysis
            "ag_news",        # News articles
            "yelp_polarity",  # Yelp reviews
            "amazon_polarity",# Amazon reviews
            "cnn_dailymail",  # Text summarization
            "wikitext",       # Wikipedia text
            "bookcorpus",     # Books
            "cifar10",        # Images
            "mnist",          # Handwritten digits
            "squad",          # Question answering
            "glue",           # General Language Understanding
        ]
        
        print("\n🌟 Popular Hugging Face Datasets:")
        print("-" * 60)
        for idx, dataset in enumerate(popular, 1):
            print(f"  {idx}. {dataset}")
        print("\n💡 Note: Some datasets may be large. Use 'streaming=True' for large datasets.")

def main():
    """Main execution function"""
    print("=" * 60)
    print("🤗 HUGGING FACE DATASET FETCHER")
    print("=" * 60)
    print()
    
    # Initialize the fetcher
    fetcher = HuggingFaceDatasetFetcher()
    
    # Show popular datasets
    fetcher.list_popular_datasets()
    
    print("\n" + "=" * 60)
    
    # Search for datasets
    search_term = input("\nEnter search term (press Enter for 'imdb'): ").strip()
    if not search_term:
        search_term = "imdb"
    
    datasets = fetcher.search_datasets(search_term, max_results=5)
    
    if datasets:
        print("\n" + "=" * 60)
        print("Dataset found! To download:")
        print(f"  - Use name: {datasets[0]}")
        
        choice = input(f"\nDownload {datasets[0]}? (y/n): ").strip().lower()
        
        if choice == 'y':
            fetcher.download_dataset(datasets[0])
        else:
            print("\n💡 Tip: To download a specific dataset, call:")
            print(f"  fetcher.download_dataset('imdb')")
    
    print("\n✨ Done!")

if __name__ == "__main__":
    main()