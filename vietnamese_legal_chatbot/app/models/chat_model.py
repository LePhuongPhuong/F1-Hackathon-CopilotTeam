"""
Chat Model Integration for Vietnamese Legal AI Chatbot
Tích hợp Mô hình Chat cho Chatbot AI Pháp lý Việt Nam

Handles LLM integration with OpenAI and local models.
Xử lý tích hợp LLM với OpenAI và các mô hình cục bộ.
"""

from openai import OpenAI
from typing import Dict, List, Optional, Any
from abc import ABC, abstractmethod
import logging

try:
    from app.utils.simple_config import get_simple_config
    settings = get_simple_config()
except Exception:
    from app.utils.demo_config import demo_settings
    settings = demo_settings

# Configure logging
logger = logging.getLogger(__name__)

class BaseChatModel(ABC):
    """Abstract base class for chat models"""
    
    @abstractmethod
    def generate_response(self, prompt: str, context: str = None) -> str:
        """Generate response from the model"""
        pass
    
    @abstractmethod
    def get_embedding(self, text: str) -> List[float]:
        """Get text embedding"""
        pass

class OpenAIChatModel(BaseChatModel):
    """OpenAI chat model implementation"""
    
    def __init__(self, 
                 api_key: Optional[str] = None,
                 api_base: Optional[str] = None,
                 model: str = None, 
                 temperature: float = None,
                 max_tokens: int = None):
        """Initialize OpenAI chat model with flexible configuration"""
        
        # Use provided parameters or fall back to demo_settings
        self.api_key = api_key or demo_settings.openai_chat_api_key
        self.api_base = api_base or demo_settings.openai_chat_api_base
        self.model_name = model or demo_settings.chat_model
        self.temperature = temperature if temperature is not None else demo_settings.temperature
        self.max_tokens = max_tokens or demo_settings.max_tokens
        
        # Configure OpenAI client for chat
        chat_client_kwargs = {
            "api_key": self.api_key,
            "base_url": self.api_base
        }
            
        self.chat_client = OpenAI(**chat_client_kwargs)
        
        # Configure separate OpenAI client for embeddings
        embedding_client_kwargs = {
            "api_key": demo_settings.openai_embedding_api_key,
            "base_url": demo_settings.openai_embedding_api_base
        }
            
        self.embedding_client = OpenAI(**embedding_client_kwargs)
        
        logger.info(f"Initialized OpenAI chat model: {self.model_name}")
        logger.info(f"Chat API: {self.api_base}")
        logger.info(f"Embedding API: {demo_settings.openai_embedding_api_base}")
    
    def generate_response(self, prompt: str, context: str = None) -> str:
        """Generate response using OpenAI"""
        try:
            # Prepare messages
            messages = []
            
            if context:
                messages.append({
                    "role": "system",
                    "content": f"Bạn là một chuyên gia pháp lý Việt Nam. Sử dụng thông tin sau để trả lời câu hỏi: {context}"
                })
            
            messages.append({
                "role": "user", 
                "content": prompt
            })
            
            response = self.chat_client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error generating OpenAI response: {e}")
            raise e
    
    def get_embedding(self, text: str) -> List[float]:
        """Get text embedding using separate embedding API"""
        try:
            response = self.embedding_client.embeddings.create(
                model=demo_settings.embedding_model,
                input=text
            )
            return response.data[0].embedding
            
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise e

class LocalChatModel(BaseChatModel):
    """Local chat model implementation for fallback"""
    
    def __init__(self, model_path: str = None):
        """Initialize local chat model"""
        # TODO: Implement local model initialization
        self.model_path = model_path
        self.model = None
    
    def generate_response(self, prompt: str, context: str = None) -> str:
        """Generate response using local model"""
        # TODO: Implement local model response
        pass
    
    def get_embedding(self, text: str) -> List[float]:
        """Get text embedding using local model"""
        # TODO: Implement local embedding
        pass

class ChatModelFactory:
    """Factory for creating chat models"""
    
    @staticmethod
    def create_model(model_type: str = "openai", **kwargs) -> BaseChatModel:
        """Create chat model based on type"""
        if model_type == "openai":
            return OpenAIChatModel(**kwargs)
        elif model_type == "local":
            return LocalChatModel(**kwargs)
        else:
            raise ValueError(f"Unsupported model type: {model_type}")

# TODO: Implement prompt templates for Vietnamese legal queries
VIETNAMESE_LEGAL_PROMPTS = {
    "legal_query": """
    Bạn là một chuyên gia pháp lý Việt Nam. Hãy trả lời câu hỏi dưới đây dựa trên:
    1. Tài liệu pháp lý được cung cấp
    2. Kiến thức về luật pháp Việt Nam
    3. Trích dẫn cụ thể từ các điều luật liên quan
    
    Câu hỏi: {question}
    
    Ngữ cảnh từ tài liệu pháp lý:
    {context}
    
    Hãy trả lời một cách chính xác, chi tiết và có trích dẫn cụ thể.
    """,
    
    "document_analysis": """
    Phân tích tài liệu pháp lý sau và trích xuất các thông tin quan trọng:
    
    Tài liệu: {document}
    
    Hãy trích xuất:
    1. Tên luật/văn bản
    2. Ngày ban hành
    3. Cơ quan ban hành
    4. Các điều khoản chính
    5. Phạm vi áp dụng
    """,
    
    "citation_format": """
    Định dạng trích dẫn theo chuẩn pháp lý Việt Nam:
    {citation_text}
    """
}
