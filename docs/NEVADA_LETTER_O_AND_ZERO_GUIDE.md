# Nevada Letter "O" and Number "0" Usage Guide

## Overview
**State:** Nevada  
**Date:** October 1, 2025  
**Status:** Documented & Updated

---

## 🔍 Key Finding

**Nevada uses BOTH letter "O" and number "0", but in different contexts!**

This is a unique system where character usage depends on the **type of plate** (standard vs personalized).

---

## ✅ Standard Plates (No Number "0")

### Rule:
**Standard sequential plates do NOT include the number zero ("0")**

### Examples:
- **Home Means Nevada series**
- Plates like: **123·ABC**
- Sequential passenger plates
- Standard specialty plates

### Character Usage:
- ✅ **Letter "O"** is used
- ❌ **Number "0"** is NOT used

### Source:
Nevada DMV specifies that standard sequential plates do not contain the number zero.

---

## ✍️ Personalized Plates (Includes Number "0")

### Rule:
**Personalized/vanity plates DO include the number zero ("0")**

### Character Usage:
- ✅ **Letter "O"** is used
- ✅ **Number "0"** is used

### Visual Distinction:
To avoid confusion between "O" and "0", Nevada uses **different designs**:

| Character | Design | Description |
|---|---|---|
| **Number "0"** | Diamond-shaped or slightly rounded rectangular | More angular, distinct shape |
| **Letter "O"** | Circular or oval | Round, traditional letter shape |

### Examples:
- Custom vanity plates
- Personalized messages
- Any plate with owner-selected characters

---

## 🎯 Processing Rules

### For Standard Plates:
```
Plate shows: 123 ABC
Character that looks like O → It's letter "O"
(Standard plates never have number zero)

Processing: Key the letter "O", never "0"
```

### For Personalized Plates:
```
Plate shows: BO0K (personalized)
- Round O → Letter "O"
- Diamond-shaped 0 → Number "0"

Processing: Check shape to determine character
- Circular/oval = Letter "O"
- Diamond/rectangular = Number "0"
```

---

## 📊 Comparison Table

| Feature | Standard Plates | Personalized Plates |
|---|---|---|
| **Uses Letter "O"** | ✅ Yes | ✅ Yes |
| **Uses Number "0"** | ❌ No | ✅ Yes |
| **Visual Distinction** | N/A (only letter O) | Diamond vs Circular |
| **Plate Types** | Sequential, standard | Vanity, custom |
| **Examples** | 123·ABC | BO0K, G0LD |

---

## 🔤 Visual Identification Guide

### How to Tell If It's "O" or "0":

#### On Standard Plates:
**Simple rule:** If it's a standard sequential plate → **It's always letter "O"**

#### On Personalized Plates:
**Look at the shape:**

```
Number "0" (Zero):
◇ Diamond-shaped
▭ Slightly rounded rectangular
⬡ More angular appearance
█ Distinct edges

Letter "O":
○ Circular
⬭ Oval
◯ Round shape
⭕ Traditional letter form
```

---

## 📝 Data Structure Updates

### Global Rules Updated:
```json
"character_restrictions": {
  "standard_plates": {
    "uses_letter_o": true,
    "uses_number_zero": false,
    "description": "Standard plates use only letter 'O' (no zeros)"
  },
  "personalized_plates": {
    "uses_letter_o": true,
    "uses_number_zero": true,
    "visual_distinction": "Number '0' is diamond-shaped; Letter 'O' is circular"
  }
}
```

### Top-Level Fields Updated:
```json
"uses_zero_for_o": false,
"allows_letter_o": true,
"letter_o_and_zero_usage": {
  "standard_plates": {
    "uses_letter_o": true,
    "uses_number_zero": false
  },
  "personalized_plates": {
    "uses_letter_o": true,
    "uses_number_zero": true,
    "visual_distinction": "Diamond-shaped vs circular"
  }
}
```

---

## ⚠️ Important Processing Notes

### For Data Entry:

1. **Determine plate type FIRST:**
   - Is it a standard sequential plate? → Only letter "O" possible
   - Is it a personalized plate? → Both "O" and "0" possible

2. **For standard plates:**
   - Any O-shaped character → Enter as letter "O"
   - Never enter number "0"

3. **For personalized plates:**
   - Check the shape carefully
   - Diamond/rectangular → Number "0"
   - Circular/oval → Letter "O"

---

## 🌟 Nevada's Unique System

### What Makes This Special:

**Nevada is unique because:**
- Most states pick ONE approach (either letter O OR number 0)
- Nevada uses BOTH, but separates them by plate type
- Visual distinction helps avoid confusion on personalized plates
- Standard plates have simpler rule (letter O only)

### Comparison to Other States:

| State | Approach |
|---|---|
| **Florida** | Only number "0", never letter "O" |
| **Maine** | Letter "O" and "I" not used (confused with 0 and 1) |
| **Nevada** | BOTH, but separated by plate type (unique!) |
| **Most States** | One or the other, not both |

---

## 🎓 Best Practices

### For Processors:

1. **Check plate type category:**
   - Standard/Sequential → Letter "O" only
   - Personalized/Vanity → Check shape for "O" vs "0"

2. **When in doubt on personalized plates:**
   - Look for angular/diamond shape → Number "0"
   - Look for round/circular shape → Letter "O"

3. **Document ambiguous cases:**
   - If unclear, note the plate type and context
   - Review with DMV images when available

### For System Design:

1. **Plate type field is critical:**
   - Must distinguish standard vs personalized
   - Processing rules depend on this classification

2. **Visual recognition training:**
   - Train operators on shape distinction
   - Provide clear examples of both characters

3. **Validation rules:**
   - Standard plates: Reject number "0"
   - Personalized plates: Accept both "O" and "0"

---

## 📸 Visual Examples Needed

### To Complete Documentation:

1. Standard plate with letter "O": **123·OAK**
2. Personalized plate with letter "O": **B○○K** (circular)
3. Personalized plate with number "0": **G◇LD** (diamond)
4. Side-by-side comparison showing shape difference

---

## 📚 Sources

- **Nevada DMV Official Documentation:** Standard plates do not contain number zero
- **Reddit User Reports:** Personalized plates use diamond-shaped zero
- **Visual Analysis:** Letter "O" is circular/oval; Number "0" is diamond-shaped

---

## ✅ Validation Checklist

- [x] Global rules updated with detailed character restrictions
- [x] Top-level fields updated (uses_zero_for_o, allows_letter_o)
- [x] Letter O and zero usage documented by plate type
- [x] Visual distinction documented
- [x] Processing rules defined
- [x] Best practices established
- [x] Documentation created

---

## 🎯 Key Takeaways

### The Simple Version:

**Standard plates:** If you see "O" → It's letter "O" (never zero)

**Personalized plates:** Look at the shape:
- Round → Letter "O"
- Diamond → Number "0"

### The Technical Version:

Nevada implements a **dual-character system** where:
- Character availability depends on plate type
- Visual design distinguishes ambiguous characters
- Processing rules must account for plate classification
- This is a unique approach among US states

---

**Status:** ✅ Documentation Complete  
**Last Updated:** October 1, 2025  
**Nevada Data:** Updated with accurate O/0 information
