"""
Script để test và setup text-embedding-3-small
Vietnamese Legal Chatbot - Embedding Model Setup
"""

import os
import sys
from typing import Optional

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.embedding_config import EmbeddingModelManager, setup_embedding_for_vietnamese_legal


def test_current_api_key():
    """Test API key hiện tại với các embedding models"""
    print("🔑 TESTING CURRENT API KEY")
    print("=" * 40)
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ No OPENAI_API_KEY found in environment")
        return False
    
    print(f"📋 API Key: {api_key[:10]}...{api_key[-4:]}")
    
    manager = EmbeddingModelManager(api_key)
    
    # Test each model
    models_to_test = [
        "text-embedding-3-small",
        "text-embedding-3-large", 
        "text-embedding-ada-002"
    ]
    
    accessible_models = []
    
    for model in models_to_test:
        print(f"\n🧪 Testing {model}...")
        if manager.test_model_access(model, api_key):
            print(f"   ✅ {model} - ACCESSIBLE")
            accessible_models.append(model)
        else:
            print(f"   ❌ {model} - NOT ACCESSIBLE")
    
    print(f"\n📊 SUMMARY:")
    print(f"   Total accessible models: {len(accessible_models)}")
    print(f"   Accessible: {', '.join(accessible_models) if accessible_models else 'None'}")
    
    return len(accessible_models) > 0


def setup_for_text_embedding_3_small():
    """Setup hệ thống để sử dụng text-embedding-3-small"""
    print("\n🎯 SETUP FOR TEXT-EMBEDDING-3-SMALL")
    print("=" * 50)
    
    # Kiểm tra API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Cần thiết lập OPENAI_API_KEY environment variable")
        print("\n💡 Hướng dẫn:")
        print("   1. Lấy API key từ: https://platform.openai.com/account/api-keys")
        print("   2. Thiết lập: set OPENAI_API_KEY=your-key-here")
        print("   3. Đảm bảo API key có quyền truy cập text-embedding-3-small")
        return False
    
    manager = EmbeddingModelManager(api_key)
    
    # Test text-embedding-3-small
    print("🧪 Testing text-embedding-3-small access...")
    if manager.test_model_access("text-embedding-3-small", api_key):
        print("   ✅ text-embedding-3-small accessible!")
        
        # Tạo sample embedding client
        try:
            client, config = manager.create_embedding_client("text-embedding-3-small", api_key)
            if client:
                print(f"   ✅ Successfully created embedding client")
                print(f"   📏 Dimension: {config.dimension}")
                print(f"   💰 Cost: ${config.pricing_per_1k}/1K tokens")
                
                return True
            else:
                print("   ❌ Failed to create embedding client")
                return False
                
        except Exception as e:
            print(f"   ❌ Error creating client: {e}")
            return False
    else:
        print("   ❌ text-embedding-3-small not accessible")
        print("\n💡 Possible reasons:")
        print("   • API key doesn't have access to newer models")
        print("   • Need to upgrade OpenAI account")
        print("   • API key restrictions")
        
        print("\n🔄 Checking fallback options...")
        if manager.test_model_access("text-embedding-ada-002", api_key):
            print("   ✅ text-embedding-ada-002 available as fallback")
        else:
            print("   ❌ No embedding models accessible")
        
        return False


def create_env_file_template():
    """Tạo template .env file"""
    env_template = """# Vietnamese Legal Chatbot - Environment Variables
# API Keys
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_EMBEDDING_API_KEY=your-embedding-api-key-here  # Optional: separate key for embeddings
PINECONE_API_KEY=your-pinecone-api-key-here

# Pinecone Configuration
PINECONE_ENVIRONMENT=us-west1-gcp
PINECONE_INDEX_NAME=vietnamese-legal-docs

# Model Configuration
CHAT_MODEL=gpt-4o-mini
EMBEDDING_MODEL=text-embedding-3-small

# Application Configuration
DEBUG=True
LOG_LEVEL=INFO
"""
    
    env_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env.template")
    
    with open(env_file_path, "w", encoding="utf-8") as f:
        f.write(env_template)
    
    print(f"📄 Created .env template at: {env_file_path}")
    print("💡 Copy to .env and fill in your actual API keys")


def main():
    """Main setup function"""
    print("🇻🇳 VIETNAMESE LEGAL CHATBOT")
    print("🤖 TEXT-EMBEDDING-3-SMALL SETUP SCRIPT")
    print("=" * 60)
    
    # Test current setup
    has_access = test_current_api_key()
    
    if has_access:
        # Setup for text-embedding-3-small
        success = setup_for_text_embedding_3_small()
        
        if success:
            print("\n🎉 SUCCESS!")
            print("✅ text-embedding-3-small is ready to use")
            print("✅ Vietnamese Legal Chatbot configured optimally")
            
            print("\n🚀 NEXT STEPS:")
            print("   1. Run the enhanced demo: py examples\\enhanced_legal_rag_demo.py")
            print("   2. Check logs for embedding model being used")
            print("   3. Start building your Vietnamese legal AI!")
        else:
            print("\n⚠️ PARTIAL SUCCESS")
            print("❌ text-embedding-3-small not accessible")
            print("✅ Fallback models available")
            
            print("\n💡 RECOMMENDATIONS:")
            print("   • Contact OpenAI support for model access")
            print("   • Upgrade OpenAI account if needed")
            print("   • Use text-embedding-ada-002 as fallback")
    else:
        print("\n❌ SETUP FAILED")
        print("   No embedding models accessible with current API key")
        
        print("\n🔧 TROUBLESHOOTING:")
        print("   1. Verify API key is correct")
        print("   2. Check OpenAI account status")
        print("   3. Ensure sufficient credits")
        print("   4. Try a different API key")
    
    # Create .env template
    print("\n📋 CREATING ENVIRONMENT TEMPLATE...")
    create_env_file_template()
    
    # Show embedding comparison
    print("\n📊 EMBEDDING MODELS COMPARISON")
    manager = EmbeddingModelManager()
    print(manager.compare_models())


if __name__ == "__main__":
    main()
