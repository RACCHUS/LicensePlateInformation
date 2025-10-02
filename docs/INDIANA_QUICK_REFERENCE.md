# Indiana License Plate Quick Reference

## 🔍 Quick ID Guide

### Visual Identifiers

| Visual Element | Code | Type | Action |
|---|---|---|---|
| **APP** in upper left corner | 31 | Apportioned | Key all |
| **Wheelchair** symbol | 35 | Handicapped | Key all |
| **M CYCLE** on bottom | 45/49 | Motorcycle | Key all |
| **BUS** stacked on side | 64/69/70 | Bus/School Bus | **OMIT BUS** |
| **RV** on left | 65 | Camper/RV | **INCLUDE RV** |
| **TRAILER** stacked | 71 | Semi-Trailer | **OMIT TRAILER** |
| **Star** ★ on left | 72/73 | State Vehicle | Key all |
| **DEALER NEW** on bottom | 47 | Dealer New | Key all |
| **DEALER USED** on bottom | 48 | Dealer Used | Key all |
| **VETERAN** on plate | 50 | Regular Veteran | Key all |
| **PURPLE HEART** on bottom | 88 | Purple Heart | Key all |

---

## ⚡ Processing Rules at a Glance

### KEY ALL CHARACTERS ✅
**27, 30, 31, 35, 42, 43, 45, 46, 47, 48, 49, 50, 67, 68, 72, 73, 77, 88**

### OMIT CHARACTERS ❌
| Code | Type | Omit |
|---|---|---|
| 34 | Disabled Veteran | OMIT "DAV" on older plates |
| 64 | Bus | OMIT stacked "BUS" |
| 69 | School Bus | OMIT "BUS" |
| 70 | School Bus Pupil | OMIT "BUS" |
| 71 | Semi-Trailer | OMIT "TRAILER" & stacked letters |
| 79 | Truck ≤10K | OMIT stacked letters |

### INCLUDE CHARACTERS ➕
| Code | Type | Include |
|---|---|---|
| 65 | Camper/RV | **INCLUDE "RV"** (must be keyed) |

### REJECT IMAGES 🚫
| Code | Type | Reject When |
|---|---|---|
| 61 | Ambulance | Marked Emergency Vehicle |
| 62 | Authority Motorcycle | Marked Emergency Vehicle |
| 63 | Authority | Marked Emergency Vehicle |

---

## 🎯 Code Number Cheat Sheet

```
27 = Support Our Troops       (key all)
30 = National Guard            (key all)
31 = Apportioned              (key all - APP in corner)
34 = Disabled Veteran          (OMIT DAV)
35 = Handicapped              (key all - wheelchair symbol)

42 = Initial Passenger         (personalized)
43 = Initial Veteran MC        (personalized motorcycle)
45 = Motorcycle               (key all - M CYCLE)
46 = PASSENGER VEHICLE        (DEFAULT - key all)
47 = Dealer New               (key all)
48 = Dealer Used              (key all)
49 = Veteran Motorcycle        (key all)
50 = Regular Veteran           (key all)

61 = Ambulance                (REJECT if emergency)
62 = Authority Motorcycle      (REJECT if emergency)
63 = Authority                (REJECT if emergency)
64 = Bus                      (OMIT BUS)
65 = Camper/RV                (INCLUDE RV)
67 = Municipal                (key all)
68 = Municipal Motorcycle      (key all)
69 = School Bus               (OMIT BUS)
70 = School Bus Pupil         (OMIT BUS)
71 = Semi-Trailer             (OMIT TRAILER)
72 = State Motorcycle          (key all - star)
73 = State Vehicle             (key all - star)

77 = Semi-Tractor             (key all)
79 = Truck ≤10K lbs           (OMIT stacked)
88 = Purple Heart             (key all)
```

---

## 🚨 Critical Rules

### 1️⃣ Zero "0" vs. Letter "O"
- Indiana allows BOTH
- Font is different - look carefully
- Both are valid characters

### 2️⃣ Prefix/Suffix Required
- ALL Indiana plates have prefix OR suffix
- Can be: A, AA, AAA (alpha) or 1, 11, 111 (numeric)
- Example: `K366360` (K prefix)

### 3️⃣ Emergency Vehicle Rule
- Codes 61, 62, 63: **REJECT** if marked emergency vehicle
- Use "Emergency Vehicle" reject code

### 4️⃣ Personalized Plates
- Code 42: Initial Passenger (always personalized)
- Code 43: Initial Veteran Motorcycle (always personalized)
- When in doubt: Use Initial Passenger dropdown

### 5️⃣ Default Rule
- Unknown or unclear → Code 46 (Passenger Vehicle)
- 114 different specialty passenger plates exist

---

## 📋 Quick Decision Flow

```
1. Check for emergency vehicle (61, 62, 63) → REJECT if marked
   ↓
2. Look for stacked text (BUS/TRAILER) → OMIT if codes 64, 69, 70, 71, 79
   ↓
3. Look for "RV" on left (65) → INCLUDE RV
   ↓
4. Look for old "DAV" text (34) → OMIT DAV
   ↓
5. Is it personalized? → Use 42 or 43
   ↓
6. Identify code number → Use corresponding processing type
   ↓
7. Key all remaining characters
```

---

## 🔢 Character Handling Examples

### Bus (Code 64) - OMIT
```
Plate shows:  [BUS]     Visual: BUS stacked vertically on left
              12345
Key in:       12345     (OMIT BUS)
```

### RV (Code 65) - INCLUDE
```
Plate shows:  RV 12345  Visual: RV on left side
Key in:       RV12345   (INCLUDE RV)
```

### Semi-Trailer (Code 71) - OMIT
```
Plate shows:  12345     Visual: TRAILER stacked on right
              [TRLR]
Key in:       12345     (OMIT TRAILER)
```

### Disabled Veteran (Code 34) - OMIT
```
Plate shows:  123       Visual: Small "DAV" on older plate
              DAV
Key in:       123       (OMIT DAV on older plates)
```

### Passenger (Code 46) - KEY ALL
```
Plate shows:  K366360
Key in:       K366360   (Key everything)
```

---

## 💡 Pro Tips

✅ **Look for code number first** - Fastest way to identify type  
✅ **Check visual identifiers** - APP, wheelchair, M CYCLE, star, etc.  
✅ **Vehicle type confirms plate type** - Bus, RV, motorcycle, etc.  
✅ **Stacked text usually omitted** - Except RV (which is included)  
✅ **When uncertain** - Default to Passenger Vehicle (46)  
✅ **Font matters** - Zero vs. O look different  
✅ **All plates have prefix/suffix** - Single/double/triple alpha or numeric  

---

## 📊 Most Common Types

1. **Code 46: Passenger Vehicle** - 114 specialty variants (default)
2. **Code 31: Apportioned** - 20 commercial variants (APP in corner)
3. **Code 71: Semi-Trailer** - 18 permanent trailer variants (OMIT TRAILER)
4. **Code 73: State Vehicle** - 6 official variants (star symbol)
5. **Code 50: Regular Veteran** - 5 military branch variants

---

## ⚠️ Common Mistakes to Avoid

❌ Keying stacked "BUS" or "TRAILER" text  
❌ Omitting "RV" on camper plates (RV must be keyed!)  
❌ Confusing zero "0" with letter "O"  
❌ Processing emergency vehicles (61, 62, 63) - should reject  
❌ Keying old "DAV" text on disabled veteran plates  
❌ Missing prefix/suffix requirement  
❌ Not recognizing personalized plates (codes 42, 43)  

---

## 🎓 Training Scenarios

### Scenario 1: Apportioned Truck
- Visual: "APP" in upper left, numbers only, company logo
- Code: 31
- Action: Key all numbers
- Dropdown: Apportioned

### Scenario 2: School Bus
- Visual: Yellow bus, "BUS" stacked on left, plate shows "BUS 12345"
- Code: 69
- Action: Key only "12345" (OMIT BUS)
- Dropdown: School Bus

### Scenario 3: RV/Camper
- Visual: Motorhome, "RV" on left, plate shows "RV 12345"
- Code: 65
- Action: Key "RV12345" (INCLUDE RV)
- Dropdown: Camper/RV

### Scenario 4: Personalized Passenger
- Visual: Custom text like "HOOSIER" on standard passenger plate
- Code: 42
- Action: Key all characters
- Dropdown: Initial Passenger

### Scenario 5: Semi-Trailer
- Visual: Trailer, "TRAILER" stacked on right, plate shows "P12345"
- Code: 71
- Action: Key only "P12345" (OMIT TRAILER)
- Dropdown: Semi-Trailer

---

**Quick Reference Version:** 1.0  
**Last Updated:** October 1, 2025  
**Print this page for desk reference!**
