"""Deep debugging của Pydantic Settings"""
import os
from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

# Load environment variables
load_dotenv()

print("=== Raw Environment Variables ===")
print(f"OPENAI_API_KEY: '{os.getenv('OPENAI_API_KEY')}'")
print(f"OPENAI_EMBEDDING_API_KEY: '{os.getenv('OPENAI_EMBEDDING_API_KEY')}'")
print(f"Length OPENAI_EMBEDDING_API_KEY: {len(os.getenv('OPENAI_EMBEDDING_API_KEY', ''))}")

# Check if có ký tự ẩn
embedding_key = os.getenv('OPENAI_EMBEDDING_API_KEY', '')
print(f"Embedding key bytes: {embedding_key.encode()}")

print("\n=== Test manual assignment ===")
os.environ['TEST_EMBEDDING_KEY'] = embedding_key
print(f"TEST_EMBEDDING_KEY: '{os.getenv('TEST_EMBEDDING_KEY')}'")

print("\n=== Test Pydantic với env name khác ===")
class TestSettings(BaseSettings):
    test_key: str = Field(..., env="TEST_EMBEDDING_KEY")
    
    class Config:
        extra = "ignore"

try:
    test_settings = TestSettings()
    print(f"✅ Test settings worked: {test_settings.test_key[:15]}...")
except Exception as e:
    print(f"❌ Test settings failed: {e}")

print("\n=== Test Pydantic với original env name ===")
class TestSettings2(BaseSettings):
    embedding_key: str = Field(..., env="OPENAI_EMBEDDING_API_KEY")
    
    class Config:
        extra = "ignore"

try:
    test_settings2 = TestSettings2()
    print(f"✅ Test settings2 worked: {test_settings2.embedding_key[:15]}...")
except Exception as e:
    print(f"❌ Test settings2 failed: {e}")

print("\n=== Check all env vars containing 'EMBEDDING' ===")
for key, value in os.environ.items():
    if 'EMBEDDING' in key:
        print(f"{key}: '{value}'")

print("\n=== Test bằng cách set thẳng env var ===")
os.environ['EMBEDDING_API_KEY'] = embedding_key
class TestSettings3(BaseSettings):
    embedding_key: str = Field(..., env="EMBEDDING_API_KEY")
    
    class Config:
        extra = "ignore"

try:
    test_settings3 = TestSettings3()
    print(f"✅ Test settings3 worked: {test_settings3.embedding_key[:15]}...")
except Exception as e:
    print(f"❌ Test settings3 failed: {e}")
