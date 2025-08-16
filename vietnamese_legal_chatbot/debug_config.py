"""Debug script để kiểm tra config"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=== Environment Variables Debug ===")
print(f"OPENAI_API_KEY: {os.getenv('OPENAI_API_KEY', 'NOT_FOUND')}")
print(f"OPENAI_EMBEDDING_API_KEY: {os.getenv('OPENAI_EMBEDDING_API_KEY', 'NOT_FOUND')}")
print(f"PINECONE_API_KEY: {os.getenv('PINECONE_API_KEY', 'NOT_FOUND')}")

print("\n=== Trying to load Settings ===")
try:
    from app.utils.simple_config import settings
    print("✅ Settings loaded successfully!")
    print(f"Chat API Key: {settings.openai_api_key[:10]}...")
    print(f"Embedding API Key: {settings.embedding_api_key[:10]}...")
    print(f"Pinecone API Key: {settings.pinecone_api_key[:10]}...")
except Exception as e:
    print(f"❌ Error loading settings: {e}")

print("\n=== Manual Settings Test ===")
try:
    from app.utils.simple_config import Settings
    settings_manual = Settings(
        openai_api_key=os.getenv('OPENAI_API_KEY'),
        embedding_api_key=os.getenv('OPENAI_EMBEDDING_API_KEY'),
        pinecone_api_key=os.getenv('PINECONE_API_KEY'),
        pinecone_environment=os.getenv('PINECONE_ENVIRONMENT', 'us-east-1-aws'),
        pinecone_index_name=os.getenv('PINECONE_INDEX_NAME', 'vietnamese-legal-docs')
    )
    print("✅ Manual settings creation successful!")
except Exception as e:
    print(f"❌ Manual settings error: {e}")
