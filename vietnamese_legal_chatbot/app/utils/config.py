"""
Configuration management for Vietnamese Legal AI Chatbot
Quản lý cấu hình cho Chatbot AI Pháp lý Việt Nam
"""

import os
from typing import List, Optional
from pydantic import Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # API Keys - Chat Model
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    openai_api_base: str = Field(default="https://api.openai.com/v1", env="OPENAI_API_BASE")
    openai_organization_id: Optional[str] = Field(default=None, env="OPENAI_ORGANIZATION_ID")
    
    # API Keys - Embedding Model (separate)
    openai_embedding_api_key: Optional[str] = Field(default=None, env="OPENAI_EMBEDDING_API_KEY")
    openai_embedding_api_base: str = Field(default="https://api.openai.com/v1", env="OPENAI_EMBEDDING_API_BASE")
    
    # Pinecone Configuration
    pinecone_api_key: str = Field(..., env="PINECONE_API_KEY")
    
    # Pinecone Configuration
    pinecone_environment: str = Field(..., env="PINECONE_ENVIRONMENT")
    pinecone_index_name: str = Field(default="vietnamese-legal-docs", env="PINECONE_INDEX_NAME")
    pinecone_dimension: int = Field(default=1536, env="PINECONE_DIMENSION")
    
    # Application Configuration
    app_name: str = Field(default="Vietnamese Legal AI Chatbot", env="APP_NAME")
    app_version: str = Field(default="1.0.0", env="APP_VERSION")
    debug: bool = Field(default=False, env="DEBUG")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    
    # Server Configuration
    fastapi_host: str = Field(default="0.0.0.0", env="FASTAPI_HOST")
    fastapi_port: int = Field(default=8000, env="FASTAPI_PORT")
    streamlit_port: int = Field(default=8501, env="STREAMLIT_PORT")
    
    # AI Configuration
    chat_model: str = Field(default="gpt-4o-mini", env="CHAT_MODEL")
    embedding_model: str = Field(default="text-embedding-3-small", env="EMBEDDING_MODEL")
    max_tokens: int = Field(default=4000, env="MAX_TOKENS")
    temperature: float = Field(default=0.1, env="TEMPERATURE")
    
    # Vietnamese Legal Configuration
    default_language: str = Field(default="vietnamese", env="DEFAULT_LANGUAGE")
    legal_domains: str = Field(
        default="hien_phap,dan_su,hinh_su,lao_dong,thuong_mai,hanh_chinh,thue,bat_dong_san",
        env="LEGAL_DOMAINS"
    )
    
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
    
    # Data Paths
    legal_documents_path: str = Field(default="./app/data/legal_documents", env="LEGAL_DOCUMENTS_PATH")
    processed_data_path: str = Field(default="./app/data/processed", env="PROCESSED_DATA_PATH")
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    @property
    def legal_domains_list(self) -> List[str]:
        """Get legal domains as a list"""
        if isinstance(self.legal_domains, str):
            return [domain.strip() for domain in self.legal_domains.split(",")]
        return self.legal_domains


class VietnameseLegalDomains:
    """Vietnamese legal domain mappings"""
    
    DOMAIN_MAPPING = {
        "hien_phap": {
            "name": "Hiến pháp",
            "name_en": "Constitution",
            "description": "Luật cơ bản của Nhà nước Cộng hòa xã hội chủ nghĩa Việt Nam"
        },
        "dan_su": {
            "name": "Bộ luật Dân sự",
            "name_en": "Civil Code",
            "description": "Các quy định về quan hệ dân sự, tài sản, hợp đồng"
        },
        "hinh_su": {
            "name": "Bộ luật Hình sự",
            "name_en": "Criminal Code", 
            "description": "Các quy định về tội phạm và hình phạt"
        },
        "lao_dong": {
            "name": "Bộ luật Lao động",
            "name_en": "Labor Code",
            "description": "Các quy định về quan hệ lao động, hợp đồng lao động"
        },
        "thuong_mai": {
            "name": "Luật Thương mại",
            "name_en": "Commercial Law",
            "description": "Các quy định về hoạt động thương mại, kinh doanh"
        },
        "hanh_chinh": {
            "name": "Luật Hành chính",
            "name_en": "Administrative Law",
            "description": "Các quy định về quản lý nhà nước và thủ tục hành chính"
        },
        "thue": {
            "name": "Luật Thuế",
            "name_en": "Tax Law",
            "description": "Các quy định về thuế và nghĩa vụ tài chính"
        },
        "bat_dong_san": {
            "name": "Luật Bất động sản",
            "name_en": "Real Estate Law",
            "description": "Các quy định về quyền sở hữu và giao dịch bất động sản"
        }
    }
    
    @classmethod
    def get_domain_name(cls, domain_code: str, language: str = "vietnamese") -> str:
        """Get domain name by code and language"""
        domain_info = cls.DOMAIN_MAPPING.get(domain_code, {})
        if language == "english":
            return domain_info.get("name_en", domain_code)
        return domain_info.get("name", domain_code)
    
    @classmethod
    def get_all_domains(cls) -> List[str]:
        """Get all available domain codes"""
        return list(cls.DOMAIN_MAPPING.keys())
    
    @classmethod
    def is_valid_domain(cls, domain_code: str) -> bool:
        """Check if domain code is valid"""
        return domain_code in cls.DOMAIN_MAPPING


# Global settings instance
settings = Settings()

# Validate required API keys
if not settings.openai_api_key or settings.openai_api_key == "your_openai_api_key_here":
    raise ValueError("OPENAI_API_KEY must be set in environment variables or .env file")

if not settings.pinecone_api_key or settings.pinecone_api_key == "your_pinecone_api_key_here":
    raise ValueError("PINECONE_API_KEY must be set in environment variables or .env file")

if not settings.secret_key or settings.secret_key == "your_secret_key_here":
    raise ValueError("SECRET_KEY must be set in environment variables or .env file")
