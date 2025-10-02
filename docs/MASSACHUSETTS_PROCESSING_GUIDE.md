# Massachusetts License Plate Processing Guide

## Overview
Massachusetts is a **plate type state** with variable processing types based on code numbers. Massachusetts uses 24+ different code numbers to identify specific plate types, each with unique processing rules.

**Last Updated:** October 1, 2025  
**Total Plate Types:** 178  
**Unique Processing Types:** 21  
**Code Numbers Used:** 24+

---

## Critical Global Rules

### 1. Emergency Vehicle Rule
**REJECT images of Marked Emergency Vehicles for:**
- Code 61 (Ambulance)
- Code 62 (Authority Motorcycle)
- Code 63 (Authority)
- Code 72 (State Motorcycle)
- Use "Emergency Vehicle" reject code

### 2. Stacked Characters Rule
**Different handling by code:**
- **Code 32 (Commercial):** KEY all stacked characters
- **Code 66 (Livery):** KEY stacked "LV"
- **Code 72 (State Motorcycle):** OMIT stacked "STATE"
- **Code 73 (State Police):** OMIT stacked "STATE"

### 3. Slanted Characters Rule
**Code 63 (Authority):** If 4 or more slanted characters present, **KEY ONLY THE FIRST 3**

### 4. Omit Letter "T" Rule
**Code 63 (Authority):** DO NOT KEY the letter "T" on left side of plate

### 5. Omit Stickers Rule
- **Code 82 (Dealer):** DO NOT KEY "D" - it is a decal sticker
- **Code 84 (Repair):** DO NOT KEY "R" - it is a decal sticker

### 6. Special Text Omission
**Code 46 (Passenger Vehicle):**
- DO NOT INCLUDE "EX POW"
- DO NOT INCLUDE "US CONGRESS"

### 7. Lightning Bolt Rule
**Code 46 (Passenger Vehicle):** Replace Lightning Bolt symbol with **FORWARD SLASH "/"**

---

## Processing Types by Code Number

### Code 31: Apportioned
**Dropdown:** Apportioned  
**Processing:** All characters must be keyed  
**Visual ID:** "APPORTIONED" on bottom of plate

```
Example: ABC123
Key in: ABC123
```

---

### Code 32: Commercial
**Dropdown:** Commercial  
**Processing:** **All stacked characters MUST BE KEYED**  
**Visual ID:** "COMMERCIAL" on bottom of plate

**Character Handling:**
```
Plate shows: 123
             ABC (stacked)
Key in: 123ABC (KEY ALL stacked)
```

---

### Code 35: Handicapped
**Dropdown:** Handicapped  
**Processing:** All characters must be keyed  
**Visual ID:** Wheelchair symbol on LEFT side of plate

---

### Code 45: Motorcycle
**Dropdown:** Motorcycle  
**Processing:** All characters must be keyed  
**Visual ID:** Smaller plate, ONLY on motorcycles

---

### Code 46: Passenger Vehicle (Default)
**Dropdown:** Passenger Vehicle  
**Processing:** All characters must be keyed with special rules  
**Note:** All veteran/military plates except standard Veteran fall under Passenger Vehicle

**Special Rules:**
1. **DO NOT INCLUDE "EX POW"** - Omit this text
2. **DO NOT INCLUDE "US CONGRESS"** - Omit this text
3. **Lightning Bolt → Forward Slash** - Replace ⚡ with /

**Character Handling:**
```
Plate shows: ⚡ABC123
Key in: /ABC123

Plate shows: ABC123 EX POW
Key in: ABC123 (OMIT "EX POW")

Plate shows: ABC123 US CONGRESS
Key in: ABC123 (OMIT "US CONGRESS")
```

---

### Code 50: Regular Veteran
**Dropdown:** Regular Veteran  
**Processing:** All characters must be keyed  
**Visual ID:** "VETERAN" on bottom of plate  
**Note:** All other Veteran/Military plates fall under Passenger Vehicle (Code 46)

---

### Code 61: Ambulance
**Dropdown:** Ambulance  
**Processing:** All characters must be keyed  
**Visual ID:** "AMBULANCE" on bottom of plate  
**⚠️ REJECT RULE:** REJECT if vehicle is a Marked Emergency Vehicle

---

### Code 62: Authority Motorcycle
**Dropdown:** Authority Motorcycle  
**Processing:** All characters must be keyed  
**Visual ID:** Smaller motorcycle plate  
**⚠️ REJECT RULE:** REJECT if vehicle is a Marked Emergency Vehicle

**Note:** Code 62 defined but not in current inventory

---

### Code 63: Authority (Complex Rules)
**Dropdown:** Authority  
**Processing:** Multiple special rules apply  
**Visual ID:** Up to 6 slanted characters on left, "T" may appear on left

**Complex Character Handling:**

**Rule 1: Omit Letter "T"**
```
Plate shows: T 3142
Key in: 3142 (OMIT "T")
```

**Rule 2: Limit Slanted Characters**
```
If 4+ slanted characters: KEY ONLY FIRST 3

Plate shows: POL5564 (6 slanted chars on left)
Key in: POL5564 (Keep first 3: POL, plus rest)

Example format: MA-POL5564
```

**⚠️ REJECT RULE:** REJECT if vehicle is a Marked Emergency Vehicle

**Code 63 Includes:** ATTA, BAT, BRTA, CATA, CCR, FRTA, GMTA, and 13+ other transit authorities

---

### Code 64: Bus
**Dropdown:** Bus  
**Processing:** All characters must be keyed  
**Visual ID:** "BUS" on bottom of plate

---

### Code 65: Camper
**Dropdown:** Camper  
**Processing:** **KEY ALL CHARACTERS displayed**  
**Visual ID:** "CAMPER" on bottom of plate

**Character Handling:**
```
Plate shows: 7682D
Key in: 7682D (KEY ALL including D suffix)
```

---

### Code 66: Livery
**Dropdown:** Livery  
**Processing:** **Stacked "LV" IS KEYED**  
**Visual ID:** "LIVERY" on bottom, stacked LV on left

**Character Handling:**
```
Plate shows: LV (stacked on left)
             64993
Key in: LV64993 (INCLUDE stacked LV)
```

---

### Code 67: Municipal
**Dropdown:** Municipal  
**Processing:** All characters MUST BE KEYED  
**Visual ID:** "OFFICIAL" on bottom of plate

---

### Code 69: School Bus
**Dropdown:** School Bus  
**Processing:** All characters must be keyed  
**Visual ID:** "SCHOOL BUS" on bottom of plate

**Note:** Code 69 defined but not in current inventory

---

### Code 70: Bus Pupil
**Dropdown:** Bus Pupil  
**Processing:** All characters must be keyed  
**Visual ID:** "PUPILS" on bottom of plate

**Note:** Code 70 defined but not in current inventory

---

### Code 71: Semi Trailer
**Dropdown:** Semi Trailer  
**Processing:** All characters must be keyed  
**Visual ID:** "SEMI-TRAILER" on bottom of plate

---

### Code 72: State Motorcycle
**Dropdown:** State Motorcycle  
**Processing:** **Stacked "STATE" IS NOT KEYED**  
**Visual ID:** Smaller motorcycle plate, STATE stacked on left  
**⚠️ REJECT RULE:** REJECT if vehicle is a Marked Emergency Vehicle

**Character Handling:**
```
Plate shows: STATE (stacked on left)
             12345
Key in: 12345 (OMIT stacked STATE)
```

---

### Code 73: State Police
**Dropdown:** State Police  
**Processing:** **Stacked "STATE" IS NOT KEYED**  
**Visual ID:** STATE stacked/slanted on left side

**Character Handling:**
```
Plate shows: STATE (stacked/slanted on left)
             POL123
Key in: POL123 (OMIT stacked STATE)
```

---

### Code 74: Taxi
**Dropdown:** Taxi  
**Processing:** All characters must be keyed  
**Visual ID:** "TAXI" on bottom of plate

---

### Code 75: Trailer
**Dropdown:** Trailer  
**Processing:** All characters must be keyed  
**Visual ID:** "TRAILER" on bottom of plate

---

### Code 76: Vanpool
**Dropdown:** Vanpool  
**Processing:** All characters must be keyed  
**Visual ID:** "VANPOOL" stacked/slanted on left side

---

### Code 80: Antique
**Dropdown:** Antique  
**Processing:** All characters must be keyed  
**Visual ID:** "ANTIQUE" on bottom of plate

---

### Code 82: Dealer
**Dropdown:** Dealer  
**Processing:** **DO NOT KEY "D" sticker**  
**Visual ID:** "DEALER" on bottom, D sticker on left

**Character Handling:**
```
Plate shows: D (decal sticker)
             8382A
Key in: 8382A (OMIT "D" sticker)
```

---

### Code 84: Repair
**Dropdown:** Repair  
**Processing:** **DO NOT KEY "R" sticker**  
**Visual ID:** "REPAIR" on bottom, R sticker on left

**Character Handling:**
```
Plate shows: R (decal sticker)
             336A
Key in: 336A (OMIT "R" sticker)
```

---

## Processing Decision Tree

```
START
│
├─ Is plate on Marked Emergency Vehicle?
│  └─ YES → Check code: 61, 62, 63, or 72? → REJECT IMAGE
│
├─ Does plate have "D" or "R" sticker on left?
│  ├─ "D" sticker → Code 82 → OMIT sticker
│  └─ "R" sticker → Code 84 → OMIT sticker
│
├─ Does plate have letter "T" on left? (Code 63)
│  └─ YES → OMIT "T"
│
├─ Does plate have 4+ slanted characters? (Code 63)
│  └─ YES → KEY ONLY FIRST 3 slanted characters
│
├─ Does plate have stacked "STATE"? (Codes 72, 73)
│  └─ YES → OMIT stacked STATE
│
├─ Does plate have stacked "LV"? (Code 66)
│  └─ YES → INCLUDE stacked LV
│
├─ Does plate have stacked characters on Commercial? (Code 32)
│  └─ YES → KEY ALL stacked characters
│
├─ Does plate show "EX POW" or "US CONGRESS"? (Code 46)
│  └─ YES → OMIT this text
│
├─ Does plate show Lightning Bolt? (Code 46)
│  └─ YES → Replace with Forward Slash "/"
│
├─ What is the code number?
│  ├─ 31 → Apportioned
│  ├─ 32 → Commercial (KEY stacked)
│  ├─ 35 → Handicapped
│  ├─ 45 → Motorcycle
│  ├─ 46 → Passenger Vehicle (special rules)
│  ├─ 50 → Regular Veteran
│  ├─ 61 → Ambulance (check emergency)
│  ├─ 62 → Authority Motorcycle (check emergency)
│  ├─ 63 → Authority (OMIT T, limit slanted)
│  ├─ 64 → Bus
│  ├─ 65 → Camper (KEY ALL)
│  ├─ 66 → Livery (INCLUDE LV)
│  ├─ 67 → Municipal
│  ├─ 69 → School Bus
│  ├─ 70 → Bus Pupil
│  ├─ 71 → Semi Trailer
│  ├─ 72 → State Motorcycle (OMIT STATE)
│  ├─ 73 → State Police (OMIT STATE)
│  ├─ 74 → Taxi
│  ├─ 75 → Trailer
│  ├─ 76 → Vanpool
│  ├─ 80 → Antique
│  ├─ 82 → Dealer (OMIT D)
│  ├─ 84 → Repair (OMIT R)
│  └─ Unknown → Default to Passenger Vehicle (46)
│
└─ Key all remaining characters
```

---

## Character Handling Summary

### ✅ KEY ALL CHARACTERS
**Most plates** - Codes: 31, 35, 45, 46 (with special rules), 50, 61, 64, 67, 69, 70, 71, 74, 75, 76, 80

### ✅ KEY STACKED CHARACTERS
- **Code 32 (Commercial):** KEY all stacked characters
- **Code 66 (Livery):** KEY stacked "LV"

### ❌ OMIT CHARACTERS
- **Code 63 (Authority):** OMIT letter "T" on left
- **Code 72 (State Motorcycle):** OMIT stacked "STATE"
- **Code 73 (State Police):** OMIT stacked "STATE"
- **Code 82 (Dealer):** OMIT "D" decal sticker
- **Code 84 (Repair):** OMIT "R" decal sticker

### ❌ OMIT TEXT
- **Code 46 (Passenger):** OMIT "EX POW"
- **Code 46 (Passenger):** OMIT "US CONGRESS"

### 🔢 LIMIT CHARACTERS
- **Code 63 (Authority):** If 4+ slanted chars, KEY ONLY FIRST 3

### ⚡ REPLACE SYMBOLS
- **Code 46 (Passenger):** Lightning Bolt → Forward Slash "/"

### 🚫 REJECT RULES
- **Codes 61, 62, 63, 72:** REJECT if Marked Emergency Vehicle

---

## Common Patterns

### Transit Authority Plates (Code 63)
**20 different authorities include:**
- ATTA, BAT, BRTA, CATA, CCR, FRTA, GMTA
- LRTA, MART, MVTA, MWRT, NRT, PVTA, SRTA
- VTA, WRA, WRTA
- Emergency Vehicle, Transit Authority, Transit Police, Turnpike

**All follow Code 63 rules:**
- OMIT "T" on left
- KEY ONLY FIRST 3 if 4+ slanted
- REJECT if marked emergency

### Passenger Vehicle Specialty Plates (Code 46)
**57 different specialty plates** including:
- Sports teams (Bruins, Celtics, Patriots, Red Sox)
- Universities and colleges
- Charitable organizations
- Environmental/conservation themes
- Regional/cultural themes

**All follow Code 46 rules:**
- OMIT "EX POW"
- OMIT "US CONGRESS"
- Lightning Bolt → "/"

---

## Tips for Accurate Processing

1. **Check for emergency vehicles first** - Codes 61, 62, 63, 72 must be rejected if marked

2. **Look for decal stickers** - "D" and "R" stickers are NOT keyed (codes 82, 84)

3. **Count slanted characters** - Code 63: If 4+, key only first 3

4. **Watch for letter "T"** - Code 63: OMIT "T" on left side

5. **Check for stacked text:**
   - Commercial (32): KEY stacked
   - Livery (66): KEY stacked LV
   - State plates (72, 73): OMIT stacked STATE

6. **Special passenger rules** - OMIT "EX POW" and "US CONGRESS", replace ⚡ with /

7. **When in doubt**, default to Passenger Vehicle (Code 46)

---

## Validation Checklist

- [ ] Identified code number correctly
- [ ] Selected correct dropdown
- [ ] Checked for marked emergency vehicle
- [ ] Applied correct character handling (OMIT/INCLUDE/LIMIT)
- [ ] Omitted decal stickers if present (D, R)
- [ ] Omitted "T" for authority plates
- [ ] Limited slanted characters if 4+ present
- [ ] Omitted/included stacked text correctly
- [ ] Applied passenger vehicle special rules
- [ ] Replaced lightning bolt with forward slash
- [ ] Keyed all other characters

---

## Statistics

- **Total Plate Types:** 178
- **Passenger Vehicle (Code 46):** 57 specialty variants (124 total with defaults)
- **Authority (Code 63):** 20 transit authority variants
- **Regular Veteran (Code 50):** 6 variants
- **Most Complex:** Code 63 (Authority) - Multiple conditional rules
- **Processing Coverage:** 100%

---

**Document Version:** 1.0  
**Last Updated:** October 1, 2025  
**Maintained by:** DOT Processing Team
