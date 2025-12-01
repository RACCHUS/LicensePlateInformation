
# State JSON Update Plan (Updated for data/states/)


This plan outlines how to update each state JSON file in `data/states/` based on your requirements.

**Before making any changes, always check if the information is already present. Only add or update fields if the information is missing or needs correction. Do not duplicate existing data.**

**For handling stacked characters:**
- Ensure all stacked characters referenced in documentation, restrictions, or notes are explicitly listed in the `stacked_characters.include` array for each state.

---


## Alabama (Yellowhammer State - Sweet Home Alabama)
- `allows_letter_o`: Should be `false` (Letter “O” NOT used)
- `uses_zero_for_o`: Should be `true` (Zero “0” used instead of “O”)
- `character_formatting.stacked_characters.omit`: Ensure `["200", "T"]` are present (OMIT these on left side)
- `character_formatting.stacked_characters.include`: Ensure all relevant stacked characters are listed, especially for Troy University and others
- `character_formatting.stacked_characters.position`/`notes`: Clarify stacked character rules and positions if not already clear
- `notes`: Add or update summary of all rules, including vertical/stacked instructions and omissions/inclusions


## Alaska (The Last Frontier)
- `notes`: Add or update with "Letter O with letters/Letter O on personalized plates/Zero 0 will be with numbers. O and 0 are visually distinct."


## Arizona (The Grand Canyon State)
- `notes`: Add or update with "Letter O used on personalized plates ONLY."
- `character_formatting.stacked_characters.include`: Ensure stacked characters are listed
- `character_formatting.stacked_characters.omit`: Add "ARK" (omit abbreviation) if not present


## Arkansas (The Natural State)
- `notes`: Add or update with "Letter O with letters/Letter O on personalized plates/Zero 0 will be with numbers. Has a three letter/three number format. Letter with stacked letters."
- `character_formatting.stacked_characters.include`: Ensure stacked characters are listed


## California (The Golden State)
- `notes`: Add or update with "Letter O with letters/Letter O on personalized plates/Zero 0 will be with numbers. Standard: a number/three letters/three numbers (#LLL###). Include the 'DP'. Include 'PP' in triangle. If tag exceeds 10 characters, omit the stacked left characters. Vertical/Diagonal. If exceeds 10 characters- OMIT the vertical letters at the front of plate."
- `character_formatting.stacked_characters.include`: Ensure "DP", "PP" (triangle), vertical/diagonal characters are listed
- `character_formatting.stacked_characters.omit`: If tag exceeds 10 characters, omit vertical/stacked left characters


## Colorado (The Centennial State)
- `notes`: Add or update with "Letter O with letters/Letter O on personalized plates/Zero 0 will be with numbers. Has a three letter/three number format or four letters/two numbers. Letter O’s and Number 0’s LOOK DIFFERENT. 'B' and '8' look similar. Vertical/Diagonal. Trailer Plates OMIT 'FLT'. Disabled Veteran Plates Omit 'DV'."
- `character_formatting.stacked_characters.omit`: Ensure "FLT", "DV" are present as appropriate
- `character_formatting.stacked_characters.include`: Ensure vertical/diagonal characters are listed


## Connecticut (The Constitution State)
- `character_formatting.stacked_characters.include`: Ensure stacked characters are listed


## Delaware (The First State)
- `notes`: Add or update with "Letter O with letters/Letter O on personalized plates/Zero 0 will be with numbers."
- `character_formatting.stacked_characters.include`: Ensure stacked characters are listed
- `character_formatting.stacked_characters.omit`: Add "DEL" abbreviation if not present

---


For each state, update the JSON file in `data/states/` as appropriate, following this mapping.
**Always check for existing information before making changes. Only add or update fields if necessary.**
