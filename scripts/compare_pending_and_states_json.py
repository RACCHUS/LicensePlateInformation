import os
import json
from difflib import unified_diff

PENDING_DIR = os.path.join('data', 'pending')
STATES_DIR = os.path.join('data', 'states')

# Fields to compare/synchronize
PENDING_FIELDS = [
    ('character_rules', 'uses_zero_for_o'),
    ('character_rules', 'special_notes'),
    ('stacked_character_rules', 'omit'),
    ('stacked_character_rules', 'include'),
]
STATES_FIELDS = [
    'uses_zero_for_o',
    'allows_letter_o',
    'notes',
]

def load_json(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {path}: {e}")
        return None

def get_state_filename(state_name, folder):
    # Normalize state name for filename
    name = state_name.lower().replace(' ', '_')
    return os.path.join(folder, f"{name}.json")

def compare_fields(pending, states, state_name):
    results = []
    # Compare uses_zero_for_o
    pending_val = pending.get('character_rules', {}).get('uses_zero_for_o')
    states_val = states.get('uses_zero_for_o')
    if pending_val is not None and states_val is not None and pending_val != states_val:
        results.append(f"Mismatch in uses_zero_for_o for {state_name}: pending={pending_val}, states={states_val}")
    # Compare allows_letter_o
    allows_o = states.get('allows_letter_o')
    if allows_o is not None:
        if pending_val is not None and allows_o == pending_val:
            results.append(f"Possible mismatch in allows_letter_o for {state_name}: pending uses_zero_for_o={pending_val}, states allows_letter_o={allows_o}")
    # Compare notes/special_notes
    pending_notes = pending.get('character_rules', {}).get('special_notes')
    states_notes = states.get('notes')
    if pending_notes and states_notes and str(pending_notes) not in str(states_notes):
        results.append(f"Notes differ for {state_name}")
    return results

def main():
    pending_files = [f for f in os.listdir(PENDING_DIR) if f.endswith('.json')]
    states_files = [f for f in os.listdir(STATES_DIR) if f.endswith('.json')]
    for pf in pending_files:
        pending_path = os.path.join(PENDING_DIR, pf)
        pending_json = load_json(pending_path)
        if not pending_json:
            continue
        # Handle if pending_json is a list (not a dict)
        state_name = None
        if isinstance(pending_json, list):
            # Try to find a dict with 'state' key
            for entry in pending_json:
                if isinstance(entry, dict) and 'state' in entry:
                    state_name = entry['state']
                    pending_json = entry
                    break
            if not state_name:
                print(f"Could not find state in list for {pf}")
                continue
        elif isinstance(pending_json, dict):
            state_name = pending_json.get('state')
            if not state_name:
                continue
        else:
            print(f"Unknown JSON structure in {pf}")
            continue
        states_path = get_state_filename(state_name, STATES_DIR)
        if not os.path.exists(states_path):
            print(f"No states JSON for {state_name}")
            continue
        states_json = load_json(states_path)
        if not states_json:
            continue
        results = compare_fields(pending_json, states_json, state_name)
        if results:
            print(f"--- {state_name} ---")
            for r in results:
                print(r)

if __name__ == '__main__':
    main()
