# script_github.py - GitHub Datasets Fetcher (FIXED)
# Platform #7: GitHub Datasets

from github import Github
import os
import pandas as pd
import requests
import json
import time

class GitHubDatasetFetcher:
    """Complete implementation for GitHub dataset operations"""
    
    def __init__(self):
        """Initialize GitHub fetcher"""
        print("🔐 Initializing GitHub Datasets...")
        print("⚠️  Note: Using GitHub Search API (rate limited)")
        print("✅ Ready!\n")
        
        # Initialize without authentication (rate limited)
        try:
            self.g = Github()
            print("📡 Connected to GitHub API (unauthenticated)")
            print("   Rate limit: 60 requests/hour")
        except Exception as e:
            print(f"⚠️  Error connecting to GitHub: {e}")
            self.g = None
    
    def search_datasets(self, search_term, max_results=5):
        """
        Search for datasets on GitHub
        
        Args:
            search_term (str): Keyword to search for
            max_results (int): Number of results to display
        
        Returns:
            list: List of repositories with dataset potential
        """
        print(f"🔍 Searching for datasets containing: '{search_term}'")
        print("-" * 60)
        
        if not self.g:
            print("❌ GitHub API not available")
            return []
        
        try:
            # Search for repositories with dataset keywords
            query = f"{search_term} dataset"
            print(f"📡 Searching GitHub repositories...")
            
            # Search repositories
            repositories = self.g.search_repositories(query)
            
            # Limit results
            results = []
            for repo in repositories[:max_results]:
                results.append({
                    'name': repo.full_name,
                    'description': repo.description[:100] if repo.description else 'No description',
                    'url': repo.html_url,
                    'stars': repo.stargazers_count,
                    'language': repo.language,
                    'datasets_likely': True
                })
            
            if not results:
                print("❌ No repositories found")
                print("💡 Try using the web interface at:")
                print("   https://github.com/search?q=dataset")
                return []
            
            print(f"\n📊 Found {len(results)} repositories:\n")
            for idx, repo in enumerate(results, 1):
                print(f"  {idx}. {repo['name']}")
                print(f"     Description: {repo['description'][:80] + '...' if repo['description'] and len(repo['description']) > 80 else repo['description']}")
                print(f"     Stars: {repo['stars']} | Language: {repo['language']}")
                print(f"     URL: {repo['url']}")
                print()
            
            return results
            
        except Exception as e:
            print(f"❌ Error searching GitHub: {e}")
            print("💡 Tip: Try using the web interface at:")
            print("   https://github.com/search?q=dataset")
            return []
    
    def download_dataset(self, repo_name, download_path="./datasets/github/"):
        """
        Download dataset files from a GitHub repository
        
        Args:
            repo_name (str): Repository name (e.g., 'owner/repo')
            download_path (str): Directory to save the dataset
        
        Returns:
            bool: True if successful, False otherwise
        """
        print(f"\n⬇️ Processing repository: {repo_name}")
        print("-" * 60)
        
        try:
            os.makedirs(download_path, exist_ok=True)
            
            # Get repository contents via GitHub API
            api_url = f"https://api.github.com/repos/{repo_name}/contents"
            headers = {'Accept': 'application/vnd.github.v3+json'}
            
            print(f"🌐 Fetching repository contents...")
            response = requests.get(api_url, headers=headers)
            
            if response.status_code != 200:
                print(f"❌ Failed to fetch repository: {response.status_code}")
                print("💡 Try downloading manually from the GitHub page")
                return False
            
            contents = response.json()
            
            # Find dataset files
            dataset_files = []
            extensions = ['.csv', '.json', '.xlsx', '.tsv', '.txt', '.data']
            
            for item in contents:
                if item['type'] == 'file':
                    # Check if it's a dataset file
                    is_dataset = any(ext in item['name'].lower() for ext in extensions)
                    if is_dataset:
                        dataset_files.append(item)
            
            if not dataset_files:
                print("❌ No dataset files found in the repository root")
                print("💡 Some repositories store data in subdirectories")
                print("   Try the web interface for manual download")
                return False
            
            # Download first dataset file
            selected = dataset_files[0]
            download_url = selected['download_url']
            
            print(f"🔄 Downloading: {selected['name']}")
            
            file_response = requests.get(download_url)
            file_response.raise_for_status()
            
            # Save file
            filepath = os.path.join(download_path, selected['name'])
            with open(filepath, 'wb') as f:
                f.write(file_response.content)
            
            print(f"✅ Dataset saved to: {filepath}")
            
            # Try to read if CSV
            if selected['name'].endswith('.csv'):
                try:
                    df = pd.read_csv(filepath)
                    print(f"📊 Shape: {df.shape[0]} rows, {df.shape[1]} columns")
                    print(f"📋 Columns: {', '.join(df.columns[:5])}{'...' if len(df.columns) > 5 else ''}")
                except:
                    pass
            
            return True
            
        except Exception as e:
            print(f"❌ Error downloading dataset: {e}")
            return False
    
    def list_popular_datasets(self):
        """List repositories known for datasets"""
        popular = [
            {"name": "awesomedata/awesome-public-datasets", "desc": "Curated list of public datasets"},
            {"name": "microsoft/ML-For-Beginners", "desc": "Machine Learning datasets"},
            {"name": "fivethirtyeight/data", "desc": "FiveThirtyEight datasets"},
            {"name": "datasets/awesome", "desc": "Awesome datasets repository"},
            {"name": "jakevdp/data", "desc": "Sample datasets"},
        ]
        
        print("\n🌟 Popular GitHub Datasets Repositories:")
        print("-" * 60)
        for item in popular:
            print(f"  {item['name']}")
            print(f"     {item['desc']}")

def main():
    """Main execution function"""
    print("=" * 60)
    print("📊 GITHUB DATASETS FETCHER")
    print("=" * 60)
    print()
    
    fetcher = GitHubDatasetFetcher()
    fetcher.list_popular_datasets()
    
    print("\n" + "=" * 60)
    
    search_term = input("\nEnter search term (press Enter for 'covid'): ").strip()
    if not search_term:
        search_term = "covid"
    
    results = fetcher.search_datasets(search_term, max_results=5)
    
    if results:
        print("=" * 60)
        choice = input(f"Download repository {results[0]['name']}? (y/n): ").strip().lower()
        
        if choice == 'y':
            fetcher.download_dataset(results[0]['name'])
        else:
            print("\n💡 To download a specific repository, use:")
            print(f"  fetcher.download_dataset('{results[0]['name']}')")
    
    print("\n✨ Done!")

if __name__ == "__main__":
    main()