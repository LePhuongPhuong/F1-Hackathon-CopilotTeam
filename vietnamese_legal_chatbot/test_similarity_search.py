#!/usr/bin/env python3
"""
Test Pinecone Similarity Search
Kiểm tra tính năng tìm kiếm tương tự trong Pinecone
"""

import sys
import os
sys.path.insert(0, os.path.abspath("."))

from app.utils.demo_config import get_demo_config
from app.services.pinecone_service import PineconeService
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_similarity_search():
    """Test similarity search functionality"""
    print("=== Testing Pinecone Similarity Search ===")
    
    try:
        # 1. Load configuration
        print("\n1. Loading configuration...")
        config = get_demo_config()
        print("✅ Configuration loaded")
        
        # 2. Initialize Pinecone service
        print("\n2. Initializing Pinecone service...")
        pinecone_service = PineconeService(
            api_key=config.pinecone_api_key,
            environment=config.pinecone_environment,
            index_name=config.pinecone_index_name,
            openai_api_key=config.openai_embedding_api_key
        )
        print("✅ Pinecone service initialized")
        
        # 3. Test similarity search directly
        print("\n3. Testing similarity search...")
        test_queries = [
            "Thời gian làm việc theo luật lao động",
            "Quyền nghỉ phép của người lao động",
            "Hợp đồng lao động có những loại nào",
            "Chế độ bảo hiểm xã hội"
        ]
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n3.{i}. Testing query: '{query}'")
            
            # Test with backward compatibility (query_text parameter)
            try:
                results_legacy = pinecone_service.similarity_search(
                    query_text=query,
                    k=3,
                    score_threshold=0.3
                )
                print(f"✅ Legacy search returned {len(results_legacy)} results")
                if results_legacy:
                    print(f"   First result preview: {results_legacy[0][:100]}...")
                
            except Exception as e:
                print(f"❌ Legacy search failed: {e}")
            
            # Test with new parameter (query parameter)
            try:
                results_new = pinecone_service.similarity_search(
                    query=query,
                    k=3,
                    score_threshold=0.3
                )
                print(f"✅ New search returned {len(results_new)} results")
                if results_new:
                    print(f"   First result preview: {results_new[0][:100]}...")
                    
            except Exception as e:
                print(f"❌ New search failed: {e}")
        
        # 4. Test with metadata filters
        print("\n4. Testing search with metadata filters...")
        try:
            filtered_results = pinecone_service.similarity_search(
                query="luật lao động",
                k=5,
                metadata_filter={"legal_domain": "lao_dong", "language": "vietnamese"}
            )
            print(f"✅ Filtered search returned {len(filtered_results)} results")
            
        except Exception as e:
            print(f"❌ Filtered search failed: {e}")
        
        print("\n🎉 Similarity search testing completed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        logger.exception("Full error details:")
        return False

if __name__ == "__main__":
    success = test_similarity_search()
    if success:
        print("\n✅ All similarity search tests passed!")
    else:
        print("\n❌ Some similarity search tests failed!")
        sys.exit(1)
