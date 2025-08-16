"""
Demo Configuration for Vietnamese Legal Chatbot
Simplified configuration for development and demo purposes
"""

import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class DemoSettings:
    """Simplified settings for demo environment"""
    
    # API Configuration - Chat Model
    openai_chat_api_key: str = os.getenv("OPENAI_API_KEY", "demo-chat-key")
    openai_chat_api_base: str = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
    
    # API Configuration - Embedding Model
    openai_embedding_api_key: str = os.getenv("OPENAI_EMBEDDING_API_KEY", "demo-embedding-key")
    openai_embedding_api_base: str = os.getenv("OPENAI_EMBEDDING_API_BASE", "https://api.openai.com/v1")
    
    # Pinecone Configuration
    pinecone_api_key: str = os.getenv("PINECONE_API_KEY", "demo-pinecone-key")
    pinecone_environment: str = os.getenv("PINECONE_ENVIRONMENT", "us-east-1")
    pinecone_index_name: str = os.getenv("PINECONE_INDEX_NAME", "vietnamese-legal-docs")
    
    # SerpAPI Configuration
    serp_api_key: str = os.getenv("SERP_API_KEY", "demo-serp-key")
    
    # Model Configuration
    chat_model: str = "gpt-4o-mini"
    embedding_model: str = "text-embedding-3-small"  # Use the correct API key now
    temperature: float = 0.1
    max_tokens: int = 1000
    top_p: float = 0.9
    
    # RAG Configuration
    top_k: int = 5
    chunk_size: int = 1000
    chunk_overlap: int = 200
    similarity_threshold: float = 0.7
    
    # Vietnamese Legal Configuration
    vietnamese_nlp_enabled: bool = True
    legal_term_extraction: bool = True
    entity_recognition: bool = True
    language_detection_threshold: float = 0.8
    
    # Regional Configuration
    default_region: str = "south"
    vietnamese_regions: list = None
    region_specialties_enabled: bool = True
    
    # Document Configuration
    document_hierarchy: list = None
    
    # Logging
    log_level: str = "INFO"
    debug_mode: bool = True
    
    def __post_init__(self):
        """Initialize default values"""
        if self.vietnamese_regions is None:
            self.vietnamese_regions = ["north", "central", "south", "special_zones"]
        
        if self.document_hierarchy is None:
            self.document_hierarchy = [
                "hien_phap", "luat", "nghi_quyet", "nghi_dinh", 
                "quyet_dinh", "thong_tu", "quyet_dinh_bo"
            ]


# Global demo settings instance
demo_settings = DemoSettings()


def get_demo_config():
    """Get demo configuration with environment overrides"""
    config = DemoSettings()
    
    # Override with environment variables if available
    config.openai_chat_api_key = os.getenv("OPENAI_CHAT_API_KEY", config.openai_chat_api_key)
    config.openai_chat_api_base = os.getenv("OPENAI_CHAT_API_BASE", config.openai_chat_api_base)
    config.openai_embedding_api_key = os.getenv("OPENAI_EMBEDDING_API_KEY", config.openai_embedding_api_key)
    config.openai_embedding_api_base = os.getenv("OPENAI_EMBEDDING_API_BASE", config.openai_embedding_api_base)
    config.pinecone_api_key = os.getenv("PINECONE_API_KEY", config.pinecone_api_key)
    config.pinecone_environment = os.getenv("PINECONE_ENVIRONMENT", config.pinecone_environment)
    config.pinecone_index_name = os.getenv("PINECONE_INDEX_NAME", config.pinecone_index_name)
    
    return config


def validate_api_keys():
    """Validate that required API keys are available"""
    config = get_demo_config()
    
    issues = []
    
    if config.openai_chat_api_key == "demo-chat-key" or not config.openai_chat_api_key:
        issues.append("OpenAI Chat API key not configured")
    
    if config.openai_embedding_api_key == "demo-embedding-key" or not config.openai_embedding_api_key:
        issues.append("OpenAI Embedding API key not configured")
    
    if config.pinecone_api_key == "demo-pinecone-key" or not config.pinecone_api_key:
        issues.append("Pinecone API key not configured")
    
    return issues

# Global demo config instance
demo_settings = get_demo_config()

# Print configuration status on import
validation_issues = validate_api_keys()
if validation_issues:
    print("⚠️  Demo Configuration Issues:")
    for issue in validation_issues:
        print(f"   - {issue}")
else:
    print("✅ Demo configuration loaded successfully")
    print(f"   - Chat API: {demo_settings.openai_chat_api_key[:15]}...")
    print(f"   - Embedding API: {demo_settings.openai_embedding_api_key[:15]}...")
    print(f"   - Pinecone: {demo_settings.pinecone_api_key[:15]}...")

if __name__ == "__main__":
    """Test configuration"""
    config = get_demo_config()
    print("Demo Configuration:")
    print(f"  Chat Model: {config.chat_model}")
    print(f"  Embedding Model: {config.embedding_model}")
    print(f"  Temperature: {config.temperature}")
    print(f"  Top K: {config.top_k}")
    print(f"  Vietnamese NLP: {config.vietnamese_nlp_enabled}")
    print(f"  Default Region: {config.default_region}")
    
    issues = validate_api_keys()
    if issues:
        print("\nConfiguration Issues:")
        for issue in issues:
            print(f"  ⚠️ {issue}")
    else:
        print("\n✅ Configuration valid!")
