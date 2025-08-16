"""Test Pydantic Settings với debug chi tiết"""
import os
from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

# Load environment variables
load_dotenv()

print("=== All Environment Variables ===")
for key, value in os.environ.items():
    if 'API' in key or 'KEY' in key or 'PINECONE' in key:
        print(f"{key}: {value[:20]}..." if len(value) > 20 else f"{key}: {value}")

print("\n=== Simple Settings Class Test ===")
class SimpleSettings(BaseSettings):
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    embedding_api_key: str = Field(..., env="OPENAI_EMBEDDING_API_KEY")
    
    class Config:
        env_file = ".env"
        case_sensitive = False

try:
    simple_settings = SimpleSettings()
    print("✅ Simple settings loaded successfully!")
    print(f"OpenAI Key: {simple_settings.openai_api_key[:10]}...")
    print(f"Embedding Key: {simple_settings.embedding_api_key[:10]}...")
except Exception as e:
    print(f"❌ Simple settings error: {e}")

print("\n=== Test with manual values ===")
try:
    manual_settings = SimpleSettings(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        embedding_api_key=os.getenv("OPENAI_EMBEDDING_API_KEY")
    )
    print("✅ Manual settings loaded successfully!")
except Exception as e:
    print(f"❌ Manual settings error: {e}")
