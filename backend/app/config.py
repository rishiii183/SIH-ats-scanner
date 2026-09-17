import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "SIH ATS Scanner API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql://postgres:postgres@localhost:5432/sih_ats"
    )
    
    # Gemini AI API Key
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
    # Upload Storage Path (Local fallback if S3/R2 not configured)
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "./uploads")
    
    class Config:
        case_sensitive = True

settings = Settings()

# Ensure uploads directory exists
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
