"""
Script to remove weather_inclusion field from all JSON files
"""

import json
import re
from pathlib import Path


def remove_weather_inclusion_from_file(file_path):
    """Remove weather_inclusion field from a JSON file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Count occurrences before
        before_count = content.count('"weather_inclusion"')
        
        if before_count == 0:
            return 0, 0  # No changes needed
        
        # Remove lines containing "weather_inclusion": value,
        # Pattern handles both with and without trailing comma
        pattern = r'\s*"weather_inclusion":\s*(?:true|false|null),?\s*\n'
        content_modified = re.sub(pattern, '', content)
        
        # Also handle case where it's the last field (no comma after)
        pattern2 = r',\s*\n\s*"weather_inclusion":\s*(?:true|false|null)\s*\n'
        content_modified = re.sub(pattern2, '\n', content_modified)
        
        # Count after
        after_count = content_modified.count('"weather_inclusion"')
        
        if after_count == 0 and before_count > 0:
            # Write back
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content_modified)
            print(f"✅ {file_path.name}: Removed {before_count} occurrences")
            return before_count, 0
        else:
            print(f"⚠️  {file_path.name}: Could not remove all ({before_count} -> {after_count})")
            return before_count, after_count
            
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return 0, 0


def main():
    """Main execution"""
    base_dir = Path(__file__).parent.parent
    data_dir = base_dir / 'data'
    
    # Process all JSON files in states and templates directories
    directories = [
        data_dir / 'states',
        data_dir / 'templates'
    ]
    
    total_removed = 0
    total_files = 0
    
    for directory in directories:
        if not directory.exists():
            print(f"⚠️  Directory not found: {directory}")
            continue
        
        print(f"\n📁 Processing {directory.name}...")
        json_files = list(directory.glob('*.json'))
        
        for json_file in json_files:
            before, after = remove_weather_inclusion_from_file(json_file)
            if before > 0:
                total_removed += (before - after)
                total_files += 1
    
    print(f"\n" + "=" * 60)
    print(f"✅ Complete!")
    print(f"   Files modified: {total_files}")
    print(f"   Total removals: {total_removed}")
    print("=" * 60)


if __name__ == "__main__":
    main()
