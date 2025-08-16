"""
Simplified Configuration for Vietnamese Legal AI Chatbot
Cấu hình đơn giản cho Chatbot AI Pháp lý Việt Nam
"""

import os
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings(BaseSettings):
    """Simplified application settings"""
    
    # API Keys
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    openai_api_base: str = Field(default="https://api.openai.com/v1", env="OPENAI_API_BASE")
    openai_organization_id: Optional[str] = Field(default=None, env="OPENAI_ORGANIZATION_ID")
    
    # Separate Embedding API Configuration  
    openai_embedding_api_key: str = Field(..., env="OPENAI_EMBEDDING_API_KEY")
    openai_embedding_api_base: str = Field(default="https://api.openai.com/v1", env="OPENAI_EMBEDDING_API_BASE")
    embedding_organization_id: Optional[str] = Field(default=None, env="EMBEDDING_ORGANIZATION_ID")
    
    pinecone_api_key: str = Field(..., env="PINECONE_API_KEY")
    
    # Security
    secret_key: str = Field(..., env="SECRET_KEY")
    
    # Pinecone Configuration
    pinecone_environment: str = Field(default="us-east-1-aws", env="PINECONE_ENVIRONMENT")
    pinecone_index_name: str = Field(default="vietnamese-legal-docs", env="PINECONE_INDEX_NAME")
    pinecone_dimension: int = Field(default=1536, env="PINECONE_DIMENSION")
    
    # Application Configuration
    app_name: str = Field(default="Vietnamese Legal AI Chatbot", env="APP_NAME")
    app_version: str = Field(default="2.0.0", env="APP_VERSION")
    debug: bool = Field(default=True, env="DEBUG")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    
    # Server Configuration
    fastapi_host: str = Field(default="0.0.0.0", env="FASTAPI_HOST")
    fastapi_port: int = Field(default=8000, env="FASTAPI_PORT")
    streamlit_port: int = Field(default=8501, env="STREAMLIT_PORT")
    
    # AI Configuration
    embedding_model: str = Field(default="text-embedding-3-small", env="EMBEDDING_MODEL")
    max_tokens: int = Field(default=4000, env="MAX_TOKENS")
    temperature: float = Field(default=0.3, env="TEMPERATURE")
    
    # Security
    secret_key: str = Field(..., env="SECRET_KEY")
    access_token_expire_minutes: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    
    # Performance Configuration
    max_concurrent_requests: int = Field(default=100, env="MAX_CONCURRENT_REQUESTS")
    response_timeout_seconds: int = Field(default=30, env="RESPONSE_TIMEOUT_SECONDS")
    pinecone_batch_size: int = Field(default=100, env="PINECONE_BATCH_SIZE")
    
    # Logging Configuration
    log_file_path: str = Field(default="./logs/app.log", env="LOG_FILE_PATH")
    log_rotation: str = Field(default="1 week", env="LOG_ROTATION")
    log_retention: str = Field(default="30 days", env="LOG_RETENTION")
    
    # Vietnamese Legal Configuration
    default_language: str = Field(default="vietnamese", env="DEFAULT_LANGUAGE")
    legal_domains: str = Field(
        default="hien_phap,dan_su,hinh_su,lao_dong,thuong_mai,hanh_chinh,thue,bat_dong_san",
        env="LEGAL_DOMAINS"
    )
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # Allow extra fields from .env file but ignore them


# Global settings instance
settings = Settings()

# Validate required API keys (with more flexible validation)
def validate_api_keys():
    """Validate that API keys are properly configured"""
    errors = []
    
    if not settings.openai_api_key or settings.openai_api_key.startswith("your_") or settings.openai_api_key.startswith("sk-test"):
        errors.append("OPENAI_API_KEY must be set to a valid API key")
    
    if not settings.embedding_api_key or settings.embedding_api_key.startswith("your_") or settings.embedding_api_key.startswith("sk-test"):
        errors.append("EMBEDDING_API_KEY must be set to a valid API key")
    
    if not settings.pinecone_api_key or settings.pinecone_api_key.startswith("your_") or settings.pinecone_api_key.startswith("test-key"):
        errors.append("PINECONE_API_KEY must be set to a valid API key")
    
    if not settings.secret_key or settings.secret_key.startswith("your_") or len(settings.secret_key) < 32:
        errors.append("SECRET_KEY must be set to a secure key (minimum 32 characters)")
    
    return errors

# Check for validation errors but don't raise exceptions (for testing purposes)
validation_errors = validate_api_keys()
if validation_errors:
    print("⚠️  Configuration warnings:")
    for error in validation_errors:
        print(f"   - {error}")


def get_simple_config():
    """Get simple configuration instance"""
    return settings
