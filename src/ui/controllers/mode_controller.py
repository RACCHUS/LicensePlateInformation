"""
Mode Controller for License Plate Information System.

Manages queue mode logic - which states are primary, secondary, or excluded
based on the current operating mode (V3, Express, I95, OOSV3, PlateType, All).
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Set

from PySide6.QtCore import QObject, Signal


class ModeController(QObject):
    """
    Controller for queue mode management.
    
    Provides state categorization based on the current mode:
    - Primary states: Large, prominent buttons
    - Secondary states: Medium buttons, frequently needed
    - Normal states: Standard buttons, all other states
    - Excluded states: Hidden or de-emphasized (mode-specific)
    """
    
    # Signals
    mode_changed = Signal(str, dict)  # mode_name, mode_config
    
    # All US states + DC + territories + Canadian provinces
    ALL_JURISDICTIONS = [
        # US States
        "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
        "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
        "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
        "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
        "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY",
        # DC and Territories
        "DC", "PR", "GU", "VI", "AS", "MP",
        # Canadian Provinces
        "AB", "BC", "MB", "NB", "NL", "NS", "NT", "NU", "ON", "PE", "QC", "SK", "YT"
    ]
    
    # Canadian provinces (for special handling in OOSV3)
    CANADIAN_PROVINCES = ["AB", "BC", "MB", "NB", "NL", "NS", "NT", "NU", "ON", "PE", "QC", "SK", "YT"]
    
    # US States only (no territories or Canada)
    US_STATES = [
        "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
        "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
        "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
        "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
        "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY", "DC"
    ]
    
    def __init__(self, parent=None, config_path: str = "config/queue_modes.json"):
        super().__init__(parent)
        
        self.config_path = Path(config_path)
        self.modes: Dict[str, dict] = {}
        self.current_mode: str = "All"
        self._current_config: dict = {}
        
        self._load_modes()
    
    def _load_modes(self):
        """Load mode definitions from config file."""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                self.modes = config.get("modes", {})
                
                # Set default mode from config
                default = config.get("default_mode", "All")
                if default in self.modes:
                    self.current_mode = default
                    self._current_config = self.modes[default]
                
                print(f"[OK] Loaded {len(self.modes)} queue modes from {self.config_path}")
            except Exception as e:
                print(f"[WARN] Error loading modes config: {e}")
                self._create_default_modes()
        else:
            print(f"[WARN] Modes config not found at {self.config_path}, using defaults")
            self._create_default_modes()
    
    def _create_default_modes(self):
        """Create default mode definitions if config missing."""
        self.modes = {
            "V3": {
                "description": "Florida primary, common out-of-state",
                "primary": ["FL"],
                "secondary": ["GA", "AL", "SC", "NC", "TN", "MS", "LA", "TX"],
                "excluded": [],
                "show_all_states": True
            },
            "All": {
                "description": "All states equally weighted",
                "primary": [],
                "secondary": [],
                "excluded": [],
                "show_all_states": True
            }
        }
        self._current_config = self.modes["All"]
    
    @property
    def available_modes(self) -> List[str]:
        """Get list of available mode names."""
        return list(self.modes.keys())
    
    @property
    def current_config(self) -> dict:
        """Get current mode configuration."""
        return self._current_config
    
    def set_mode(self, mode_name: str) -> bool:
        """
        Switch to a different mode.
        
        Args:
            mode_name: Name of mode to switch to
            
        Returns:
            True if mode was changed, False if invalid mode
        """
        if mode_name not in self.modes:
            print(f"[WARN] Unknown mode: {mode_name}")
            return False
        
        if mode_name == self.current_mode:
            return True  # Already in this mode
        
        self.current_mode = mode_name
        self._current_config = self.modes[mode_name]
        
        print(f"[MODE] Changed to: {mode_name}")
        self.mode_changed.emit(mode_name, self._current_config)
        return True
    
    def get_mode_description(self, mode_name: Optional[str] = None) -> str:
        """Get description for a mode."""
        mode = mode_name or self.current_mode
        if mode in self.modes:
            return self.modes[mode].get("description", "")
        return ""
    
    def get_primary_states(self) -> List[str]:
        """Get primary states for current mode (largest buttons)."""
        return self._current_config.get("primary", [])
    
    def get_secondary_states(self) -> List[str]:
        """Get secondary/frequent states for current mode."""
        return self._current_config.get("secondary", [])
    
    def get_excluded_states(self) -> Set[str]:
        """Get states excluded in current mode."""
        return set(self._current_config.get("excluded", []))
    
    def get_normal_states(self) -> List[str]:
        """
        Get states that are neither primary, secondary, nor excluded.
        These are shown in the "All States" section.
        """
        primary = set(self.get_primary_states())
        secondary = set(self.get_secondary_states())
        excluded = self.get_excluded_states()
        
        # Return US states that aren't primary, secondary, or excluded
        return [s for s in self.US_STATES 
                if s not in primary and s not in secondary and s not in excluded]
    
    def get_canadian_provinces(self) -> List[str]:
        """Get Canadian provinces (shown separately or in OOSV3)."""
        excluded = self.get_excluded_states()
        return [p for p in self.CANADIAN_PROVINCES if p not in excluded]
    
    def is_state_excluded(self, state_code: str) -> bool:
        """Check if a state is excluded in current mode."""
        return state_code in self.get_excluded_states()
    
    def is_state_primary(self, state_code: str) -> bool:
        """Check if a state is primary in current mode."""
        return state_code in self.get_primary_states()
    
    def is_state_secondary(self, state_code: str) -> bool:
        """Check if a state is secondary in current mode."""
        return state_code in self.get_secondary_states()
    
    def get_state_category(self, state_code: str) -> str:
        """
        Get the category of a state in current mode.
        
        Returns:
            'primary', 'secondary', 'normal', or 'excluded'
        """
        if self.is_state_excluded(state_code):
            return 'excluded'
        if self.is_state_primary(state_code):
            return 'primary'
        if self.is_state_secondary(state_code):
            return 'secondary'
        return 'normal'
    
    def show_all_states(self) -> bool:
        """Check if 'All States' section should be shown."""
        return self._current_config.get("show_all_states", True)
    
    def get_organized_states(self) -> Dict[str, List[str]]:
        """
        Get all states organized by category for UI layout.
        
        Returns:
            Dict with keys: 'primary', 'secondary', 'normal', 'canadian'
        """
        return {
            'primary': self.get_primary_states(),
            'secondary': self.get_secondary_states(),
            'normal': self.get_normal_states(),
            'canadian': self.get_canadian_provinces()
        }
