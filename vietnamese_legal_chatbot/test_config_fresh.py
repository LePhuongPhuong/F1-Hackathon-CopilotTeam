"""Test simplified config loading với minimal implementation"""
import os
import sys
from pathlib import Path

# Thêm thư mục app vào Python path
app_path = Path(__file__).parent / "app"
sys.path.insert(0, str(app_path))

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

# Load environment variables
load_dotenv()

print("=== Environment Variables Check ===")
required_vars = ['OPENAI_API_KEY', 'OPENAI_EMBEDDING_API_KEY', 'PINECONE_API_KEY', 'SECRET_KEY']
for var in required_vars:
    value = os.getenv(var)
    if value:
        print(f"✅ {var}: {value[:15]}...")
    else:
        print(f"❌ {var}: NOT_FOUND")

print("\n=== Testing Minimal Settings Class ===")

class MinimalSettings(BaseSettings):
    """Minimal settings for testing"""
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    embedding_api_key: str = Field(..., env="OPENAI_EMBEDDING_API_KEY")
    pinecone_api_key: str = Field(..., env="PINECONE_API_KEY")
    secret_key: str = Field(..., env="SECRET_KEY")
    
    pinecone_environment: str = Field(default="us-east-1-aws", env="PINECONE_ENVIRONMENT")
    pinecone_index_name: str = Field(default="vietnamese-legal-docs", env="PINECONE_INDEX_NAME")
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # Ignore extra fields

try:
    minimal_settings = MinimalSettings()
    print("✅ Minimal settings created successfully!")
    print(f"OpenAI API Key: {minimal_settings.openai_api_key[:15]}...")
    print(f"Embedding API Key: {minimal_settings.embedding_api_key[:15]}...")
    print(f"Pinecone API Key: {minimal_settings.pinecone_api_key[:15]}...")
    print(f"Secret Key: {minimal_settings.secret_key[:15]}...")
    print(f"Pinecone Environment: {minimal_settings.pinecone_environment}")
    print(f"Pinecone Index: {minimal_settings.pinecone_index_name}")
except Exception as e:
    print(f"❌ Error creating minimal settings: {e}")

print("\n=== Testing Direct Import ===")
try:
    # Reload the module to clear cache
    if 'app.utils.simple_config' in sys.modules:
        del sys.modules['app.utils.simple_config']
    if 'app.utils' in sys.modules:
        del sys.modules['app.utils']
    
    from utils.simple_config import Settings
    direct_settings = Settings()
    print("✅ Direct settings import successful!")
    print(f"Direct OpenAI Key: {direct_settings.openai_api_key[:15]}...")
    print(f"Direct Embedding Key: {direct_settings.embedding_api_key[:15]}...")
except Exception as e:
    print(f"❌ Direct settings import error: {e}")
