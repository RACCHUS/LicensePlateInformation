"""
User Image Manager for handling user-submitted license plate images.

Provides functionality to save, load, list, and delete user images
with their associated metadata stored in JSON sidecar files.
"""

import os
import sys
import shutil
import json
from pathlib import Path
from typing import List, Optional, Dict
from datetime import datetime
import hashlib

# Handle both relative and absolute imports for flexibility
try:
    from ..models.user_image import UserImage
except ImportError:
    from models.user_image import UserImage


class UserImageManager:
    """
    Manages user-submitted license plate images.
    
    Images are stored in a writable location:
    - For development: data/user_images/{STATE_CODE}/
    - For bundled app: Uses the app's executable directory for persistence
    """
    
    SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp', '.tiff'}
    
    def __init__(self, data_path: Optional[Path] = None):
        """
        Initialize the UserImageManager.
        
        Args:
            data_path: Path to the data directory. If None, determines automatically.
        """
        # Determine writable base path
        if getattr(sys, 'frozen', False):
            # Running as bundled executable - use the executable's directory
            # (not _MEIPASS which is temp and gets deleted)
            exe_dir = Path(sys.executable).parent
            self.data_path = exe_dir / 'data'
        elif data_path is not None:
            self.data_path = Path(data_path)
        else:
            # Default to project's data directory
            self.data_path = Path(__file__).parent.parent.parent / 'data'
        
        self.user_images_path = self.data_path / 'user_images'
        
        # Ensure base directory exists
        self.user_images_path.mkdir(parents=True, exist_ok=True)
    
    def _get_state_dir(self, state_code: str) -> Path:
        """Get the directory for a state's user images."""
        state_dir = self.user_images_path / state_code.upper()
        state_dir.mkdir(parents=True, exist_ok=True)
        return state_dir
    
    def _get_metadata_path(self, image_path: Path) -> Path:
        """Get the metadata JSON sidecar path for an image."""
        return image_path.with_suffix(image_path.suffix + '.meta.json')
    
    def _generate_unique_filename(self, state_code: str, original_name: str) -> str:
        """
        Generate a unique filename for the user image.
        
        Uses timestamp + hash to ensure uniqueness while keeping
        the original extension.
        """
        ext = Path(original_name).suffix.lower()
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        # Create short hash from original name + timestamp
        hash_input = f"{original_name}{timestamp}".encode()
        short_hash = hashlib.md5(hash_input).hexdigest()[:6]
        return f"user_{state_code}_{timestamp}_{short_hash}{ext}"
    
    def save_image(
        self,
        source_path: str | Path,
        state_code: str,
        plate_type: Optional[str] = None,
        description: Optional[str] = None,
        is_character_example: bool = False,
        excluded_characters: Optional[List[str]] = None,
        included_characters: Optional[List[str]] = None,
        notes: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> Optional[UserImage]:
        """
        Save a user image with optional metadata.
        
        Args:
            source_path: Path to the source image file
            state_code: Two-letter state code (e.g., 'FL', 'CA')
            plate_type: Optional plate type name
            description: Optional description
            is_character_example: Whether this is a character rule example
            excluded_characters: Characters to exclude/omit
            included_characters: Characters to include/allow
            notes: Optional notes
            tags: Optional list of tags
            
        Returns:
            UserImage object if successful, None if failed
        """
        source_path = Path(source_path)
        
        # Validate source file
        if not source_path.exists():
            print(f"[-] Source file not found: {source_path}")
            return None
        
        if source_path.suffix.lower() not in self.SUPPORTED_FORMATS:
            print(f"[-] Unsupported format: {source_path.suffix}")
            return None
        
        # Generate unique filename
        state_code = state_code.upper()
        filename = self._generate_unique_filename(state_code, source_path.name)
        
        # Get destination directory and path
        state_dir = self._get_state_dir(state_code)
        dest_path = state_dir / filename
        
        try:
            # Copy the image file
            shutil.copy2(source_path, dest_path)
            
            # Create UserImage object
            user_image = UserImage(
                filename=filename,
                state_code=state_code,
                plate_type=plate_type,
                description=description,
                is_character_example=is_character_example,
                excluded_characters=excluded_characters or [],
                included_characters=included_characters or [],
                notes=notes,
                tags=tags or [],
                source_path=str(source_path)
            )
            
            # Save metadata sidecar if there's any metadata
            if user_image.has_metadata:
                self._save_metadata(dest_path, user_image)
            
            print(f"[+] Saved user image: {dest_path.relative_to(self.data_path)}")
            return user_image
            
        except Exception as e:
            print(f"[-] Failed to save image: {e}")
            # Clean up if partial save
            if dest_path.exists():
                dest_path.unlink()
            return None
    
    def _save_metadata(self, image_path: Path, user_image: UserImage):
        """Save metadata to JSON sidecar file."""
        metadata_path = self._get_metadata_path(image_path)
        with open(metadata_path, 'w', encoding='utf-8') as f:
            f.write(user_image.to_json())
    
    def get_image_metadata(self, state_code: str, filename: str) -> Optional[UserImage]:
        """
        Load metadata for a user image.
        
        Args:
            state_code: Two-letter state code
            filename: Image filename
            
        Returns:
            UserImage with metadata if found, basic UserImage otherwise
        """
        state_dir = self._get_state_dir(state_code)
        image_path = state_dir / filename
        
        if not image_path.exists():
            return None
        
        metadata_path = self._get_metadata_path(image_path)
        
        if metadata_path.exists():
            try:
                with open(metadata_path, 'r', encoding='utf-8') as f:
                    return UserImage.from_json(f.read())
            except (json.JSONDecodeError, KeyError) as e:
                print(f"[-] Failed to load metadata for {filename}: {e}")
        
        # Return basic UserImage without metadata
        return UserImage(filename=filename, state_code=state_code.upper())
    
    def get_user_images(self, state_code: str) -> List[Path]:
        """
        Get list of user image paths for a state.
        
        Args:
            state_code: Two-letter state code
            
        Returns:
            List of Path objects for user images
        """
        state_dir = self.user_images_path / state_code.upper()
        
        if not state_dir.exists():
            return []
        
        images = []
        for file in state_dir.iterdir():
            if file.is_file() and file.suffix.lower() in self.SUPPORTED_FORMATS:
                images.append(file)
        
        return sorted(images, key=lambda p: p.stat().st_mtime, reverse=True)
    
    def get_all_user_images(self) -> Dict[str, List[Path]]:
        """
        Get all user images organized by state.
        
        Returns:
            Dictionary mapping state codes to lists of image paths
        """
        result = {}
        
        if not self.user_images_path.exists():
            return result
        
        for state_dir in self.user_images_path.iterdir():
            if state_dir.is_dir() and len(state_dir.name) == 2:
                images = self.get_user_images(state_dir.name)
                if images:
                    result[state_dir.name] = images
        
        return result
    
    def delete_user_image(self, state_code: str, filename: str) -> bool:
        """
        Delete a user image and its metadata.
        
        Args:
            state_code: Two-letter state code
            filename: Image filename
            
        Returns:
            True if deleted successfully, False otherwise
        """
        state_dir = self.user_images_path / state_code.upper()
        image_path = state_dir / filename
        
        if not image_path.exists():
            print(f"[-] Image not found: {image_path}")
            return False
        
        try:
            # Delete image
            image_path.unlink()
            
            # Delete metadata if exists
            metadata_path = self._get_metadata_path(image_path)
            if metadata_path.exists():
                metadata_path.unlink()
            
            print(f"[+] Deleted user image: {filename}")
            return True
            
        except Exception as e:
            print(f"[-] Failed to delete image: {e}")
            return False
    
    def update_metadata(
        self,
        state_code: str,
        filename: str,
        **kwargs
    ) -> Optional[UserImage]:
        """
        Update metadata for an existing user image.
        
        Args:
            state_code: Two-letter state code
            filename: Image filename
            **kwargs: Metadata fields to update
            
        Returns:
            Updated UserImage if successful, None otherwise
        """
        user_image = self.get_image_metadata(state_code, filename)
        
        if user_image is None:
            return None
        
        # Update fields
        for key, value in kwargs.items():
            if hasattr(user_image, key):
                setattr(user_image, key, value)
        
        # Save updated metadata
        state_dir = self._get_state_dir(state_code)
        image_path = state_dir / filename
        self._save_metadata(image_path, user_image)
        
        return user_image
    
    def get_user_images_dir(self, state_code: str) -> Path:
        """
        Get the user images directory path for a state.
        Creates the directory if it doesn't exist.
        
        Args:
            state_code: Two-letter state code
            
        Returns:
            Path to the state's user images directory
        """
        return self._get_state_dir(state_code)
    
    def has_user_images(self, state_code: str) -> bool:
        """Check if a state has any user images."""
        return len(self.get_user_images(state_code)) > 0
    
    def get_image_count(self, state_code: Optional[str] = None) -> int:
        """
        Get count of user images.
        
        Args:
            state_code: If provided, count only for this state
            
        Returns:
            Number of user images
        """
        if state_code:
            return len(self.get_user_images(state_code))
        
        total = 0
        for images in self.get_all_user_images().values():
            total += len(images)
        return total
