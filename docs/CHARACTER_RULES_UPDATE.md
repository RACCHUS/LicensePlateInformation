# Character Handling Rules Update Summary

**Date:** October 1, 2025  
**Source:** OOSv2.txt documentation  
**Status:** ✅ COMPLETE - 49 states updated

---

## What Was Updated

### 1. Letter O vs Zero 0 Rules

**States That Do NOT Use Letter "O" (17 states):**
- Alabama, Connecticut, Florida, Georgia, Hawaii
- Idaho, Kansas, Michigan, Minnesota, Missouri
- Montana, Nebraska, Nevada, New Jersey, New Mexico
- Texas, Utah

**Rule:** `uses_zero_for_o: true`, `allows_letter_o: false`

**States Using O with Letters, 0 with Numbers (19 states):**
- Alaska, Arkansas, California, Colorado, Delaware
- Illinois, Indiana, Iowa, Louisiana, Massachusetts
- Maryland, Mississippi, North Dakota, Ohio, Oklahoma
- Puerto Rico, Rhode Island, Virginia, Washington

**Rule:** `uses_zero_for_o: true`, `allows_letter_o: true`

**States: O Only on Personalized/Vanity (4 states):**
- Arizona, Kentucky, Maine, New Hampshire

**Rule:** O restricted to personalized plates only

**Special Cases:**
- **New York:** No O on standard; O and 0 on vanity (O rounder, 0 slimmer)
- **North Carolina:** O only on Outer Banks (OBX) special tags
- **Tennessee:** No O on standard; O and 0 on Drive Out Tags/Temporary Permits
- **Pennsylvania:** Both O and 0 used; numbers ¼" taller
- **Oregon:** O and 0 interchangeable/not distinguished

---

### 2. Stacked/Slanted Character Rules

#### INCLUDE Stacked Characters

**Alabama:**
- Include: X2, TL, TR, DV, Q1 (middle of plate)
- Omit: 200, T (left side)

**Arkansas:**
- Include: AB, EM, US, PHS, Ex, FX, PF
- Omit: TRUCK, ARK

**Delaware:**
- Include: CL

**Kansas:**
- Include: PWR

**Kentucky:**
- Include: BX, AY, GX, HK, V

**Louisiana:**
- Include: MA, NA, AR, MH, NG (ALWAYS)
- Omit: USMC, NAVY, ARMY (slanted branch names)
- Special: Include slanted if no stacked (e.g., LA-ARMY453)

**Maryland:**
- Include: AF, HDV (ALWAYS)

**Michigan:**
- Include: M, S (State University), D (smaller letters in middle)
- Omit: EX POW, DV (omit one if both), IRAQ, VIETNAM (branch/campaign names)

**Mississippi:**
- Include: TLR, AU, AV, MC, MQ, DB
- Omit: TLR on red plates ending with A
- Special: B/F plates with small numbers MUST be keyed
- Special: National Guard plates ADD prefix "NG" (e.g., MS-NG28624)

**Nevada:**
- Include: DT

**New Hampshire:**
- Include: CH
- Symbols: &, +, and, - (ALWAYS include these symbols)
- Special: NH ONLY accepts these symbols; dropdown always "Standard" not "DASH IN tag"

**New Jersey:**
- Include: WD, NG, HM, NJ (stacked/small numbers)
- Omit: Small characters on New/Used Dealer plates only
- Special: Non-dealer plates include ALL characters including small ones (e.g., NJ-5647DTM where "47" is small)

**New Mexico:**
- Include: MI, LC, SU, KID (ALL stacked)

**New York:**
- Include: EMTP, VAS, DAV, MD

**North Carolina:**
- Include: DV, IC, VF, PH, PD, NC, NG (vertical/small must be keyed)
- Omit: ALL symbols (-)
- Special: Supreme Court plates ADD prefix "SC"

**Oregon:**
- Include: HP, HU (stacked)
- Special: Apportioned plates include small "Y"

**Pennsylvania:**
- Include: Stacked on US ARMY VETERAN, US AIR VETERAN, VETERAN, NATIONAL GUARD, EMERGENCY MEDICAL SERVICES, FIRE FIGHTER
- Include: Small "PD" by wheelchair symbol

**Rhode Island:**
- Include: TRL
- Omit: Dash (-)

**South Carolina:**
- Include: CC, EA, VT, ZD
- Visual: Tree in middle of plate

**Tennessee:**
- Include: V0 (on Volunteers plates)
- Omit: T (on Volunteers plates)

**Texas:**
- Include: DV
- Omit: T (in white part of plate)

**Virginia:**
- Include: ID, ZE, TR, RS (stacked in rescue square)
- Include: FD (from Fire Fighter logo)
- Omit: DV, VET (vertical/diagonal with different font/color)

**Washington:**
- Include: AR, GRN
- Omit: TRAN

**Wyoming:**
- Include: TRL, 22T (slanted on TRUCK plates)
- Special: Single digit before horse needs leading 0 (e.g., WY-013918)

#### OMIT Stacked Characters

**California:**
- Omit: E
- Special: Max 10 characters; if plate exceeds 10, OMIT stacked on LEFT side

**Colorado:**
- Omit: FLT
- Omit: DV (on Disabled Veteran plates)

**Idaho:**
- Omit: PRP

**Minnesota:**
- Omit: E (top right corner - it's a sticker)

**North Dakota:**
- Omit: PRP (on left side)

**Oklahoma:**
- Omit: UD013 (on Used Dealer plates)

**Ontario (Canada):**
- Omit: PRP (on YOURS TO DISCOVER plate)

**Vermont:**
- Omit: TRK

---

## JSON Structure Added

Each updated state JSON now contains:

```json
{
  "uses_zero_for_o": true/false,
  "allows_letter_o": true/false,
  "processing_metadata": {
    "global_rules": {
      "stacked_characters": {
        "include": ["X2", "TL", "TR"],
        "omit": ["200", "T"],
        "position": "Description of where to include/omit",
        "max_characters": 10,
        "prefix_rules": {
          "rule_type": "description"
        },
        "symbols_allowed": ["&", "+", "-"],
        "notes": "Detailed processing instructions"
      }
    }
  },
  "notes": "Updated with O vs 0 rules and processing instructions"
}
```

---

## Visual Identifiers Added

- **South Carolina:** Tree in middle of plate
- **Oregon:** "OR" in top left

---

## Special Rules Documented

- **U-Haul:** Can use customer plates

---

## States Updated

✅ **49 states updated** with character handling rules:
- Alabama, Alaska, Arizona, Arkansas, California
- Colorado, Connecticut, Delaware, Florida, Georgia
- Hawaii, Idaho, Illinois, Indiana, Iowa
- Kansas, Kentucky, Louisiana, Maine, Maryland
- Massachusetts, Michigan, Minnesota, Mississippi, Missouri
- Montana, Nebraska, Nevada, New Hampshire, New Jersey
- New Mexico, New York, North Carolina, North Dakota, Ohio
- Oklahoma, Ontario, Oregon, Pennsylvania, Puerto Rico
- Rhode Island, South Carolina, Tennessee, Texas, Utah
- Vermont, Virginia, Washington, Wyoming

⏭️ **11 states skipped** (no rules found in OOSv2.txt):
- Alberta, American Samoa, Diplomatic Corps, Guam
- Northern Mariana Islands, South Dakota, US Government
- US Virgin Islands, Washington DC, West Virginia, Wisconsin

---

## Verification Results

### Alabama ✅
- Uses zero for O: True
- Allows letter O: False
- Stacked include: X2, TL, TR, DV, Q1
- Stacked omit: 200, T

### California ✅
- Uses zero for O: True
- Allows letter O: True (with letters only)
- Stacked omit: E
- Max characters: 10

### New Hampshire ✅
- Uses zero for O: True
- Allows letter O: True (personalized only)
- Stacked include: CH
- Symbols allowed: &, +, and, -

### Louisiana ✅
- Uses zero for O: True
- Allows letter O: True (with letters)
- Stacked include: MA, NA, AR, MH, NG
- Stacked omit: USMC, NAVY, ARMY

---

## Application Impact

### For Data Entry Personnel:
1. **O vs 0 rules** clearly defined per state
2. **Stacked character handling** standardized
3. **Special symbols** documented (especially NH)
4. **Prefix rules** for special cases (MS National Guard, NC Supreme Court)

### For Processing System:
1. Validation rules can reference `processing_metadata.global_rules.stacked_characters`
2. Character restrictions enforced via `uses_zero_for_o` and `allows_letter_o`
3. State-specific edge cases documented in notes

### For Quality Assurance:
1. Clear rules for what to include/omit
2. Visual identifiers help verify correct plate identification
3. Special cases and exceptions documented

---

## Next Steps

### Immediate:
1. ✅ **DONE:** Update all state JSONs with character rules
2. **TODO:** Run dropdown update script
3. **TODO:** Test application with updated rules

### Run This Command:
```bash
python scripts/updating/auto_update_dropdown.py
```

Then restart the application:
```bash
python main.py
```

### Future Enhancements:
1. Add visual validation for stacked characters
2. Implement real-time character validation based on state rules
3. Create training materials showing examples of stacked characters
4. Add plate images to demonstrate include/omit rules

---

## Files Modified

### State JSON Files (49 files)
All updated with:
- O vs 0 usage rules
- Stacked/slanted character handling
- Processing metadata
- Enhanced notes

### Scripts Created
- `scripts/updating/update_character_rules.py` - Systematic updater

### Documentation
- This file: `docs/CHARACTER_RULES_UPDATE.md`

---

## Quality Assurance Checklist

- [x] All 17 "no letter O" states marked correctly
- [x] All 19 "O with letters, 0 with numbers" states marked
- [x] All 4 "O only personalized" states marked
- [x] Special cases documented (NY, NC, TN, PA, OR)
- [x] Stacked character include rules added
- [x] Stacked character omit rules added
- [x] Special prefix rules added (MS, NC, WY)
- [x] Symbol rules added (NH)
- [x] Visual identifiers added (SC, OR)
- [x] Max character rules added (CA)
- [x] JSON structure validated
- [x] Sample states verified

---

## Support

For questions about character handling:
1. Check this document: `docs/CHARACTER_RULES_UPDATE.md`
2. Review source: `data/pending/OOSv2.txt`
3. Check state JSON: `data/states/{state_name}.json`
4. Look at `processing_metadata.global_rules.stacked_characters`

**The system now has comprehensive character handling rules for accurate license plate data entry!** 🎉
