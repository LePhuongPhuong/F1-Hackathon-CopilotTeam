"""
Flexible Embedding Configuration for Vietnamese Legal Chatbot
Cấu hình embedding linh hoạt cho Chatbot Pháp lý Việt Nam
"""

import os
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class EmbeddingModelConfig:
    """Configuration for embedding models"""
    name: str
    model_id: str
    dimension: int
    max_tokens: int
    pricing_per_1k: float  # USD per 1K tokens
    description: str
    requires_special_access: bool = False
    supported_languages: List[str] = None
    
    def __post_init__(self):
        if self.supported_languages is None:
            self.supported_languages = ["english", "vietnamese"]


class EmbeddingModelManager:
    """Quản lý các model embedding khác nhau"""
    
    # Danh sách các model embedding được hỗ trợ
    SUPPORTED_MODELS = {
        "text-embedding-ada-002": EmbeddingModelConfig(
            name="Ada 002",
            model_id="text-embedding-ada-002",
            dimension=1536,
            max_tokens=8191,
            pricing_per_1k=0.0001,
            description="OpenAI legacy embedding model, stable and reliable",
            requires_special_access=False
        ),
        "text-embedding-3-small": EmbeddingModelConfig(
            name="Embedding 3 Small",
            model_id="text-embedding-3-small",
            dimension=1536,
            max_tokens=8191,
            pricing_per_1k=0.00002,
            description="Latest OpenAI embedding model, better performance",
            requires_special_access=True
        ),
        "text-embedding-3-large": EmbeddingModelConfig(
            name="Embedding 3 Large",
            model_id="text-embedding-3-large",
            dimension=3072,
            max_tokens=8191,
            pricing_per_1k=0.00013,
            description="Highest quality OpenAI embedding model",
            requires_special_access=True
        )
    }
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_EMBEDDING_API_KEY") or os.getenv("OPENAI_API_KEY")
        self.current_model = "text-embedding-ada-002"  # Stable default
        self.preferred_model = "text-embedding-ada-002"  # Most compatible choice
        
    def get_model_config(self, model_id: str) -> Optional[EmbeddingModelConfig]:
        """Lấy config của model cụ thể"""
        return self.SUPPORTED_MODELS.get(model_id)
    
    def list_available_models(self) -> Dict[str, EmbeddingModelConfig]:
        """Liệt kê tất cả models có sẵn"""
        return self.SUPPORTED_MODELS.copy()
    
    def auto_select_model(self, api_key: Optional[str] = None) -> str:
        """Tự động chọn model tốt nhất có thể sử dụng"""
        test_api_key = api_key or self.api_key
        
        if not test_api_key or test_api_key.startswith("demo-"):
            logger.info("Using demo mode, selecting default model")
            return self.current_model
        
        # Thứ tự ưu tiên: ada-002 -> 3-small -> 3-large  
        priority_models = [
            "text-embedding-ada-002",  # Most compatible first
            "text-embedding-3-small",
            "text-embedding-3-large"
        ]
        
        for model in priority_models:
            if self.test_model_access(model, test_api_key):
                logger.info(f"Auto-selected embedding model: {model}")
                return model
        
        logger.warning("No embedding model accessible, falling back to ada-002")
        return "text-embedding-ada-002"
    
    def test_model_access(self, model_id: str, api_key: str) -> bool:
        """Test xem có thể truy cập model không"""
        try:
            # Import here to avoid dependency issues
            from openai import OpenAI
            
            client = OpenAI(api_key=api_key)
            
            # Test với text nhỏ
            response = client.embeddings.create(
                model=model_id,
                input="test"
            )
            
            if response and response.data:
                logger.info(f"✅ Model {model_id} accessible")
                return True
                
        except Exception as e:
            error_msg = str(e).lower()
            if "key not allowed" in error_msg or "access denied" in error_msg:
                logger.warning(f"❌ Model {model_id} not accessible: Permission denied")
            elif "does not exist" in error_msg:
                logger.warning(f"❌ Model {model_id} not accessible: Model not found")
            else:
                logger.warning(f"❌ Model {model_id} not accessible: {e}")
            return False
        
        return False
    
    def get_recommended_model(self, use_case: str = "general") -> str:
        """Gợi ý model phù hợp cho use case"""
        if use_case == "high_quality":
            return "text-embedding-3-large"
        elif use_case == "cost_effective":
            return "text-embedding-ada-002"
        elif use_case == "balanced":
            return "text-embedding-3-small"
        else:
            return self.preferred_model
    
    def compare_models(self) -> str:
        """So sánh các models"""
        comparison = "\n📊 EMBEDDING MODELS COMPARISON\n"
        comparison += "=" * 50 + "\n"
        
        for model_id, config in self.SUPPORTED_MODELS.items():
            comparison += f"\n🤖 {config.name} ({model_id})\n"
            comparison += f"   📏 Dimension: {config.dimension}\n"
            comparison += f"   💰 Cost: ${config.pricing_per_1k}/1K tokens\n"
            comparison += f"   🔐 Special Access: {'Yes' if config.requires_special_access else 'No'}\n"
            comparison += f"   📝 Description: {config.description}\n"
        
        comparison += "\n💡 RECOMMENDATIONS:\n"
        comparison += "   • text-embedding-ada-002: Most stable and compatible (RECOMMENDED)\n"
        comparison += "   • text-embedding-3-small: Better performance but needs special access\n"
        comparison += "   • text-embedding-3-large: Highest quality, more expensive\n"
        
        return comparison
    
    def create_embedding_client(self, model_id: Optional[str] = None, api_key: Optional[str] = None):
        """Tạo embedding client với model cụ thể"""
        try:
            from langchain_openai import OpenAIEmbeddings
            
            selected_model = model_id or self.auto_select_model(api_key)
            use_api_key = api_key or self.api_key
            
            config = self.get_model_config(selected_model)
            if not config:
                raise ValueError(f"Unsupported model: {selected_model}")
            
            logger.info(f"Creating embedding client with model: {selected_model}")
            
            embeddings = OpenAIEmbeddings(
                model=selected_model,
                openai_api_key=use_api_key,
                dimensions=config.dimension
            )
            
            return embeddings, config
            
        except ImportError:
            logger.error("OpenAI dependencies not available")
            return None, None
        except Exception as e:
            logger.error(f"Failed to create embedding client: {e}")
            return None, None


def get_embedding_manager() -> EmbeddingModelManager:
    """Get global embedding manager instance"""
    return EmbeddingModelManager()


def setup_embedding_for_vietnamese_legal():
    """Setup tối ưu cho Vietnamese Legal use case"""
    manager = EmbeddingModelManager()
    
    print("🇻🇳 VIETNAMESE LEGAL CHATBOT - EMBEDDING SETUP")
    print("=" * 50)
    
    # Hiển thị comparison
    print(manager.compare_models())
    
    # Auto-select model
    recommended = manager.auto_select_model()
    config = manager.get_model_config(recommended)
    
    print(f"\n🎯 RECOMMENDED MODEL: {config.name}")
    print(f"   Model ID: {recommended}")
    print(f"   Dimension: {config.dimension}")
    print(f"   Cost: ${config.pricing_per_1k}/1K tokens")
    print(f"   Best for: Vietnamese legal document processing")
    
    return manager, recommended, config


if __name__ == "__main__":
    # Demo embedding manager
    manager, model, config = setup_embedding_for_vietnamese_legal()
    
    # Test model access
    print(f"\n🧪 TESTING MODEL ACCESS...")
    api_key = os.getenv("OPENAI_API_KEY")
    
    if api_key and not api_key.startswith("demo-"):
        for model_id in manager.SUPPORTED_MODELS.keys():
            accessible = manager.test_model_access(model_id, api_key)
            status = "✅ Accessible" if accessible else "❌ Not accessible"
            print(f"   {model_id}: {status}")
    else:
        print("   No valid API key found, skipping access test")
    
    # Create client
    print(f"\n🔧 CREATING EMBEDDING CLIENT...")
    client, client_config = manager.create_embedding_client()
    if client:
        print(f"   ✅ Created client for: {client_config.name}")
    else:
        print(f"   ❌ Failed to create client")
