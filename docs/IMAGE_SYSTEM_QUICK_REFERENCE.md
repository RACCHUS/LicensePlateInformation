# Quick Reference: Image System

## Image Viewer Information Display

### What You See:
```
┌─────────────────────────────────────┐
│  [◀ Previous]   Image 1 of 6  [Next ▶]
├─────────────────────────────────────┤
│                                     │
│         [LICENSE PLATE IMAGE]       │
│                                     │
├─────────────────────────────────────┤
│  Passenger Default                  │  ← Plate Type Name (from JSON)
│  AL • Plate Type: Passenger Default │
│     • File: plate_sample.png        │  ← State, Type, Filename
└─────────────────────────────────────┘
```

### Information Shown:
1. **Top Bar**: Navigation and image counter
2. **Main Area**: License plate image (resized to fit)
3. **Bottom Bar**: 
   - Line 1: **Plate Type Name** (actual type from state JSON)
   - Line 2: **State Code • Plate Type • Filename**

---

## Image Priority Order

Images appear in this order:

### 1. By Vehicle Type (TYPE_PRIORITY):
```
0 = Generic (plate_sample)           ← APPEARS FIRST
1 = Commercial (truck, trailer)      ← APPEARS SECOND
2 = Passenger/Standard
3 = Motorcycle
4 = Specialty
5+ = Other types
```

### 2. By Image Type (IMAGE_TYPE_PRIORITY):
```
Within each vehicle type:
1 = Sample (plate_sample, truck_sample)  ← APPEARS FIRST
2 = Blank (blank_template)
3 = Font (font_sample, font0.png)
4 = Variation (other images)
```

### Example Order for a State:
```
1. plate_sample.png          (Generic, Sample)
2. truck_sample.png          (Commercial Truck, Sample)
3. trailer_sample.png        (Commercial Trailer, Sample)
4. semi-trailer_sample.png   (Commercial Semi, Sample)
5. fleet-trailer_sample.png  (Commercial Fleet, Sample)
6. font0.png                 (Generic, Font)
7. passenger_variation.png   (Passenger, Variation)
...and so on
```

---

## Scripts

### Update JSON Files
```bash
python scripts\update_json_image_paths.py
```
**What it does**: Updates all state JSON files with correct image paths from Plates folder
**When to run**: After adding new images to Plates directory

### Test Image Priority
```bash
python scripts\test_image_priority.py
```
**What it does**: Verifies images appear in correct priority order
**Output**: Shows which images appear first for each state

---

## Adding New Images

### Step 1: Add Image File
Place in: `data/images/Plates/{StateName}/`

**Naming Convention:**
- `plate_sample.png` - Standard/Passenger plate
- `truck_sample.png` - Truck plate
- `trailer_sample.png` - Trailer plate
- `semi-trailer_sample.png` - Semi-trailer plate
- `fleet-trailer_sample.png` - Fleet trailer
- `rental-trailer_sample.png` - Rental trailer
- `permanent-trailer_sample.png` - Permanent trailer
- `font0.png` or `fontO.png` - Character font reference

### Step 2: Update JSON
```bash
python scripts\update_json_image_paths.py
```

### Step 3: Verify
```bash
python scripts\test_image_priority.py
```

### Step 4: Test in App
```bash
python main.py
```
Select the state and verify the image appears correctly.

---

## Troubleshooting

### Image Not Showing?
1. Check file exists in `data/images/Plates/{StateName}/`
2. Check file extension is `.png`, `.jpg`, `.jpeg`, or `.gif`
3. Run update script: `python scripts\update_json_image_paths.py`
4. Check JSON file has correct path

### Wrong Image Order?
1. Check filename follows naming convention
2. Run test script: `python scripts\test_image_priority.py`
3. Review priority system above
4. Ensure `_sample` is in filename for priority images

### Plate Type Name Not Showing?
1. Check JSON file has `type_name` field
2. Check image path in JSON matches actual file
3. Verify JSON `images` section has the path
4. Run update script to regenerate paths

### Error: "unhashable type: 'list'"
**Fixed!** This was caused by variation arrays in JSON. Now handled automatically.

---

## File Locations

### Images:
- `data/images/Plates/{StateName}/` - New centralized location
- `data/images/{STATE_CODE}/plates/` - Alternative location
- `data/images/{STATE_CODE}/` - Legacy location

### JSON Files:
- `data/states/{state_name}.json` - State configuration and plate types

### Scripts:
- `scripts/update_json_image_paths.py` - Update all JSON files
- `scripts/test_image_priority.py` - Test priority ordering

### Code:
- `src/gui/components/image_display/image_viewer.py` - Image viewer component

---

## State Code → Folder Name Mapping

Some states have special mappings:

| Code | Folder Name      | JSON File         |
|------|------------------|-------------------|
| IL   | Illinios (typo!) | illinois.json     |
| NH   | New Hampshire    | new_hampshire.json|
| NJ   | New Jersey       | new_jersey.json   |
| NM   | New Mexico       | new_mexico.json   |
| NY   | New York         | new_york.json     |
| NC   | North Carolina   | north_carolina.json|
| ND   | North Dakota     | north_dakota.json |
| RI   | Rhode Island     | rhode_island.json |
| SC   | South Carolina   | south_carolina.json|
| SD   | South Dakota     | south_dakota.json |
| WV   | West Virginia    | west_virginia.json|

All other states use standard naming (e.g., Alabama → alabama.json)

---

## Quick Commands

```bash
# Full workflow for adding images:
python scripts\update_json_image_paths.py
python scripts\test_image_priority.py
python main.py

# Check all images are in order:
python scripts\test_image_priority.py | findstr "WARNING ERROR"

# Update single state (not implemented - always updates all):
# Use the full script, it's fast enough
```

---

## Notes

- Image viewer automatically resizes images to fit the display area
- Aspect ratio is always maintained
- Navigation buttons disable when at first/last image
- System handles missing images gracefully
- Multiple image locations are supported for backward compatibility
