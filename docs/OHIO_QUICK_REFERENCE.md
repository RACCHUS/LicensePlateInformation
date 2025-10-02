# Ohio License Plate Processing - Quick Reference

## Character Rules (CRITICAL)

### ⚠️ ZERO RULE
**Zero (0) cannot be used alone.**
Zero (0) must be led by or followed by another number (1-9).

```
✅ Valid:   01, 10, 102, 203   (zero with other digits)
❌ Invalid: 0                  (zero alone)
```

### Duplicate Policy
- ✅ Standard/Personalized: **NO duplicates**
- ⚠️  Dealer plates: **CAN duplicate** standard plates (exception)

## Processing Types by Code

### Code 31: Apportioned 🚛
- **Dropdown:** "Apportioned"
- **Visual:** "APPORTIONED" on BOTTOM
- **No modifications**

### Code 35: Disabled/Handicapped ♿
- **Dropdown:** "Disabled/Handicapped Motorcycle"
- **Visual:** WHEELCHAIR SYMBOL on LEFT
- **Important:** Applies to **BOTH vehicles AND motorcycles**
- **No modifications**

### Code 45: Motorcycle 🏍️
- **Dropdown:** "Motorcycle"
- **Visual:** Smaller plate size
- **⚠️ OMIT stacked "VET"**
- **Note:** For both standard and veteran motorcycles
- **Example:** OH-04MOF (4th char is letter O)

### Code 47: Dealer 🚗
- **Dropdown:** "Dealer"
- **Visual:** "DEALER" on BOTTOM
- **⚠️ OMIT all small characters**

### Code 50: Combat Veteran 🎖️
- **Dropdown:** "Combat Veteran"
- **Visual:** "VETERAN/COMBAT VETERAN" on BOTTOM
- **May have:** Red wheelchair logo
- **Important:** Use for **ANY military plate** (vehicle OR motorcycle)
- **No modifications**
- **Note:** Decals and insignia may be visible

### Code 68: Municipal Motorcycle 👮‍♂️🏍️
- **Dropdown:** "Municipal Motorcycle"
- **Visual:** 
  - Smaller plate size
  - "Ohio" on bottom
  - **Starts with OSP**
- **Motorcycles ONLY**
- **No modifications**

### Code 75: Trailer 🚚
- **Dropdown:** "Trailer"
- **Visual:** "TRAILER" on BOTTOM
- **⚠️ OMIT company names**

### Code 77: Truck 🚛
- **Dropdown:** "Truck"
- **Visual:** "TRUCK" on BOTTOM
- **No modifications**

### Code 80: Historical Vehicle 🏍️
- **Dropdown:** "Historical Vehicle"
- **Visual:** "HISTORICAL" on TOP or BOTTOM
- **⚠️ OMIT vertical "OHIO"**
- **Motorcycles ONLY**

### Code 46: Passenger Vehicle 🚗
- **Dropdown:** "Passenger Vehicle"
- **Default:** Everything not covered above
- **No modifications**

## Decision Tree

```
Start
  │
  ├─ "APPORTIONED" on bottom? → Code 31
  │
  ├─ Wheelchair symbol? → Code 35 (vehicles OR motorcycles)
  │
  ├─ Motorcycle plate?
  │   ├─ Starts "OSP"? → Code 68 (Municipal)
  │   ├─ "HISTORICAL"? → Code 80 + omit vertical OHIO
  │   ├─ "VETERAN"? → Code 50 (Combat Veteran)
  │   └─ Standard? → Code 45 + omit stacked VET
  │
  ├─ "DEALER" on bottom? → Code 47 + omit small chars
  │
  ├─ "VETERAN/COMBAT VETERAN" on bottom? → Code 50 (all military)
  │
  ├─ "TRAILER" on bottom? → Code 75 + omit company names
  │
  ├─ "TRUCK" on bottom? → Code 77
  │
  └─ None of above? → Code 46 (Passenger)
```

## Character Modification Summary

| Code | Plate Type | Modification |
|------|------------|--------------|
| 45 | Motorcycle | **Omit stacked "VET"** |
| 47 | Dealer | **Omit all small characters** |
| 75 | Trailer | **Omit company names** |
| 80 | Historical | **Omit vertical "OHIO"** |
| All others | - | No modification |

## Common Mistakes to Avoid

❌ **Using zero (0) alone** (must be with another digit 1-9)
❌ **Omitting wheelchair plates on vehicles** (Code 35 is for BOTH)
❌ **Using separate codes for military motorcycles** (all military = Code 50)
❌ **Keying stacked "VET"** on motorcycles (omit it!)
❌ **Keying small characters** on dealer plates (omit them!)
❌ **Keying company names** on trailer plates (omit them!)
❌ **Keying vertical "OHIO"** on historical plates (omit it!)

## Quick Tips

✅ **Zero Rule:** 0 cannot be alone - must be 01, 10, 20, etc.
✅ **Code 35 = Both:** Wheelchair applies to vehicles AND motorcycles
✅ **Code 50 = All Military:** One code for all veteran/military plates
✅ **Bottom Text:** Most codes have identifier on plate bottom
✅ **Motorcycles Only:** Codes 45, 68, 80 are motorcycle-specific
✅ **When in Doubt:** Code 46 (Passenger Vehicle)

## Visual Identifier Guide

| Visual Cue | Code | Plate Type |
|------------|------|------------|
| "APPORTIONED" bottom | 31 | Apportioned |
| Wheelchair symbol | 35 | Disabled/Handicapped |
| Small plate size | 45/68/80 | Motorcycle types |
| "DEALER" bottom | 47 | Dealer |
| "VETERAN/COMBAT VETERAN" | 50 | Combat Veteran |
| "OSP" prefix | 68 | Municipal Motorcycle |
| "TRAILER" bottom | 75 | Trailer |
| "TRUCK" bottom | 77 | Truck |
| "HISTORICAL" | 80 | Historical Vehicle |
| No special marker | 46 | Passenger Vehicle |

## Validation Checklist

Before submitting:
- [ ] Verified zero (0) is not alone
- [ ] Checked for wheelchair symbol (Code 35)
- [ ] Identified bottom text (APPORTIONED, DEALER, VETERAN, TRAILER, TRUCK)
- [ ] Checked if motorcycle plate (Codes 45, 68, or 80)
- [ ] Omitted stacked "VET" if Code 45
- [ ] Omitted small characters if Code 47
- [ ] Omitted company names if Code 75
- [ ] Omitted vertical "OHIO" if Code 80
- [ ] Selected correct dropdown based on code

## Special Reminders

### Code 35 Important!
Even though dropdown says "Disabled/Handicapped **Motorcycle**", it applies to **BOTH** motorcycles AND automobiles. Don't be confused by the name!

### Code 50 Comprehensive
Use Code 50 for **ANY** military plate - doesn't matter if it's a vehicle or motorcycle, or what branch of service. All military = Code 50.

### Dealer Duplicates Exception
Only Dealer plates (Code 47) are allowed to have the same number as standard plates. This is the ONLY exception to Ohio's no-duplicates rule.

---

**Last Updated:** October 1, 2025
**Total Plate Types:** 531
**Processing Types:** 10 unique codes
**Status:** Production Ready ✅

For detailed documentation, see: `docs/OHIO_PROCESSING_GUIDE.md`
