"""
Logging utility for License Plate Information System
Provides consistent logging across the application
"""

import logging
import os
import sys
from datetime import datetime
from typing import Optional


# Global logger instance
_logger: Optional[logging.Logger] = None


def setup_logger(
    name: str = 'LicensePlateApp',
    log_file: Optional[str] = None,
    level: int = logging.INFO,
    console_output: bool = True
) -> logging.Logger:
    """
    Set up and configure the application logger.
    
    Args:
        name: Logger name
        log_file: Path to log file (optional, defaults to app.log in app directory)
        level: Logging level (default INFO)
        console_output: Whether to also output to console
        
    Returns:
        Configured logger instance
    """
    global _logger
    
    if _logger is not None:
        return _logger
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Prevent duplicate handlers
    if logger.handlers:
        return logger
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # File handler
    if log_file is None:
        # Get app directory
        if getattr(sys, 'frozen', False):
            app_dir = os.path.dirname(sys.executable)
        else:
            app_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        log_dir = os.path.join(app_dir, 'logs')
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, 'app.log')
    
    try:
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except (OSError, PermissionError) as e:
        # If we can't write to file, just use console
        print(f"Warning: Could not create log file: {e}")
    
    # Console handler
    if console_output:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    _logger = logger
    return logger


def get_logger() -> logging.Logger:
    """
    Get the application logger, creating it if necessary.
    
    Returns:
        Logger instance
    """
    global _logger
    if _logger is None:
        _logger = setup_logger()
    return _logger


def log_error(message: str, exc: Optional[Exception] = None, extra_info: Optional[dict] = None):
    """
    Log an error with optional exception details.
    
    Args:
        message: Error message
        exc: Exception object (optional)
        extra_info: Additional context information
    """
    logger = get_logger()
    
    log_message = message
    if extra_info:
        log_message += f" | Context: {extra_info}"
    
    if exc:
        logger.error(log_message, exc_info=True)
    else:
        logger.error(log_message)


def log_warning(message: str, extra_info: Optional[dict] = None):
    """
    Log a warning message.
    
    Args:
        message: Warning message
        extra_info: Additional context information
    """
    logger = get_logger()
    
    log_message = message
    if extra_info:
        log_message += f" | Context: {extra_info}"
    
    logger.warning(log_message)


def log_info(message: str):
    """
    Log an informational message.
    
    Args:
        message: Info message
    """
    logger = get_logger()
    logger.info(message)


def log_debug(message: str):
    """
    Log a debug message.
    
    Args:
        message: Debug message
    """
    logger = get_logger()
    logger.debug(message)


class ErrorHandler:
    """Context manager for handling errors with logging"""
    
    def __init__(self, operation: str, reraise: bool = True, default_return=None):
        """
        Initialize error handler.
        
        Args:
            operation: Description of the operation being performed
            reraise: Whether to re-raise exceptions after logging
            default_return: Value to return if exception occurs and not reraising
        """
        self.operation = operation
        self.reraise = reraise
        self.default_return = default_return
        self.exception = None
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val is not None:
            self.exception = exc_val
            log_error(f"Error during {self.operation}: {exc_val}", exc=exc_val)
            
            if not self.reraise:
                return True  # Suppress exception
        
        return False
