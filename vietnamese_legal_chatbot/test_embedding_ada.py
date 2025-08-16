"""
Test simple embedding with text-embedding-ada-002
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

def test_embedding_3_small():
    """Test text-embedding-3-small with current API keys"""
    
    print("🔍 Testing text-embedding-3-small...")
    
    # Get API keys from environment
    api_key = os.getenv("OPENAI_EMBEDDING_API_KEY") or os.getenv("OPENAI_API_KEY")
    api_base = os.getenv("OPENAI_EMBEDDING_API_BASE") or os.getenv("OPENAI_API_BASE")
    
    print(f"🔑 API Key: {api_key[:8]}..." if api_key else "❌ No API key")
    print(f"🌐 API Base: {api_base}")
    
    # Test text
    test_text = "Quyền dân sự của công dân được bảo vệ như thế nào?"
    
    try:
        # Create OpenAI client
        client = OpenAI(
            api_key=api_key,
            base_url=api_base
        )
        
        print(f"📝 Test text: {test_text}")
        print("⏳ Creating embedding...")
        
        # Create embedding
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=test_text
        )
        
        embedding = response.data[0].embedding
        
        print(f"✅ Success! Embedding created")
        print(f"📊 Embedding dimension: {len(embedding)}")
        print(f"🔢 First 5 values: {embedding[:5]}")
        print(f"💰 Usage: {response.usage.total_tokens} tokens")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🇻🇳 VIETNAMESE LEGAL AI - EMBEDDING TEST")
    print("=" * 50)
    
    success = test_embedding_3_small()
    
    print("=" * 50)
    if success:
        print("🎉 Embedding test passed! text-embedding-3-small is working correctly.")
    else:
        print("😞 Embedding test failed. Please check your API configuration.")
