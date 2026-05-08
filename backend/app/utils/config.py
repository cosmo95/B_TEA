"""
Configuration Settings for B_TEA Backend
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    """
    
    # Environment
    ENV: str = "development"
    DEBUG: bool = True
    
    # Server
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8000
    
    # Database
    DATABASE_URL: str = "postgresql://btea_user:btea_password@localhost:5432/btea_db"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
    ]
    
    # File Upload
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: set = {"csv", "pdf"}
    UPLOAD_DIRECTORY: str = "uploads"
    
    # Data Processing
    ANALYSIS_TIMEOUT: int = 300  # 5 minutes
    BATCH_SIZE: int = 1000
    
    # ML Model
    CATEGORIZATION_CONFIDENCE_THRESHOLD: float = 0.5
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/btea.log"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Singleton instance
settings = Settings()
