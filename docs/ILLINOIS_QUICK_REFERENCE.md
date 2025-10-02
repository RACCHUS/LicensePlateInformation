# Illinois License Plate Processing - Quick Reference

## Character Rules (CRITICAL)

### ⚠️ NO ALPHA-NUMERIC MIXING
Illinois **DOES NOT MIX** alpha and numeric characters together.
Applies to ALL plates including PERSONALIZED.

### Format Examples
```
✅ Passenger:      MARY 124    (letters SPACE numbers)
✅ Pickup:         124 MARY    (numbers SPACE letters)
✅ Personalized:   ABCDEF      (all alpha)
✅ Personalized:   123456      (all numeric)
❌ Invalid:        MA12RY      (mixed - NOT ALLOWED)
```

## Processing Types by Code

### Code 31: Apportioned 🚛
- **Dropdown:** "Apportioned Plate"
- **Visual:** "Apportioned" text on plate
- **No modifications**

### Code 35: Disabled/Handicapped ♿
- **Dropdown:** "Disabled/Handicapped Plate"
- **Visual:** Wheelchair symbol on LEFT + ALL NUMERIC
- **No modifications**

### Code 44: Disabled Vanity ♿
- **Dropdown:** "Disabled Vanity Plate"
- **Visual:** Wheelchair symbol on LEFT + ALPHA or ALPHA-NUMERIC
- **No modifications**
- **TIP:** Wheelchair + NOT all numeric = Disabled Vanity

### Code 57: Semi Trailer 🚚
- **Dropdown:** "Semi Trailer Plate"
- **Visual:** 'ST' vertical on RIGHT side
- **⚠️ MUST KEY 'ST' SUFFIX!**
- Example: Plate shows `123456` with vertical ST → Key as `123456ST`

### Code 77: B Truck 🚛
- **Dropdown:** "B Truck"
- **Visual:** 'B' or 'B TRUCK' vertical on RIGHT side
- **⚠️ MUST ADD 'B' AT END!**
- Example: Plate shows `3107003` → Key as `3107003B`

### Code 46: Passenger Vehicle 🚗
Most common - everything else is passenger vehicle.

#### Standard Passenger
- **Dropdown:** "Passenger Vehicle"
- **No modifications**

#### Ham Radio 📻
- **Dropdown:** "Passenger Vehicle"
- **⚠️ INCLUDE 'HAM', OMIT 'RADIO'**
- Examples: `HAM000000`, `HAMN9BVG`

#### Ambulance 🚑
- **Dropdown:** "Passenger Vehicle"
- **⚠️ ADD 'AM' AT END!**
- Examples: `000000AM`, `797002AM`
- **Special:** Reject if clearly marked emergency vehicle

#### Commercial 📦
- **Dropdown:** "Passenger Vehicle"
- **⚠️ OMIT small 'T'**
- Example: Plate shows `1234T56` → Key as `123456`

#### Temporary 📄
- **Dropdown:** "Passenger Vehicle"
- **Printed paper plates only**
- **Do NOT accept hand-written tags**

## Decision Tree

```
Start
  │
  ├─ See "Apportioned" text? → Code 31
  │
  ├─ See wheelchair symbol?
  │   ├─ All numeric? → Code 35 (Disabled/Handicapped)
  │   └─ Alpha/Alpha-numeric? → Code 44 (Disabled Vanity)
  │
  ├─ See 'ST' vertical on right? → Code 57 (Semi Trailer) + KEY 'ST'
  │
  ├─ See 'B' vertical on right? → Code 77 (B Truck) + ADD 'B'
  │
  └─ None of above? → Code 46 (Passenger Vehicle)
      │
      ├─ See 'HAM'? → Include HAM, omit RADIO
      ├─ Ambulance text? → Add 'AM' at end
      ├─ Small 'T'? → Omit the 'T'
      └─ Temporary paper? → Process as passenger
```

## Character Modification Summary

| Plate Type | Visual Cue | Modification Required |
|------------|------------|----------------------|
| Semi Trailer | 'ST' vertical | **Key 'ST' suffix** |
| B Truck | 'B' vertical | **Add 'B' at end** |
| Ham Radio | 'HAM' text | **Include HAM, omit RADIO** |
| Ambulance | 'Ambulance' text | **Add 'AM' at end** |
| Commercial | Small 'T' | **Omit the 'T'** |
| All others | N/A | No modification |

## Common Mistakes to Avoid

❌ **Mixing alpha and numeric** (except personalized all-alpha or all-numeric)
❌ **Forgetting space** in standard passenger plates
❌ **Missing 'ST' suffix** on semi trailers
❌ **Missing 'B' suffix** on B trucks
❌ **Keying 'RADIO'** on ham radio plates (omit it!)
❌ **Keying small 'T'** on commercial plates (omit it!)
❌ **Accepting hand-written** temporary tags (reject)

## Quick Tips

✅ **Wheelchair + all numeric** = Disabled/Handicapped (Code 35)
✅ **Wheelchair + not all numeric** = Disabled Vanity (Code 44)
✅ **Vertical text on right** = Look for ST or B
✅ **When in doubt** = Passenger Vehicle (Code 46)
✅ **Space matters** = Standard passenger MUST have space

## Validation Checklist

Before submitting:
- [ ] Checked for alpha-numeric mixing (not allowed!)
- [ ] Added space separator for standard passenger
- [ ] Keyed 'ST' suffix if semi trailer
- [ ] Added 'B' suffix if B truck
- [ ] Included 'HAM', omitted 'RADIO' if ham radio
- [ ] Added 'AM' suffix if ambulance
- [ ] Omitted small 'T' if commercial
- [ ] Selected correct dropdown based on code

---

**Last Updated:** October 1, 2025
**Total Plate Types:** 186
**Processing Types:** 10 unique types
**Status:** Production Ready ✅

For detailed documentation, see: `docs/ILLINOIS_PROCESSING_GUIDE.md`
