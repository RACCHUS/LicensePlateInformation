# Ohio License Plate Processing Documentation

## Overview
Ohio has been updated with comprehensive processing type information from the official CSV matrix and processing documentation. Ohio is a **PLATE TYPE STATE** with variable processing requirements based on plate type codes.

## Update Summary

### Files Modified
- **data/states/ohio.json** - Main state data file
  - Added 259 new plate types from CSV
  - Updated 259 plate types with processing rules
  - Total: 531 plate types

### Scripts Created
1. **scripts/update_ohio_from_csv.py** - Imports plate types from CSV matrix
2. **scripts/update_ohio_processing_types.py** - Applies detailed processing rules
3. **scripts/ohio_processing_report.py** - Generates comprehensive reports

## Global Processing Rules

### Character Restrictions
**Zero (0) cannot be used alone. Zero (0) must be led by or followed by another number (1-9).**

### Duplicate Policy
- Ohio **does not produce duplicate** standard or personalized license plates numbers
- Dealer Licensing **may assign** Dealer plates to new and used dealerships which **duplicate** standard or personalized issued license plates
- This is an exception to the no-duplicates rule

### Temporary Plates
- Ohio issues Temporary Plates

## Processing Types by Code Number

### Code 31: Apportioned
- **Processing Type:** `apportioned`
- **Dropdown Selection:** "Apportioned"
- **Visual Identifier:** "APPORTIONED" appears on BOTTOM of plate
- **Rules:** Select "Apportioned" Plate Type from drop-down

### Code 35: Disabled/Handicapped
- **Processing Type:** `disabled_handicapped`
- **Dropdown Selection:** "Disabled/Handicapped Motorcycle"
- **Visual Identifier:** WHEELCHAIR SYMBOL on LEFT side of plate
- **Special Note:** Applies to **both motorcycles AND automobiles**
- **Rules:** Select when wheelchair symbol is present

### Code 45: Motorcycle
- **Processing Type:** `motorcycle`
- **Dropdown Selection:** "Motorcycle"
- **Visual Identifier:** Smaller plate size
- **Character Modification:** **DO NOT KEY stacked "VET"**
- **Special Note:** These plates are on Motorcycles ONLY!
- **Rules:** "Motorcycle" will be selected for both Standard and Veteran motorcycles
- **Example:** Plate should be verified as OH-04MOF (FOURTH CHARACTER IS THE LETTER O)

### Code 47: Dealer
- **Processing Type:** `dealer`
- **Dropdown Selection:** "Dealer"
- **Visual Identifier:** "DEALER" appears on BOTTOM of plate
- **Character Modification:** **Smaller characters are NOT to be KEYED**
- **Rules:** Omit all small numbers for Ohio Dealer Plates

### Code 50: Combat Veteran
- **Processing Type:** `combat_veteran`
- **Dropdown Selection:** "Combat Veteran"
- **Visual Identifier:** "VETERAN/COMBAT VETERAN" appears on BOTTOM of plate
- **May have:** Red handicapped logo (wheelchair)
- **Special Note:** Use this plate type for **any military plate, whether a vehicle or motorcycle**
- **Decals:** Various decals and insignia may be seen on veteran plates
- **Rules:** Covers all military/veteran plates

### Code 68: Municipal Motorcycle
- **Processing Type:** `municipal_motorcycle`
- **Dropdown Selection:** "Municipal Motorcycle"
- **Visual Identifier:** 
  - Smaller plate size
  - "Ohio" appears across bottom of plate
  - **Starts with OSP**
- **Special Note:** These plates are on Motorcycles ONLY!

### Code 75: Trailer
- **Processing Type:** `trailer`
- **Dropdown Selection:** "Trailer"
- **Visual Identifier:** "TRAILER" appears on BOTTOM of plate
- **Character Modification:** **OMIT Company names when present**
- **Rules:** Select "Trailer" Plate Type from drop-down

### Code 77: Truck
- **Processing Type:** `truck`
- **Dropdown Selection:** "Truck"
- **Visual Identifier:** "TRUCK" appears on BOTTOM of plate
- **Rules:** Select "Truck" Plate Type from drop-down

### Code 80: Historical Vehicle
- **Processing Type:** `historical_vehicle`
- **Dropdown Selection:** "Historical Vehicle"
- **Visual Identifier:** "HISTORICAL" appears on TOP or BOTTOM of plate
- **Character Modification:** **OMIT Vertical OHIO when present**
- **Special Note:** These plates are on Motorcycles ONLY!

### Code 46: Passenger Vehicle
- **Processing Type:** `passenger_vehicle`
- **Dropdown Selection:** "Passenger Vehicle"
- **Rules:** Select "Passenger Vehicle" from drop-down
- **Note:** Used for all plates not covered by other codes

## Statistics

### Plate Type Counts
- **Total Plate Types:** 531
- **Currently Processed:** 272
- **Newly Added from CSV:** 259
- **Pending Custom Definition:** 0 ✅ (all updated)
- **With Images:** 272 (51.2%)

### Breakdown by Code
- **Code 31 (Apportioned):** 2 plate types
- **Code 35 (Handicapped):** 2 plate types
- **Code 45 (Motorcycle):** 10 plate types
- **Code 46 (Passenger):** 204 plate types
- **Code 47 (Dealer):** 2 plate types
- **Code 50 (Veteran):** 30 plate types
- **Code 68 (Municipal):** 1 plate type
- **Code 75 (Trailer):** 4 plate types
- **Code 77 (Truck):** 3 plate types
- **Code 80 (Historical):** 1 plate type
- **Code 0 (Legacy/Other):** 271 plate types

## Processing Workflow

### Step-by-Step Processing Guide

1. **Identify Visual Markers**
   - Look for "APPORTIONED" on bottom (Code 31)
   - Look for wheelchair symbol (Code 35)
   - Check plate size (motorcycles - Code 45, 68, or 80)
   - Look for "DEALER" on bottom (Code 47)
   - Look for "VETERAN/COMBAT VETERAN" on bottom (Code 50)
   - Look for "OSP" prefix on motorcycle (Code 68)
   - Look for "TRAILER" on bottom (Code 75)
   - Look for "TRUCK" on bottom (Code 77)
   - Look for "HISTORICAL" on top/bottom (Code 80)

2. **Determine Code Type**
   - If "APPORTIONED" → Code 31
   - If wheelchair symbol → Code 35 (vehicles OR motorcycles)
   - If motorcycle + standard → Code 45
   - If "DEALER" → Code 47
   - If "VETERAN/COMBAT VETERAN" → Code 50 (all military)
   - If motorcycle + OSP prefix → Code 68
   - If "TRAILER" → Code 75
   - If "TRUCK" → Code 77
   - If "HISTORICAL" → Code 80
   - Otherwise → Code 46 (Passenger)

3. **Apply Character Modifications**
   - Code 45: Omit stacked "VET"
   - Code 47: Omit all small characters
   - Code 75: Omit company names
   - Code 80: Omit vertical "OHIO"

4. **Verify Character Rules**
   - Zero (0) cannot be alone - must be with another digit 1-9

## Decision Tree

```
Start
  │
  ├─ "APPORTIONED" on bottom? → Code 31 (Apportioned)
  │
  ├─ Wheelchair symbol? → Code 35 (Disabled/Handicapped) - vehicles OR motorcycles
  │
  ├─ Motorcycle plate?
  │   ├─ Starts with "OSP"? → Code 68 (Municipal Motorcycle)
  │   ├─ Says "HISTORICAL"? → Code 80 (Historical) + omit vertical OHIO
  │   ├─ Says "VETERAN"? → Code 50 (Combat Veteran)
  │   └─ Standard? → Code 45 (Motorcycle) + omit stacked VET
  │
  ├─ "DEALER" on bottom? → Code 47 (Dealer) + omit small characters
  │
  ├─ "VETERAN/COMBAT VETERAN" on bottom? → Code 50 (Combat Veteran) - all military
  │
  ├─ "TRAILER" on bottom? → Code 75 (Trailer) + omit company names
  │
  ├─ "TRUCK" on bottom? → Code 77 (Truck)
  │
  └─ None of above? → Code 46 (Passenger Vehicle)
```

## Character Modification Summary

| Plate Type | Code | Modification Required |
|------------|------|----------------------|
| Motorcycle | 45 | **Omit stacked "VET"** |
| Dealer | 47 | **Omit all small characters** |
| Trailer | 75 | **Omit company names** |
| Historical | 80 | **Omit vertical "OHIO"** |
| All others | - | No modification |

## Key Takeaways

1. **Zero Rule Critical**: Zero (0) cannot appear alone - must be with another digit
2. **Code 35 for Both**: Wheelchair symbol applies to BOTH vehicles and motorcycles
3. **Code 50 Universal**: Combat Veteran code covers ALL military plates (vehicles and motorcycles)
4. **Code 46 Default**: Passenger Vehicle is the catch-all for everything not covered
5. **Dealer Duplicates OK**: Only Dealer plates (Code 47) can duplicate standard plates
6. **Character Omissions**: Several codes require omitting certain characters (VET, small chars, company names, OHIO)

## Special Notes

### Code 35 - Important!
Unlike some states, Ohio's Code 35 (Disabled/Handicapped) applies to **BOTH** motorcycles AND automobiles. The dropdown says "Disabled/Handicapped Motorcycle" but it covers both vehicle types.

### Code 50 - Comprehensive
Code 50 (Combat Veteran) is used for **ANY** military plate, whether vehicle or motorcycle. This simplifies processing - all military/veteran plates use the same code.

### Motorcycle Verification
Example given: OH-04MOF where the FOURTH CHARACTER IS THE LETTER O (not zero).

## Implementation Status

### ✅ Completed
- [x] Imported all 259 plate types from CSV matrix
- [x] Added processing metadata from CSV columns
- [x] Defined 10 distinct processing types
- [x] Updated global processing rules
- [x] Created comprehensive documentation

### 📋 Next Steps
1. Test processing logic with sample plate images
2. Validate against actual data processing requirements
3. Add images for newly added plate types (currently 51.2% coverage)
4. Create unit tests for each processing type
5. Document edge cases and exceptions

## Reference Files

### Source Documents
- `data/pending/Plate_Type_Matrix_Vs_Jun_25[1] (1)(Ohio).csv` - Official CSV matrix
- Processing documentation provided by user

### Generated Files
- `data/states/ohio.json` - Complete state data
- `scripts/update_ohio_from_csv.py` - CSV import script
- `scripts/update_ohio_processing_types.py` - Processing type update script
- `scripts/ohio_processing_report.py` - Report generator

## Contact & Support

For questions about Ohio processing:
1. Review this documentation
2. Check the official CSV matrix
3. Consult processing metadata in JSON file
4. Generate fresh report: `python scripts/ohio_processing_report.py`

---

**Last Updated:** October 1, 2025
**Status:** Complete ✅
**Plate Types:** 531
**Processing Types Defined:** 10
**Coverage:** All plate types have processing definitions
