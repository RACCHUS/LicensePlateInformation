"""
Quick test to verify font mappings are working correctly
Shows what actual system font each state gets mapped to
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from gui.components.font_display.character_font_panel import CharacterFontPanel
import json
import glob

def test_font_mappings():
    """Test font mapping for all states"""
    
    panel = CharacterFontPanel(None)
    
    state_files = sorted(glob.glob('data/states/*.json'))
    
    print("=" * 90)
    print("ACTUAL FONT MAPPINGS - What System Font Each State Uses")
    print("=" * 90)
    print()
    
    # Group by actual system font
    font_usage = {}
    
    for state_file in state_files:
        state_code = os.path.basename(state_file)[:-5].upper()
        state_name = os.path.basename(state_file)[:-5].replace('_', ' ').title()
        
        try:
            with open(state_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                font_desc = data.get('main_font', 'NOT SPECIFIED')
            
            # Get the actual system font that would be used
            system_font = panel._find_best_font(font_desc)
            font_key = f"{system_font[0]} ({system_font[1]}pt, {system_font[2]})"
            
            if font_key not in font_usage:
                font_usage[font_key] = []
            
            font_usage[font_key].append({
                'code': state_code,
                'name': state_name,
                'description': font_desc
            })
            
        except Exception as e:
            print(f"Error processing {state_file}: {e}")
    
    # Display grouped by system font
    for system_font, states in sorted(font_usage.items()):
        print(f"\n{system_font}")
        print("-" * 90)
        print(f"  {len(states)} states use this font:")
        print()
        
        for state in states:
            print(f"    {state['code']:6} - {state['name']:30} ← {state['description'][:50]}")
    
    print()
    print("=" * 90)
    print(f"\nSUMMARY:")
    print(f"  Total states:        {len(state_files)}")
    print(f"  System fonts used:   {len(font_usage)}")
    print("=" * 90)
    
    # Show which system fonts are used
    print("\nSystem fonts being used:")
    for font in sorted(font_usage.keys()):
        count = len(font_usage[font])
        print(f"  • {font:40} - {count:2} states")

if __name__ == '__main__':
    test_font_mappings()
