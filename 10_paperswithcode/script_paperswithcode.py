# script_paperswithcode_web.py - Papers With Code Web Interface
# Platform #10: Papers With Code Datasets

import webbrowser
import os
import json

class PapersWithCodeFetcher:
    """Papers With Code using web interface"""
    
    def __init__(self):
        print("🔐 Initializing Papers With Code...")
        print("ℹ️  This is a dataset CATALOG - it provides links to datasets")
        print("⚠️  API may be rate-limited - using web interface")
        print("✅ Ready!\n")
    
    def search_datasets(self, search_term):
        """Open browser to search for datasets"""
        print(f"🔍 Searching for: '{search_term}'")
        print("-" * 60)
        
        url = f"https://paperswithcode.com/datasets?q={search_term.replace(' ', '+')}"
        print(f"🌐 Opening browser to: {url}")
        webbrowser.open(url)
        print("✅ Browser opened!")
        
        return [{'name': search_term, 'url': url}]
    
    def download_dataset(self, dataset_name, download_path="./datasets/paperswithcode/"):
        """Save dataset info (Papers With Code doesn't host files)"""
        print(f"\n📝 Saving info for: {dataset_name}")
        print("-" * 60)
        
        try:
            os.makedirs(download_path, exist_ok=True)
            
            info = {
                'name': dataset_name,
                'note': 'Papers With Code is a catalog - datasets are hosted elsewhere',
                'search_url': f"https://paperswithcode.com/datasets?q={dataset_name.replace(' ', '+')}"
            }
            
            json_file = os.path.join(download_path, f"{dataset_name.replace('/', '_')}_info.json")
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(info, f, indent=2)
            
            print(f"✅ Info saved to: {json_file}")
            print(f"\n📥 To download this dataset, visit:")
            print(f"   {info['search_url']}")
            
            # Open in browser
            webbrowser.open(info['search_url'])
            return True
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def list_popular_datasets(self):
        """List popular datasets"""
        popular = [
            "CIFAR-10", "ImageNet", "MNIST", "COCO",
            "SQuAD", "GLUE", "Fashion-MNIST", "IMDB"
        ]
        print("\n🌟 Popular Papers With Code Datasets:")
        print("-" * 60)
        for idx, ds in enumerate(popular, 1):
            print(f"  {idx}. {ds}")

def main():
    print("=" * 60)
    print("📊 PAPERS WITH CODE DATASETS")
    print("=" * 60)
    print()
    
    fetcher = PapersWithCodeFetcher()
    fetcher.list_popular_datasets()
    
    print("\n" + "=" * 60)
    print("ℹ️  Papers With Code is a CATALOG - it doesn't host files.")
    print("   It provides links to datasets hosted elsewhere.")
    
    search_term = input("\nEnter dataset name (press Enter for 'Fashion-MNIST'): ").strip()
    if not search_term:
        search_term = "Fashion-MNIST"
    
    fetcher.search_datasets(search_term)
    
    print("\n" + "=" * 60)
    choice = input(f"Save info for '{search_term}'? (y/n): ").strip().lower()
    if choice == 'y':
        fetcher.download_dataset(search_term)
    
    print("\n✨ Done!")

if __name__ == "__main__":
    main()