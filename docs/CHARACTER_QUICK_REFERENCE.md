# Quick Reference: Character Handling by State

## 🚫 NO Letter "O" - Always Use Zero "0"

Alabama, Connecticut, Florida, Georgia, Hawaii, Idaho, Kansas, Michigan, Minnesota, Missouri, Montana, Nebraska, Nevada, New Jersey, New Mexico, Texas, Utah

**Example:** TX-ABC012 ✅ (not TX-ABC0O2 ❌)

---

## ✅ Letter "O" with Letters, Zero "0" with Numbers

Alaska, Arkansas, California, Colorado, Delaware, Illinois, Indiana, Iowa, Louisiana, Massachusetts, Maryland, Mississippi, North Dakota, Ohio, Oklahoma, Puerto Rico, Rhode Island, Virginia, Washington

**Example:** CA-2ABC456 ✅ (O with letters, 0 with numbers)

---

## 🔹 Letter "O" ONLY on Personalized/Vanity

Arizona, Kentucky, Maine, New Hampshire

**Standard plates:** Use 0 only  
**Vanity plates:** O allowed

---

## Critical Stacked Character Rules

### ALWAYS INCLUDE
- **Louisiana:** MA, NA, AR, MH, NG
- **Maryland:** AF, HDV
- **New Hampshire:** CH + symbols (&, +, and, -)

### ALWAYS OMIT
- **California:** E (and LEFT stacked if >10 chars)
- **Minnesota:** E (it's a sticker!)
- **Michigan:** EX POW, duplicate DV, branch names

### SPECIAL CASES

**Mississippi National Guard:**
- ADD prefix "NG" → MS-NG28624

**North Carolina Supreme Court:**
- ADD prefix "SC"

**Wyoming (single digit before horse):**
- ADD leading 0 → WY-013918

**New Jersey Dealer Plates:**
- OMIT small characters on dealer plates ONLY
- INCLUDE all characters on non-dealer plates

---

## Quick Decision Tree

**See letter that looks like O or 0?**
1. Check state in "NO Letter O" list → Use 0
2. State allows both → Is it in letters? Use O. In numbers? Use 0.
3. Not sure? Check state JSON file

**See stacked/small characters?**
1. Check state rules above
2. Military/service codes? Usually INCLUDE
3. Vehicle type words? Usually OMIT
4. When in doubt, check CHARACTER_RULES_UPDATE.md

---

## State-Specific Notes

**Alabama:** Include X2, TL, TR, DV, Q1 in middle; omit 200, T on left

**California:** Max 10 chars; omit LEFT stacked if exceeds

**Louisiana:** Include state codes; omit branch names (unless no stacked chars)

**New Hampshire:** ONLY state that accepts symbols (&, +, and, -)

**Tennessee:** Volunteers plates: include V0, omit T

---

## Full Documentation

See: `docs/CHARACTER_RULES_UPDATE.md`
