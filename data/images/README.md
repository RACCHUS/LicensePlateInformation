# Image Directory Structure

This directory contains reference images for license plates, organized by state and type.

## Directory Structure

```
images/
├── FL/                    # Florida
│   ├── plates/           # Example plate images
│   ├── logos/            # State logo/seal images
│   └── characters/       # Character reference images
├── GA/                   # Georgia
│   ├── plates/
│   ├── logos/
│   └── characters/
├── AL/                   # Alabama
│   ├── plates/
│   ├── logos/
│   └── characters/
├── SC/                   # South Carolina
│   ├── plates/
│   ├── logos/
│   └── characters/
└── NC/                   # North Carolina
    ├── plates/
    ├── logos/
    └── characters/
```

## Image Types

### Plates
- Example plate images showing actual plates in use
- Different plate types (passenger, commercial, specialty)
- Various lighting conditions and angles
- File naming: `[type]_[description].jpg` (e.g., `passenger_standard.jpg`)

### Logos
- State seals, logos, and graphic elements
- File naming: `logo.png` or `seal.png`

### Characters
- Individual character references showing state-specific fonts
- Ambiguous characters (0, O, 1, I, L, 8, B, etc.)
- File naming: `[character]_[description].png` (e.g., `0_slashed.png`, `O_letter.png`)

## Adding Images

To add new images:

1. Create the appropriate state directory if it doesn't exist
2. Place images in the correct subdirectory
3. Use descriptive filenames
4. Preferred formats: JPG for plates, PNG for logos and characters
5. Keep file sizes reasonable (under 1MB for quick loading)

## Image Sources

- Use public domain images when possible
- State DMV reference materials
- High-quality photographs with clear character visibility
- Ensure proper licensing for any copyrighted materials

## Usage in Application

Images are referenced in the database and loaded dynamically in the GUI. The application will show placeholder text if images are not found, so the system works without images but is enhanced when they are present.