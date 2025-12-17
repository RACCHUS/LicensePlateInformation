"""
User Image data model for user-submitted license plate images.
"""

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
import json


@dataclass
class UserImage:
    """
    Represents a user-submitted license plate image with optional metadata.
    
    All fields except filename and state_code are optional to allow
    users to add images quickly without requiring detailed information.
    """
    filename: str
    state_code: str
    plate_type: Optional[str] = None
    description: Optional[str] = None
    is_character_example: bool = False
    excluded_characters: Optional[List[str]] = None
    included_characters: Optional[List[str]] = None
    notes: Optional[str] = None
    tags: Optional[List[str]] = None
    added_date: str = field(default_factory=lambda: datetime.now().isoformat())
    source_path: Optional[str] = None  # Original path before import
    
    def __post_init__(self):
        """Initialize default values for list fields."""
        if self.excluded_characters is None:
            self.excluded_characters = []
        if self.included_characters is None:
            self.included_characters = []
        if self.tags is None:
            self.tags = []
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'filename': self.filename,
            'state_code': self.state_code,
            'plate_type': self.plate_type,
            'description': self.description,
            'is_character_example': self.is_character_example,
            'excluded_characters': self.excluded_characters,
            'included_characters': self.included_characters,
            'notes': self.notes,
            'tags': self.tags,
            'added_date': self.added_date,
            'source_path': self.source_path
        }
    
    def to_json(self) -> str:
        """Serialize to JSON string."""
        return json.dumps(self.to_dict(), indent=2)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'UserImage':
        """Create UserImage from dictionary."""
        return cls(
            filename=data.get('filename', ''),
            state_code=data.get('state_code', ''),
            plate_type=data.get('plate_type'),
            description=data.get('description'),
            is_character_example=bool(data.get('is_character_example', False)),
            excluded_characters=data.get('excluded_characters', []),
            included_characters=data.get('included_characters', []),
            notes=data.get('notes'),
            tags=data.get('tags', []),
            added_date=data.get('added_date', datetime.now().isoformat()),
            source_path=data.get('source_path')
        )
    
    @classmethod
    def from_json(cls, json_str: str) -> 'UserImage':
        """Create UserImage from JSON string."""
        return cls.from_dict(json.loads(json_str))
    
    @property
    def display_name(self) -> str:
        """Get a display-friendly name for the image."""
        if self.description:
            return self.description
        if self.plate_type:
            return f"{self.plate_type} - {self.filename}"
        return self.filename
    
    @property
    def has_metadata(self) -> bool:
        """Check if the image has any optional metadata."""
        return bool(
            self.plate_type or 
            self.description or 
            self.is_character_example or 
            self.excluded_characters or 
            self.included_characters or 
            self.notes or 
            self.tags
        )
