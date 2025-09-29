"""
Data models for License Plate Information System
"""

from dataclasses import dataclass
from typing import List, Optional
import json

@dataclass
class State:
    """Represents a US state with license plate information"""
    state_id: Optional[int] = None
    name: str = ""
    abbreviation: str = ""
    slogan: Optional[str] = None
    uses_zero_for_o: bool = False
    allows_letter_o: bool = True
    zero_is_slashed: bool = False
    primary_colors: Optional[List[str]] = None
    logo_path: Optional[str] = None
    notes: Optional[str] = None
    
    def __post_init__(self):
        if self.primary_colors is None:
            self.primary_colors = []
    
    @property
    def colors_json(self) -> str:
        """Get colors as JSON string for database storage"""
        return json.dumps(self.primary_colors)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'State':
        """Create State from dictionary"""
        # Handle colors field which might be JSON string or list
        colors = data.get('primary_colors', [])
        if isinstance(colors, str):
            try:
                colors = json.loads(colors)
            except:
                colors = []
        
        return cls(
            state_id=data.get('state_id'),
            name=data.get('name', ''),
            abbreviation=data.get('abbreviation', ''),
            slogan=data.get('slogan'),
            uses_zero_for_o=bool(data.get('uses_zero_for_o', False)),
            allows_letter_o=bool(data.get('allows_letter_o', True)),
            zero_is_slashed=bool(data.get('zero_is_slashed', False)),
            primary_colors=colors,
            logo_path=data.get('logo_path'),
            notes=data.get('notes')
        )

@dataclass
class PlateType:
    """Represents a specific type of license plate within a state"""
    type_id: Optional[int] = None
    state_id: Optional[int] = None
    type_name: str = ""
    pattern: Optional[str] = None
    character_count: Optional[int] = None
    description: Optional[str] = None
    is_active: bool = True
    example_plate: Optional[str] = None
    background_color: Optional[str] = None
    text_color: Optional[str] = None
    has_stickers: bool = False
    sticker_description: Optional[str] = None
    image_path: Optional[str] = None
    notes: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: dict) -> 'PlateType':
        """Create PlateType from dictionary"""
        return cls(
            type_id=data.get('type_id'),
            state_id=data.get('state_id'),
            type_name=data.get('type_name', ''),
            pattern=data.get('pattern'),
            character_count=data.get('character_count'),
            description=data.get('description'),
            is_active=bool(data.get('is_active', True)),
            example_plate=data.get('example_plate'),
            background_color=data.get('background_color'),
            text_color=data.get('text_color'),
            has_stickers=bool(data.get('has_stickers', False)),
            sticker_description=data.get('sticker_description'),
            image_path=data.get('image_path'),
            notes=data.get('notes')
        )

@dataclass
class CharacterReference:
    """Represents character appearance information for a state"""
    ref_id: Optional[int] = None
    state_id: Optional[int] = None
    character: str = ""
    character_type: str = ""  # 'digit' or 'letter'
    image_path: Optional[str] = None
    description: Optional[str] = None
    is_ambiguous: bool = False
    confusion_chars: Optional[List[str]] = None
    
    def __post_init__(self):
        if self.confusion_chars is None:
            self.confusion_chars = []
    
    @property
    def confusion_chars_json(self) -> str:
        """Get confusion characters as JSON string"""
        return json.dumps(self.confusion_chars)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'CharacterReference':
        """Create CharacterReference from dictionary"""
        # Handle confusion_chars field which might be JSON string or list
        confusion_chars = data.get('confusion_chars', [])
        if isinstance(confusion_chars, str):
            try:
                confusion_chars = json.loads(confusion_chars)
            except:
                confusion_chars = []
        
        return cls(
            ref_id=data.get('ref_id'),
            state_id=data.get('state_id'),
            character=data.get('character', ''),
            character_type=data.get('character_type', ''),
            image_path=data.get('image_path'),
            description=data.get('description'),
            is_ambiguous=bool(data.get('is_ambiguous', False)),
            confusion_chars=confusion_chars
        )

@dataclass
class LookupHistory:
    """Represents a search history entry"""
    lookup_id: Optional[int] = None
    search_term: str = ""
    state_found: Optional[str] = None
    plate_type_found: Optional[str] = None
    timestamp: Optional[str] = None
    user_notes: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: dict) -> 'LookupHistory':
        """Create LookupHistory from dictionary"""
        return cls(
            lookup_id=data.get('lookup_id'),
            search_term=data.get('search_term', ''),
            state_found=data.get('state_found'),
            plate_type_found=data.get('plate_type_found'),
            timestamp=data.get('timestamp'),
            user_notes=data.get('user_notes')
        )