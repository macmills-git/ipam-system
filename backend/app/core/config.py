from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://ipam:ipam_password@localhost:5432/ipam"
    DATABASE_TEST_URL: str = "postgresql://ipam:ipam_password@localhost:5432/ipam_test"
    
    # Security
    SECRET_KEY: str = "change-this-to-a-secure-random-string-min-32-characters-long"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # Scanner
    SCANNER_ENABLED: bool = True
    SCANNER_INTERVAL_SECONDS: int = 300
    SCANNER_TIMEOUT_SECONDS: int = 2
    SCANNER_CONCURRENT_SCANS: int = 50
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 100
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Monitoring
    PROMETHEUS_ENABLED: bool = True
    METRICS_PORT: int = 9090
    
    class Config:
        env_file = ".env"
        case_sensitive = True
    
    @property
    def CORS_ORIGINS(self) -> List[str]:
        origins = os.getenv("CORS_ORIGINS", "http://localhost:3000")
        return [origin.strip() for origin in origins.split(",")]

settings = Settings()
