"""
API Key Management for Vietnamese Legal Chatbot
Quản lý API Keys cho Chatbot Pháp lý Việt Nam
"""

import os
from typing import Dict, Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class APIKeyManager:
    """Quản lý API keys riêng biệt cho các dịch vụ khác nhau"""
    
    def __init__(self):
        self.chat_api_key = None
        self.embedding_api_key = None
        self.pinecone_api_key = None
        self._load_keys()
    
    def _load_keys(self):
        """Load API keys từ environment variables"""
        # Chat API Key (OpenAI GPT)
        self.chat_api_key = os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_CHAT_API_KEY")
        
        # Embedding API Key (có thể khác với chat key)
        self.embedding_api_key = (
            os.getenv("OPENAI_EMBEDDING_API_KEY") or 
            os.getenv("OPENAI_API_KEY")  # Fallback to main key
        )
        
        # Pinecone API Key
        self.pinecone_api_key = os.getenv("PINECONE_API_KEY")
        
        logger.info("API keys loaded from environment")
    
    def get_chat_config(self) -> Dict[str, str]:
        """Lấy config cho chat model"""
        return {
            "api_key": self.chat_api_key,
            "api_base": os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1"),
            "model": os.getenv("CHAT_MODEL", "gpt-4o-mini")
        }
    
    def get_embedding_config(self) -> Dict[str, str]:
        """Lấy config cho embedding model"""
        return {
            "api_key": self.embedding_api_key,
            "api_base": os.getenv("OPENAI_EMBEDDING_API_BASE", "https://api.openai.com/v1"),
            "model": os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002")
        }
    
    def get_pinecone_config(self) -> Dict[str, str]:
        """Lấy config cho Pinecone"""
        return {
            "api_key": self.pinecone_api_key,
            "environment": os.getenv("PINECONE_ENVIRONMENT", "us-west1-gcp"),
            "index_name": os.getenv("PINECONE_INDEX_NAME", "vietnamese-legal-docs")
        }
    
    def validate_keys(self) -> Tuple[bool, Dict[str, bool]]:
        """Kiểm tra tính hợp lệ của các API keys"""
        validation = {
            "chat_api_valid": self._is_valid_key(self.chat_api_key),
            "embedding_api_valid": self._is_valid_key(self.embedding_api_key),
            "pinecone_api_valid": self._is_valid_key(self.pinecone_api_key)
        }
        
        all_valid = all(validation.values())
        return all_valid, validation
    
    def _is_valid_key(self, key: Optional[str]) -> bool:
        """Kiểm tra key có hợp lệ không"""
        if not key:
            return False
        if key.startswith("demo-") or key == "test-key":
            return False
        return len(key.strip()) > 10
    
    def get_missing_keys(self) -> list:
        """Lấy danh sách các keys bị thiếu"""
        missing = []
        
        if not self._is_valid_key(self.chat_api_key):
            missing.append("Chat API Key (OPENAI_API_KEY hoặc OPENAI_CHAT_API_KEY)")
        
        if not self._is_valid_key(self.embedding_api_key):
            missing.append("Embedding API Key (OPENAI_EMBEDDING_API_KEY)")
        
        if not self._is_valid_key(self.pinecone_api_key):
            missing.append("Pinecone API Key (PINECONE_API_KEY)")
        
        return missing
    
    def set_demo_mode(self):
        """Thiết lập chế độ demo với mock keys"""
        self.chat_api_key = "demo-chat-key"
        self.embedding_api_key = "demo-embedding-key"
        self.pinecone_api_key = "demo-pinecone-key"
        logger.info("API Key Manager set to demo mode")
    
    def log_key_status(self):
        """Log trạng thái của các API keys"""
        chat_status = "✅ Valid" if self._is_valid_key(self.chat_api_key) else "❌ Missing/Invalid"
        embedding_status = "✅ Valid" if self._is_valid_key(self.embedding_api_key) else "❌ Missing/Invalid"
        pinecone_status = "✅ Valid" if self._is_valid_key(self.pinecone_api_key) else "❌ Missing/Invalid"
        
        logger.info(f"API Key Status:")
        logger.info(f"  Chat API: {chat_status}")
        logger.info(f"  Embedding API: {embedding_status}")
        logger.info(f"  Pinecone API: {pinecone_status}")


# Global instance
api_key_manager = APIKeyManager()


def get_api_key_manager() -> APIKeyManager:
    """Get global API key manager instance"""
    return api_key_manager


def setup_production_keys():
    """Setup for production with environment validation"""
    manager = get_api_key_manager()
    is_valid, validation = manager.validate_keys()
    
    if not is_valid:
        missing = manager.get_missing_keys()
        raise ValueError(f"Missing required API keys: {', '.join(missing)}")
    
    manager.log_key_status()
    return manager


def setup_demo_keys():
    """Setup for demo/development mode"""
    manager = get_api_key_manager()
    manager.set_demo_mode()
    manager.log_key_status()
    return manager


if __name__ == "__main__":
    # Test API key manager
    manager = APIKeyManager()
    manager.log_key_status()
    
    print("\nChat Config:", manager.get_chat_config())
    print("Embedding Config:", manager.get_embedding_config())
    print("Pinecone Config:", manager.get_pinecone_config())
    
    is_valid, validation = manager.validate_keys()
    print(f"\nAll keys valid: {is_valid}")
    print("Validation details:", validation)
    
    if not is_valid:
        missing = manager.get_missing_keys()
        print("Missing keys:", missing)
