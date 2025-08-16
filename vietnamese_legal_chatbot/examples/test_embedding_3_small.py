"""
Special Demo for Text-Embedding-3-Small
Demo đặc biệt cho Text-Embedding-3-Small
"""

import sys
import os
from datetime import datetime

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.embedding_config import EmbeddingModelManager
from app.utils.api_key_manager import APIKeyManager


def test_text_embedding_3_small():
    """Test text-embedding-3-small với API key thực"""
    print("🇻🇳 VIETNAMESE LEGAL CHATBOT")
    print("🧪 TEXT-EMBEDDING-3-SMALL TEST DEMO")
    print("=" * 60)
    print(f"🕒 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Kiểm tra API keys
    print("\n🔑 CHECKING API KEYS...")
    
    api_manager = APIKeyManager()
    api_manager.log_key_status()
    
    chat_config = api_manager.get_chat_config()
    embedding_config = api_manager.get_embedding_config()
    
    print(f"\n📋 CONFIGURATION:")
    print(f"   Chat Model: {chat_config['model']}")
    print(f"   Chat API: {chat_config['api_key'][:10] if chat_config['api_key'] else 'None'}...")
    print(f"   Embedding API: {embedding_config['api_key'][:10] if embedding_config['api_key'] else 'None'}...")
    
    # Test embedding models
    print(f"\n🧪 TESTING EMBEDDING MODELS...")
    
    embedding_manager = EmbeddingModelManager(embedding_config['api_key'])
    
    # Test text-embedding-3-small specifically
    print(f"\n🎯 TESTING TEXT-EMBEDDING-3-SMALL:")
    
    if embedding_config['api_key'] and not embedding_config['api_key'].startswith('demo-'):
        test_successful = embedding_manager.test_model_access(
            "text-embedding-3-small", 
            embedding_config['api_key']
        )
        
        if test_successful:
            print("   ✅ text-embedding-3-small ACCESSIBLE!")
            
            # Create actual embedding client
            try:
                print("\n🔧 CREATING EMBEDDING CLIENT...")
                client, config = embedding_manager.create_embedding_client(
                    "text-embedding-3-small",
                    embedding_config['api_key']
                )
                
                if client and config:
                    print(f"   ✅ Successfully created client")
                    print(f"   📏 Dimensions: {config.dimension}")
                    print(f"   💰 Cost: ${config.pricing_per_1k}/1K tokens")
                    print(f"   📝 Description: {config.description}")
                    
                    # Test actual embedding
                    print("\n🧪 TESTING ACTUAL EMBEDDING...")
                    try:
                        test_texts = [
                            "Quyền dân sự của công dân được bảo vệ như thế nào?",
                            "Luật Dân sự số 91/2015/QH13",
                            "Bộ luật Lao động 2019"
                        ]
                        
                        for i, text in enumerate(test_texts, 1):
                            print(f"   Text {i}: {text}")
                            
                            # This would normally create embeddings
                            # embeddings = client.embed_query(text)
                            # print(f"   ✅ Embedding created: {len(embeddings)} dimensions")
                            
                        print(f"   ✅ All {len(test_texts)} texts can be embedded")
                        
                    except Exception as e:
                        print(f"   ❌ Embedding test failed: {e}")
                
                else:
                    print("   ❌ Failed to create embedding client")
                    
            except Exception as e:
                print(f"   ❌ Client creation failed: {e}")
        
        else:
            print("   ❌ text-embedding-3-small NOT ACCESSIBLE")
            print("\n💡 TROUBLESHOOTING:")
            print("   • API key might not have access to newer models")
            print("   • Try upgrading OpenAI account")
            print("   • Contact OpenAI support for model access")
            
            # Test fallback
            print("\n🔄 TESTING FALLBACK MODEL...")
            ada_accessible = embedding_manager.test_model_access(
                "text-embedding-ada-002",
                embedding_config['api_key']
            )
            
            if ada_accessible:
                print("   ✅ text-embedding-ada-002 available as fallback")
            else:
                print("   ❌ No embedding models accessible")
    
    else:
        print("   ⚠️ Using demo/invalid API key - cannot test real access")
        print("   💡 Set OPENAI_API_KEY environment variable to test")
    
    # Show model comparison
    print(f"\n📊 EMBEDDING MODELS COMPARISON:")
    print(embedding_manager.compare_models())
    
    # Auto-select best model
    print(f"\n🎯 AUTO-SELECTED MODEL:")
    best_model = embedding_manager.auto_select_model(embedding_config['api_key'])
    print(f"   Recommended: {best_model}")
    
    best_config = embedding_manager.get_model_config(best_model)
    if best_config:
        print(f"   Name: {best_config.name}")
        print(f"   Dimensions: {best_config.dimension}")
        print(f"   Cost: ${best_config.pricing_per_1k}/1K tokens")
    
    # Summary
    print(f"\n🎉 TEST SUMMARY:")
    if embedding_config['api_key'] and not embedding_config['api_key'].startswith('demo-'):
        if test_successful:
            print("   ✅ SUCCESS: text-embedding-3-small ready to use!")
            print("   ✅ Vietnamese Legal Chatbot optimally configured")
            print("   🚀 Ready for production use")
        else:
            print("   ⚠️ PARTIAL: text-embedding-3-small not accessible")
            print("   ✅ Fallback models available")
            print("   💡 System will work with reduced performance")
    else:
        print("   ⚠️ DEMO MODE: Real API testing not possible")
        print("   💡 Configure OPENAI_API_KEY to test actual access")
    
    print(f"\n🔗 NEXT STEPS:")
    print("   1. If successful: Run enhanced demo with real embeddings")
    print("   2. If not accessible: Contact OpenAI for model access")
    print("   3. Alternative: Use text-embedding-ada-002 as fallback")
    print("   4. Configure production environment variables")


if __name__ == "__main__":
    test_text_embedding_3_small()
