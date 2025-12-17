"""
Custom exceptions for License Plate Information System
Provides specific exception types for different error categories
"""
from typing import Optional


class LicensePlateError(Exception):
    """Base exception for all application errors"""
    
    def __init__(self, message: str, details: Optional[str] = None):
        self.message = message
        self.details = details
        super().__init__(self.message)
    
    def __str__(self):
        if self.details:
            return f"{self.message} - {self.details}"
        return self.message


class DatabaseError(LicensePlateError):
    """Exception raised for database operation failures"""
    
    def __init__(self, message: str, operation: Optional[str] = None, details: Optional[str] = None):
        self.operation = operation
        super().__init__(message, details)
    
    def __str__(self):
        parts = [self.message]
        if self.operation:
            parts.append(f"Operation: {self.operation}")
        if self.details:
            parts.append(f"Details: {self.details}")
        return " | ".join(parts)


class DatabaseConnectionError(DatabaseError):
    """Exception raised when database connection fails"""
    pass


class DatabaseQueryError(DatabaseError):
    """Exception raised when a database query fails"""
    pass


class DataLoadError(LicensePlateError):
    """Exception raised when loading data from files fails"""
    
    def __init__(self, message: str, file_path: Optional[str] = None, details: Optional[str] = None):
        self.file_path = file_path
        super().__init__(message, details)
    
    def __str__(self):
        parts = [self.message]
        if self.file_path:
            parts.append(f"File: {self.file_path}")
        if self.details:
            parts.append(f"Details: {self.details}")
        return " | ".join(parts)


class JSONParseError(DataLoadError):
    """Exception raised when JSON parsing fails"""
    pass


class ImageLoadError(LicensePlateError):
    """Exception raised when loading images fails"""
    
    def __init__(self, message: str, image_path: Optional[str] = None, details: Optional[str] = None):
        self.image_path = image_path
        super().__init__(message, details)


class ImageNotFoundError(ImageLoadError):
    """Exception raised when image file is not found"""
    pass


class UnsupportedImageFormatError(ImageLoadError):
    """Exception raised when image format is not supported"""
    pass


class SearchError(LicensePlateError):
    """Exception raised when search operations fail"""
    
    def __init__(self, message: str, query: Optional[str] = None, details: Optional[str] = None):
        self.query = query
        super().__init__(message, details)


class InvalidSearchQueryError(SearchError):
    """Exception raised when search query is invalid"""
    pass


class ConfigurationError(LicensePlateError):
    """Exception raised for configuration-related errors"""
    pass


class ValidationError(LicensePlateError):
    """Exception raised when data validation fails"""
    
    def __init__(self, message: str, field: Optional[str] = None, value: Optional[str] = None, details: Optional[str] = None):
        self.field = field
        self.value = value
        super().__init__(message, details)
