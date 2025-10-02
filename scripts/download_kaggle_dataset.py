"""
Download and integrate Kaggle US License Plates dataset.
Dataset: mexwell/us-license-plates
"""

import os
from pathlib import Path

def download_kaggle_dataset():
    """Download the US License Plates dataset from Kaggle."""
    
    print("=" * 80)
    print("KAGGLE DATASET DOWNLOADER - US LICENSE PLATES")
    print("=" * 80)
    
    # Check if kagglehub is installed
    try:
        import kagglehub
        print("✅ kagglehub module found")
    except ImportError:
        print("❌ kagglehub not installed")
        print("\nTo install, run:")
        print("  pip install kagglehub")
        return None
    
    # Check for Kaggle credentials
    kaggle_json = Path.home() / ".kaggle" / "kaggle.json"
    if not kaggle_json.exists():
        print("\n⚠️  WARNING: Kaggle credentials not found!")
        print("\nTo authenticate with Kaggle:")
        print("1. Go to https://www.kaggle.com/settings/account")
        print("2. Scroll to 'API' section")
        print("3. Click 'Create New Token'")
        print("4. Save kaggle.json to:", kaggle_json.parent)
        print("\nOr set environment variables:")
        print("  KAGGLE_USERNAME=your_username")
        print("  KAGGLE_KEY=your_key")
        return None
    
    print(f"✅ Kaggle credentials found: {kaggle_json}")
    
    # Download dataset
    try:
        print("\n📥 Downloading dataset: mexwell/us-license-plates")
        print("This may take a few minutes depending on dataset size...")
        
        path = kagglehub.dataset_download("mexwell/us-license-plates")
        
        print(f"\n✅ Dataset downloaded successfully!")
        print(f"📁 Path to dataset files: {path}")
        
        # List files in the downloaded dataset
        dataset_path = Path(path)
        if dataset_path.exists():
            print("\n📂 Dataset contents:")
            for item in sorted(dataset_path.rglob("*")):
                if item.is_file():
                    size_mb = item.stat().st_size / (1024 * 1024)
                    print(f"   {item.relative_to(dataset_path)} ({size_mb:.2f} MB)")
        
        return path
        
    except Exception as e:
        print(f"\n❌ Error downloading dataset: {e}")
        return None

def explore_dataset(dataset_path):
    """Explore the dataset structure and contents."""
    if not dataset_path:
        return
    
    path = Path(dataset_path)
    
    print("\n" + "=" * 80)
    print("DATASET EXPLORATION")
    print("=" * 80)
    
    # Look for common file types
    images = list(path.rglob("*.jpg")) + list(path.rglob("*.png")) + list(path.rglob("*.jpeg"))
    csvs = list(path.rglob("*.csv"))
    jsons = list(path.rglob("*.json"))
    txts = list(path.rglob("*.txt"))
    
    print(f"\n📊 File Summary:")
    print(f"   Images: {len(images)}")
    print(f"   CSV files: {len(csvs)}")
    print(f"   JSON files: {len(jsons)}")
    print(f"   Text files: {len(txts)}")
    
    if csvs:
        print(f"\n📄 CSV Files found:")
        for csv in csvs:
            print(f"   {csv.name}")
    
    if jsons:
        print(f"\n📄 JSON Files found:")
        for json_file in jsons:
            print(f"   {json_file.name}")
    
    # Check for state-organized structure
    state_dirs = [d for d in path.iterdir() if d.is_dir()]
    if state_dirs:
        print(f"\n📁 Directories found: {len(state_dirs)}")
        for d in sorted(state_dirs)[:10]:  # Show first 10
            file_count = len(list(d.rglob("*.*")))
            print(f"   {d.name}: {file_count} files")
        if len(state_dirs) > 10:
            print(f"   ... and {len(state_dirs) - 10} more")

def suggest_integration_plan(dataset_path):
    """Suggest how to integrate this dataset into the project."""
    if not dataset_path:
        return
    
    print("\n" + "=" * 80)
    print("INTEGRATION RECOMMENDATIONS")
    print("=" * 80)
    
    print("\n📋 Suggested next steps:")
    print("\n1. ANALYZE DATASET STRUCTURE")
    print("   - Check if images are organized by state")
    print("   - Identify naming conventions")
    print("   - Look for metadata files (CSV/JSON)")
    
    print("\n2. CREATE IMAGE ORGANIZER")
    print("   - Script to copy/move images to data/images/STATE/")
    print("   - Match plate types to existing JSON files")
    print("   - Update image paths in JSONs")
    
    print("\n3. EXTRACT METADATA")
    print("   - Parse any CSV/JSON files for plate info")
    print("   - Cross-reference with existing data")
    print("   - Update plate_characteristics fields")
    
    print("\n4. UPDATE JSON FILES")
    print("   - Add image paths to 'images' field")
    print("   - Update plate_sample paths")
    print("   - Validate all references")
    
    print("\n💡 Would you like me to create:")
    print("   A) Dataset analyzer script")
    print("   B) Image import/organizer tool")
    print("   C) Metadata extraction script")
    print("   D) All of the above")

if __name__ == "__main__":
    dataset_path = download_kaggle_dataset()
    
    if dataset_path:
        explore_dataset(dataset_path)
        suggest_integration_plan(dataset_path)
    
    print("\n" + "=" * 80)
    print("COMPLETE")
    print("=" * 80)
