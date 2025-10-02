# Indiana License Plate Processing Guide

## Overview
Indiana is a **plate type state** with variable processing types based on code numbers. Indiana uses 24+ different code numbers to identify specific plate types, each with unique processing rules.

**Last Updated:** October 1, 2025  
**Total Plate Types:** 278  
**Unique Processing Types:** 22  
**Code Numbers Used:** 24+

---

## Critical Global Rules

### 1. Prefix/Suffix Rule
**All Indiana license plates have either a prefix or suffix.**
- Prefixes and suffixes can be:
  - Single, double, or triple alpha: `A`, `AA`, `AAA`
  - Single, double, or triple numeric: `1`, `11`, `111`
- Example: `K366360` (prefix K, followed by 6 digits)

### 2. Zero vs. Letter "O" Rule
**Indiana allows BOTH the number zero "0" and the letter "O".**
- The font is different for zero vs. letter O
- Carefully distinguish between the two characters
- Both are valid and can appear on plates

### 3. Emergency Vehicle Rule
**REJECT images of Marked Emergency Vehicles for:**
- Code 61 (Ambulance)
- Code 62 (Authority Motorcycle)
- Code 63 (Authority)
- Use "Emergency Vehicle" reject code

### 4. Customized Registration Note
Tags may have customized registrations that are not standard issue. When in doubt, **USE INITIAL PASSENGER DROPDOWN** for personalized plates.

---

## Processing Types by Code Number

### Code 27: Support Our Troops
**Dropdown:** Support our Troops  
**Processing:** All characters must be keyed  
**Visual ID:** Ribbon on left of plate, "Support Our Troops" text  
**Example:** `ST248`, `AA9999`

---

### Code 30: National Guard
**Dropdown:** National Guard  
**Processing:** All characters must be keyed  
**Visual ID:** Militiaman logo, registration starts with "NG"

---

### Code 31: Apportioned (Commercial)
**Dropdown:** Apportioned  
**Processing:** All characters must be keyed  
**Visual ID:** "APP" appears in UPPER LEFT CORNER  
**Note:** Plate contains numeric characters only  
**Weight Class:** Greater than 10,000 lbs  
**Variations:** 20 different company-branded apportioned plates

---

### Code 34: Disabled Veteran
**Dropdown:** Disabled Veteran  
**Processing:** **OMIT "DAV"** if displayed on older plates  
**Visual ID:** "DISABLED HOOSIER VETERAN" on bottom of plate  
**Branch Variants:**
- Merchant Marine
- Army, Navy, Coast Guard
- Marine, Air Force

**Character Handling:**
```
Plate shows: DAV123
Key in: 123
```

---

### Code 35: Disabled/Handicapped
**Dropdown:** Handicapped  
**Processing:** All characters must be keyed  
**Visual ID:** Wheelchair symbol on LEFT side of plate  
**Includes:** Standard and motorcycle variants

---

### Code 42: Initial Passenger (Personalized)
**Dropdown:** Initial Passenger  
**Processing:** All characters must be keyed  
**Note:** This plate type is **ALWAYS** customized/personalized  
**Use Case:** When passenger plate is personalized

---

### Code 43: Initial Veteran Motorcycle (Personalized)
**Dropdown:** Initial Veteran Motorcycle  
**Processing:** All characters must be keyed  
**Visual ID:** "Veteran" on plate, smaller motorcycle size  
**Note:** This plate type is **ALWAYS** customized/personalized

---

### Code 45: Motorcycle
**Dropdown:** Motorcycle  
**Processing:** All characters must be keyed  
**Visual ID:** "M CYCLE" on BOTTOM of plate  
**Size:** Smaller plate (motorcycle size)  
**Variants:** Standard, Historic, Native American, Specialty

---

### Code 46: Passenger Vehicle (Default)
**Dropdown:** Passenger Vehicle  
**Processing:** All characters must be keyed  
**Note:** All plates NOT previously mentioned are Passenger Vehicles  
**Count:** 114 different specialty passenger plates  
**Examples:** Collegiate plates, charitable organizations, specialty themes

**This is the default category** for any plate that doesn't fit other codes.

---

### Code 47: Dealer (New)
**Dropdown:** Dealer  
**Processing:** All characters must be keyed  
**Visual ID:** "DEALER NEW" on BOTTOM of plate  
**Note:** Plate contains a letter

---

### Code 48: Used Car Dealer
**Dropdown:** Used Car Dealer  
**Processing:** All characters must be keyed  
**Visual ID:** "DEALER USED" on BOTTOM of plate

---

### Code 49: Veteran Motorcycle
**Dropdown:** Veteran Motorcycle  
**Processing:** All characters must be keyed  
**Visual ID:** "M CYCLE" on BOTTOM, veteran identifier visible  
**Size:** Smaller motorcycle plate

---

### Code 50: Regular Veteran
**Dropdown:** Regular Veteran  
**Processing:** All characters must be keyed  
**Visual ID:** "VETERAN" appears on plate  
**Branch Variants:**
- Army Veteran
- Navy Veteran
- Air Force Veteran
- Marine Corps Veteran
- Coast Guard Veteran

---

### Code 61: Ambulance
**Dropdown:** Ambulance  
**Processing:** All characters must be keyed  
**Visual ID:** Ambulance vehicle type  
**⚠️ REJECT RULE:** REJECT if vehicle is a Marked Emergency Vehicle

---

### Code 62: Authority Motorcycle
**Dropdown:** Authority Motorcycle  
**Processing:** All characters must be keyed  
**Size:** Smaller motorcycle plate  
**⚠️ REJECT RULE:** REJECT if vehicle is a Marked Emergency Vehicle

---

### Code 63: Authority
**Dropdown:** Authority  
**Processing:** All characters must be keyed  
**⚠️ REJECT RULE:** REJECT if vehicle is a Marked Emergency Vehicle

---

### Code 64: Bus
**Dropdown:** Bus  
**Processing:** **OMIT stacked "BUS"**  
**Visual ID:** "BUS" appears on BOTTOM or LEFT of plate (vertical)  
**Vehicle Type:** Bus

**Character Handling:**
```
Plate shows: BUS 12345 (BUS is stacked vertically on left)
Key in: 12345
```

---

### Code 65: Camper/RV
**Dropdown:** Camper/RV  
**Processing:** **INCLUDE "RV"** - must be keyed  
**Visual ID:** "RV" on LEFT of plate  
**Vehicle Type:** RV, Camper, or Motorhome

**Character Handling:**
```
Plate shows: RV 12345
Key in: RV12345 (RV IS KEYED)
```

---

### Code 67: Municipal
**Dropdown:** Municipal  
**Processing:** All characters must be keyed  
**Visual ID:** "Municipal" across bottom of plate

---

### Code 68: Municipal Motorcycle
**Dropdown:** Municipal Motorcycle  
**Processing:** All characters must be keyed  
**Size:** Smaller motorcycle plate  
**Note:** Use **AUTHORITY MOTORCYCLE DROPDOWN** if needed

---

### Code 69: School Bus
**Dropdown:** School Bus  
**Processing:** **OMIT "BUS"**  
**Visual ID:** "BUS" on BOTTOM or LEFT of plate  
**Vehicle Type:** School Bus

**Character Handling:**
```
Plate shows: BUS 12345
Key in: 12345
```

---

### Code 70: School Bus (Pupil)
**Dropdown:** School Bus(Pupil)  
**Processing:** **OMIT "BUS"**  
**Visual ID:** "PUPILS" appears on tag line  
**Vehicle Type:** School Bus

---

### Code 71: Semi-Trailer
**Dropdown:** Semi-Trailer  
**Processing:** **OMIT "TRAILER" and OMIT stacked letters**  
**Visual ID:** "SEMI-TRAILER", "SEMI", or "Trailer" on BOTTOM/SIDE  
**Vehicle Type:** Semi-Trailer  
**Weight Class:** Greater than 10,000 lbs  
**Variations:** 18 different permanent trailer plates (some with company branding)

**Character Handling:**
```
Plate shows: 12345 TRAILER (with TRAILER stacked on right)
Key in: 12345

Plate shows: P12345 TRAILER
Key in: P12345 (for permanent trailers starting with P)
```

**Special Notes:**
- Permanent Trailer plates may display "PERM" in top left corner
- Company-branded trailers: Omit company name and "TRAILER" text
- Vertical "TRAILER" on right side is NOT keyed

---

### Code 72: State Motorcycle
**Dropdown:** State Motorcycle  
**Processing:** All characters must be keyed  
**Visual ID:** Black star on LEFT of plate  
**Vehicle Type:** Motorcycle  
**Variants:** Representative, Senator, US Senator

---

### Code 73: State Vehicle
**Dropdown:** State Vehicle  
**Processing:** All characters must be keyed  
**Visual ID:** Star symbol on LEFT, official title on BOTTOM  
**Bottom Text Examples:**
- "State Representative"
- "State Senator"
- "U.S. Senator"

**Note:** More current plates will display the official title clearly on bottom.

---

### Code 77: Semi-Tractor
**Dropdown:** Semi-Tractor  
**Processing:** All characters must be keyed  
**Visual ID:** "SEMI TRACTOR", "TRUCK", or "MINI TRUCK" on BOTTOM  
**Vehicle Type:** Truck  
**Weight Class:** Greater than 11,000 lbs  
**Registration:** May begin with "TC"

---

### Code 79: Truck (≤10,000 lbs)
**Dropdown:** Truck  
**Processing:** **OMIT stacked letters**  
**Visual ID:** "TRAILER/TRUCK" and weight class on BOTTOM  
**Vehicle Type:** Truck or Trailer  
**Weight Class:** Less than or equal to 10,000 lbs  
**Registration:** Usually begins with "TK"

**Character Handling:**
```
Plate shows: TK12345 (with stacked letters on side)
Key in: TK12345
```

---

### Code 88: Purple Heart
**Dropdown:** Purple Heart  
**Processing:** All characters must be keyed  
**Visual ID:** "PURPLE HEART" on BOTTOM, symbol on LEFT  
**Registration:** Newer plates begin with "PH"  
**Variants:** May include wheelchair logo for disabled Purple Heart recipients

---

## Processing Decision Tree

```
START
│
├─ Is plate on Marked Emergency Vehicle?
│  └─ YES → Check code: 61, 62, or 63? → REJECT IMAGE
│
├─ Does plate show stacked "BUS" or "TRAILER"?
│  ├─ YES → Code 64, 69, 70, 71, or 79? → OMIT stacked text
│  └─ NO → Continue
│
├─ Does plate show "RV" on left?
│  └─ YES → Code 65 → INCLUDE "RV" in registration
│
├─ Does older plate show small "DAV"?
│  └─ YES → Code 34 → OMIT "DAV"
│
├─ Is plate personalized/customized?
│  ├─ YES → Check for veteran motorcycle → Code 43
│  ├─ YES → Otherwise → Code 42
│  └─ NO → Continue
│
├─ What is the code number?
│  ├─ 27 → Support Our Troops
│  ├─ 30 → National Guard
│  ├─ 31 → Apportioned (APP in corner)
│  ├─ 34 → Disabled Veteran (OMIT DAV)
│  ├─ 35 → Handicapped (wheelchair symbol)
│  ├─ 45 → Motorcycle (M CYCLE on bottom)
│  ├─ 46 → Passenger Vehicle (default)
│  ├─ 47 → Dealer New
│  ├─ 48 → Used Car Dealer
│  ├─ 49 → Veteran Motorcycle
│  ├─ 50 → Regular Veteran
│  ├─ 61 → Ambulance
│  ├─ 64 → Bus (OMIT stacked BUS)
│  ├─ 65 → RV (INCLUDE RV)
│  ├─ 67 → Municipal
│  ├─ 68 → Municipal Motorcycle
│  ├─ 71 → Semi-Trailer (OMIT TRAILER)
│  ├─ 72 → State Motorcycle
│  ├─ 73 → State Vehicle
│  ├─ 77 → Semi-Tractor
│  ├─ 79 → Truck ≤10K lbs (OMIT stacked)
│  ├─ 88 → Purple Heart
│  └─ Unknown → Default to Passenger Vehicle (46)
│
└─ Key all visible characters (except OMIT rules above)
```

---

## Character Handling Summary

### ✅ KEY ALL CHARACTERS
**Most plates** - Codes: 27, 30, 31, 35, 42, 43, 45, 46, 47, 48, 49, 50, 67, 68, 72, 73, 77, 88

### ❌ OMIT CHARACTERS
- **Code 34:** OMIT "DAV" on older Disabled Veteran plates
- **Code 64:** OMIT stacked "BUS" on Bus plates
- **Code 69:** OMIT "BUS" on School Bus plates
- **Code 70:** OMIT "BUS" on School Bus Pupil plates
- **Code 71:** OMIT "TRAILER" and stacked letters on Semi-Trailer plates
- **Code 79:** OMIT stacked letters on Truck plates

### ➕ INCLUDE CHARACTERS
- **Code 65:** INCLUDE "RV" on Camper/RV plates (RV must be keyed)

### 🚫 REJECT RULES
- **Codes 61, 62, 63:** REJECT if vehicle is a Marked Emergency Vehicle

---

## Common Patterns

### Passenger Vehicle Prefix/Suffix Patterns
```
Single alpha prefix:    K366360
Double alpha prefix:    AA12345
Triple alpha prefix:    AAA1234
Single numeric suffix:  12345A
Double numeric suffix:  1234AA
Triple numeric suffix:  123AAA
```

### Apportioned Plates
```
APP in upper left:      APP 123456
Numeric only:           12345
Company branded:        [Company Logo] 12345
```

### Motorcycle Plates
```
Standard:               123M (M CYCLE on bottom)
Veteran:                VET123M (M CYCLE + veteran ID)
State:                  12★M (star on left)
Municipal:              MUN123M
```

### Commercial Vehicles
```
Semi-Tractor:           TC12345 (SEMI TRACTOR on bottom)
Semi-Trailer:           12345 (TRAILER text omitted)
Truck ≤10K:             TK12345 (stacked letters omitted)
```

---

## Tips for Accurate Processing

1. **Always check the code number first** - This determines the processing type
2. **Look for visual identifiers:**
   - APP in corner = Apportioned
   - Wheelchair symbol = Handicapped
   - M CYCLE on bottom = Motorcycle
   - Star on left = State vehicle
   - BUS/TRAILER text = Commercial vehicle

3. **Remember the font difference** between zero "0" and letter "O"

4. **For personalized plates**, use Initial Passenger (42) or Initial Veteran Motorcycle (43)

5. **When in doubt**, default to Passenger Vehicle (Code 46)

6. **Check vehicle type** - Helps confirm correct plate category

7. **Watch for stacked text** - Usually needs to be omitted (except RV)

8. **Emergency vehicles** - Codes 61, 62, 63 should be rejected if marked emergency vehicle

---

## Validation Checklist

- [ ] Identified code number correctly
- [ ] Selected correct dropdown from processing type
- [ ] Applied correct character handling rule (OMIT/INCLUDE)
- [ ] Distinguished between zero "0" and letter "O"
- [ ] Checked for emergency vehicle (codes 61, 62, 63)
- [ ] Omitted stacked text where applicable
- [ ] Included all required characters
- [ ] Verified prefix/suffix format
- [ ] Confirmed vehicle type matches plate type

---

## Statistics

- **Total Plate Types:** 278
- **Passenger Vehicle (Code 46):** 114 specialty variants
- **Apportioned (Code 31):** 20 company variants
- **Semi-Trailer (Code 71):** 18 permanent trailer variants
- **State Officials (Code 73):** 6 variants
- **Veterans (Codes 34, 49, 50):** 9 total variants
- **Motorcycle Types (Codes 43, 45, 49, 68, 72):** 10 total variants
- **Commercial Vehicles (Codes 31, 71, 77, 79):** 42+ variants

---

**Document Version:** 1.0  
**Last Updated:** October 1, 2025  
**Maintained by:** DOT Processing Team
