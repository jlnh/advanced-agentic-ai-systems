from pydantic_settings import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # OpenAI Configuration
    openai_api_key: str
    openai_model: str = "gpt-3.5-turbo"
    
    # LangChain Configuration
    langchain_api_key: Optional[str] = None
    langchain_project: str = "advanced-agentic-ai"
    langchain_tracing_v2: bool = True
    
    # Redis Configuration
    redis_url: str = "redis://localhost:6379"
    
    # API Configuration
    api_keys: List[str] = ["demo-key-123"]
    allowed_origins: List[str] = ["*"]
    
    # Rate Limiting
    default_rate_limit: int = 10
    rate_limit_window: int = 60
    
    # Monitoring
    log_level: str = "INFO"
    sentry_dsn: Optional[str] = None
    
    # Development
    debug: bool = False
    environment: str = "development"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

def get_settings() -> Settings:
    """Get application settings"""
    return Settings()