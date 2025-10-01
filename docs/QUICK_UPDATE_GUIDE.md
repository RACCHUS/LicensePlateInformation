# Quick Reference: Updating Plate Type Dropdown

## ✅ ONE-CLICK UPDATE (Recommended)

```bash
python scripts/updating/auto_update_dropdown.py
```

**Or just double-click the file!**

This single script automatically:
- ✅ Scans all state JSON files
- ✅ Extracts all plate types  
- ✅ Updates extracted_plate_types.json
- ✅ Updates state_plate_type_mapping.json ← **Required for dropdown**
- ✅ Shows you a complete summary

---

## When to Run

Run `auto_update_dropdown.py` after:
- ✅ Adding new states
- ✅ Adding plate types to existing states
- ✅ Updating plate type names
- ✅ Making ANY changes to state JSON files

---

## Current Status

**Total Plate Types:** 338  
**Total States:** 60

**Top States by Plate Count:**
1. Florida (FL): 265 types
2. Alabama (AL): 78 types ← **Just fixed!**
3. Georgia (GA): 15 types
4. Tennessee (TN): 11 types

---

## Restart Application

After updating, restart the app:
```bash
python main.py
```

The dropdown will now show the updated plate types!

---

## Troubleshooting

**Dropdown not updating?**
1. Did you run `auto_update_dropdown.py`? ← Must do this!
2. Did you restart the application?
3. Check both files were updated:
   - `data/extracted_plate_types.json`
   - `data/state_plate_type_mapping.json` ← **App uses this one**

**Still having issues?**
- Check the full documentation: `docs/ALABAMA_FIX_SUMMARY.md`
- Verify state JSON file has correct plate_types array
- Look for errors in terminal output

---

## That's It!

Just remember: **One script updates everything** 🎉

`python scripts/updating/auto_update_dropdown.py`
