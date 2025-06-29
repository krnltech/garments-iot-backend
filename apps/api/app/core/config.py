"""
Core configuration and settings
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    """Application settings"""
    
    # JWT Configuration
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database Configuration
    TIMESCALE_USER: str = os.getenv("TIMESCALE_USER", "postgres")
    TIMESCALE_PASSWORD: str = os.getenv("TIMESCALE_PASSWORD", "password")
    TIMESCALE_HOST: str = os.getenv("TIMESCALE_HOST", "localhost")
    TIMESCALE_PORT: str = os.getenv("TIMESCALE_PORT", "5432")
    TIMESCALE_DB: str = os.getenv("TIMESCALE_DB", "metrics")
    
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.TIMESCALE_USER}:{self.TIMESCALE_PASSWORD}@{self.TIMESCALE_HOST}:{self.TIMESCALE_PORT}/{self.TIMESCALE_DB}"
    
    # CORS Configuration
    CORS_ORIGINS: list = ["*"]  # Configure appropriately for production
    
    # App Configuration
    APP_NAME: str = "Garments IoT Backend API"
    APP_DESCRIPTION: str = "Backend API for IoT-integrated garments production tracking with OAuth2 authentication"
    VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

settings = Settings()
