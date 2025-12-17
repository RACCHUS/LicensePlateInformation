# License Plate Information - User Guide

Welcome to the License Plate Information System! This guide will help you get started.

## Overview

This application provides quick access to license plate information for all US states and Canadian provinces. It's designed for rapid lookup during toll processing workflows.

## Getting Started

### 1. Select a Mode

The **Mode** dropdown in the toolbar lets you optimize the interface for your current queue:

- **All** - Shows all states equally (default)
- **V3** - Florida primary, common out-of-state secondary
- **Express** - Same as V3
- **I95** - Florida primary, I-95 corridor states secondary
- **OOSV3** - Out-of-state plates only (excludes FL and Plate Type states)
- **PlateType** - States with multiple plate types (MA, ME, OH, IN, IL)

### 2. Select a State

Click any state button in the left panel. The four info panels will immediately update:

- **State Info** (top-left) - Basic state information and character rules
- **Character Rules** (top-right) - O vs 0 rules and stacked character details
- **Plate Type Info** (bottom-left) - Details about the selected plate type
- **Images** (bottom-right) - Sample plate images

### 3. Select a Plate Type

For states with multiple plate types (FL, MA, ME, OH, IN, IL), use the **Plate Type** dropdown to select a specific type. Other states only have "Standard" available.

## Tips for Fast Lookups

1. **Use keyboard shortcuts** - Press `Ctrl+Shift+1` through `Ctrl+Shift+5` to quickly switch modes
2. **Search** - Press `Ctrl+F` to search for state information
3. **Mode buttons show priority** - In V3/Express modes, FL is prominently displayed at the top

## Interface Layout

The interface shows all information at once - no need to click tabs:

```
┌─────────────┬──────────────────┬──────────────────┐
│ State Panel │ State Info       │ Character Rules  │
│             │                  │                  │
│ Mode: V3    ├──────────────────┼──────────────────┤
│             │ Plate Type Info  │ Images           │
│ [FL] [GA]...│                  │                  │
└─────────────┴──────────────────┴──────────────────┘
```

## Changing Default Mode

1. Go to **File > Settings** (or press `Ctrl+,`)
2. Select your preferred default mode
3. The app will start in this mode next time

## Need More Help?

- **Keyboard Shortcuts** - See `Help > Keyboard Shortcuts`
- **Emergency Vehicles** - See `Help > Emergency Vehicle Guide`
- **Character Recognition** - See `Help > Character Recognition (O vs 0)`
