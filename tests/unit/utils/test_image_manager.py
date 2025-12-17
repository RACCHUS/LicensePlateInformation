"""
Unit tests for image_manager.py
Tests for LicensePlateImageManager class
"""

import pytest
from pathlib import Path
from PIL import Image
from src.utils.image_manager import LicensePlateImageManager


# ============================================================================
# INITIALIZATION TESTS
# ============================================================================

class TestImageManagerInit:
    """Test cases for ImageManager initialization"""
    
    def test_init_with_default_root(self):
        """Test initialization with default project root"""
        manager = LicensePlateImageManager()
        assert manager is not None
        assert manager.project_root is not None
    
    def test_init_with_custom_root(self, tmp_path):
        """Test initialization with custom project root"""
        manager = LicensePlateImageManager(str(tmp_path))
        assert manager.project_root == tmp_path
    
    def test_images_directory_created(self, tmp_path):
        """Test that images directory is created"""
        manager = LicensePlateImageManager(str(tmp_path))
        assert manager.images_dir.exists()
    
    def test_supported_formats(self):
        """Test that supported formats are defined"""
        manager = LicensePlateImageManager()
        assert isinstance(manager.supported_formats, set)
        assert '.jpg' in manager.supported_formats
        assert '.png' in manager.supported_formats


# ============================================================================
# STATE STRUCTURE TESTS
# ============================================================================

class TestCreateStateStructure:
    """Test cases for create_state_structure()"""
    
    def test_create_state_structure(self, tmp_path):
        """Test creating state directory structure"""
        manager = LicensePlateImageManager(str(tmp_path))
        state_dir = manager.create_state_structure('FL')
        
        assert state_dir.exists()
        assert (state_dir / 'plates').exists()
        assert (state_dir / 'characters').exists()
        assert (state_dir / 'stickers').exists()
    
    def test_create_state_structure_uppercase(self, tmp_path):
        """Test that state abbreviation is converted to uppercase"""
        manager = LicensePlateImageManager(str(tmp_path))
        state_dir = manager.create_state_structure('fl')
        
        assert 'FL' in str(state_dir)
    
    def test_create_state_structure_idempotent(self, tmp_path):
        """Test that structure creation is idempotent"""
        manager = LicensePlateImageManager(str(tmp_path))
        
        # Create twice
        state_dir1 = manager.create_state_structure('CA')
        state_dir2 = manager.create_state_structure('CA')
        
        assert state_dir1 == state_dir2
        assert state_dir1.exists()


# ============================================================================
# IMAGE IMPORT TESTS
# ============================================================================

class TestImportImage:
    """Test cases for import_image()"""
    
    def test_import_image_basic(self, tmp_path, sample_image_dir):
        """Test basic image import"""
        manager = LicensePlateImageManager(str(tmp_path))
        
        # Create source image
        source_img = tmp_path / 'source.jpg'
        img = Image.new('RGB', (100, 50), color='blue')
        img.save(source_img)
        
        result = manager.import_image(
            source_img,
            'FL',
            'plates',
            subcategory='passenger'
        )
        
        assert result is True
    
    def test_import_image_invalid_source(self, tmp_path):
        """Test import with non-existent source file"""
        manager = LicensePlateImageManager(str(tmp_path))
        
        result = manager.import_image(
            tmp_path / 'nonexistent.jpg',
            'FL',
            'plates'
        )
        
        assert result is False
    
    def test_import_image_unsupported_format(self, tmp_path):
        """Test import with unsupported file format"""
        manager = LicensePlateImageManager(str(tmp_path))
        
        # Create unsupported file
        source_file = tmp_path / 'source.txt'
        source_file.touch()
        
        result = manager.import_image(
            source_file,
            'FL',
            'plates'
        )
        
        assert result is False
    
    def test_import_image_invalid_category(self, tmp_path):
        """Test import with invalid category"""
        manager = LicensePlateImageManager(str(tmp_path))
        
        # Create source image
        source_img = tmp_path / 'source.jpg'
        img = Image.new('RGB', (100, 50), color='blue')
        img.save(source_img)
        
        result = manager.import_image(
            source_img,
            'FL',
            'invalid_category'
        )
        
        assert result is False


# ============================================================================
# IMAGE LISTING TESTS
# ============================================================================

class TestListImages:
    """Test cases for list_images()"""
    
    def test_list_images_empty(self, tmp_path):
        """Test listing images with no images"""
        manager = LicensePlateImageManager(str(tmp_path))
        images = manager.list_images()
        
        assert isinstance(images, list)
    
    def test_list_images_by_state(self, tmp_path):
        """Test listing images filtered by state"""
        manager = LicensePlateImageManager(str(tmp_path))
        images = manager.list_images(state_abbrev='FL')
        
        assert isinstance(images, list)


# ============================================================================
# IMAGE METADATA TESTS
# ============================================================================

class TestImageMetadata:
    """Test cases for image metadata operations"""
    
    def test_get_image_metadata_nonexistent(self, tmp_path):
        """Test getting metadata for non-existent image"""
        manager = LicensePlateImageManager(str(tmp_path))
        metadata = manager.get_image_metadata(str(tmp_path / 'nonexistent.jpg'))
        
        # Should return graceful fallback metadata
        assert metadata is not None
        assert metadata['category'] == 'unknown'
        assert metadata['description'] == 'No metadata file found'


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestImageManagerIntegration:
    """Integration tests for image manager"""
    
    def test_full_workflow(self, tmp_path):
        """Test complete workflow of importing and managing images"""
        manager = LicensePlateImageManager(str(tmp_path))
        
        # Create state structure
        state_dir = manager.create_state_structure('TX')
        assert state_dir.exists()
        
        # Create and import image
        source_img = tmp_path / 'test_plate.jpg'
        img = Image.new('RGB', (100, 50), color='red')
        img.save(source_img)
        
        result = manager.import_image(
            source_img,
            'TX',
            'plates',
            subcategory='passenger',
            description='Test plate image'
        )
        
        # Verify success
        assert result is True
