"""
Logging Configuration for B_TEA Backend
"""

import logging
import os
from logging.handlers import RotatingFileHandler
from app.utils.config import settings


def get_logger(name: str) -> logging.Logger:
    """
    Get configured logger instance
    
    Args:
        name: Logger name (usually __name__)
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(settings.LOG_LEVEL)
    
    # Prevent duplicate handlers
    if logger.handlers:
        return logger
    
    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(settings.LOG_LEVEL)
    
    # File Handler (with rotation)
    os.makedirs("logs", exist_ok=True)
    file_handler = RotatingFileHandler(
        settings.LOG_FILE,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(settings.LOG_LEVEL)
    
    # Formatter
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    # Add handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger
