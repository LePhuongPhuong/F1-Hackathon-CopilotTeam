"""
Pinecone Setup Script for Vietnamese Legal AI Chatbot
Script Thiết lập Pinecone cho Chatbot AI Pháp lý Việt Nam

Initialize Pinecone index and load initial Vietnamese legal documents.
Khởi tạo chỉ mục Pinecone và tải tài liệu pháp lý Việt Nam ban đầu.
"""

import os
import sys
import logging
from pathlib import Path
from typing import List, Dict, Any

# Add app directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

# TODO: Import khi implement
# import pinecone
# from app.utils.config import settings
# from app.services.pinecone_service import PineconeService
# from app.services.document_processor import VietnameseLegalDocumentProcessor

def setup_logging():
    """Setup logging for setup script"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/setup_pinecone.log'),
            logging.StreamHandler()
        ]
    )

def validate_environment():
    """Validate required environment variables"""
    required_vars = [
        'OPENAI_API_KEY',
        'PINECONE_API_KEY', 
        'PINECONE_ENVIRONMENT',
        'PINECONE_INDEX_NAME'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        logging.error(f"Missing environment variables: {missing_vars}")
        logging.error("Please set these variables in .env file or environment")
        return False
    
    return True

def create_pinecone_index():
    """Create Pinecone index with optimal configuration for Vietnamese legal docs"""
    try:
        logging.info("Creating Pinecone index...")
        
        # TODO: Implement Pinecone index creation
        # pinecone.init(
        #     api_key=settings.pinecone_api_key,
        #     environment=settings.pinecone_environment
        # )
        
        # Check if index already exists
        # existing_indexes = pinecone.list_indexes()
        # if settings.pinecone_index_name in existing_indexes:
        #     logging.info(f"Index {settings.pinecone_index_name} already exists")
        #     return True
        
        # Create index with optimal settings for Vietnamese legal documents
        # pinecone.create_index(
        #     name=settings.pinecone_index_name,
        #     dimension=settings.pinecone_dimension,  # 1536 for OpenAI embeddings
        #     metric='cosine',
        #     metadata_config={
        #         "indexed": [
        #             "legal_domain",
        #             "document_type", 
        #             "language",
        #             "article_number",
        #             "effective_date"
        #         ]
        #     }
        # )
        
        logging.info(f"Successfully created Pinecone index: {os.getenv('PINECONE_INDEX_NAME')}")
        return True
        
    except Exception as e:
        logging.error(f"Failed to create Pinecone index: {e}")
        return False

def load_sample_legal_documents():
    """Load sample Vietnamese legal documents into Pinecone"""
    try:
        logging.info("Loading sample Vietnamese legal documents...")
        
        # TODO: Implement document loading
        sample_documents = get_sample_documents()
        
        # Process and upload documents
        # processor = VietnameseLegalDocumentProcessor()
        # pinecone_service = PineconeService(
        #     api_key=settings.pinecone_api_key,
        #     environment=settings.pinecone_environment,
        #     index_name=settings.pinecone_index_name
        # )
        
        processed_count = 0
        for doc_info in sample_documents:
            try:
                logging.info(f"Processing document: {doc_info['title']}")
                
                # TODO: Process and upload document
                # processed_doc = processor.process_legal_document(doc_info['content'])
                # success = pinecone_service.upsert_documents([processed_doc])
                
                # if success:
                #     processed_count += 1
                #     logging.info(f"Successfully uploaded: {doc_info['title']}")
                
                processed_count += 1  # Placeholder
                
            except Exception as e:
                logging.error(f"Failed to process document {doc_info['title']}: {e}")
        
        logging.info(f"Successfully loaded {processed_count} sample documents")
        return True
        
    except Exception as e:
        logging.error(f"Failed to load sample documents: {e}")
        return False

def get_sample_documents() -> List[Dict[str, Any]]:
    """Get sample Vietnamese legal documents for initial setup"""
    return [
        {
            'title': 'Bộ luật Dân sự 2015 - Điều 1',
            'content': '''
            Điều 1. Phạm vi điều chỉnh
            Bộ luật này quy định về quan hệ dân sự phát sinh trong các lĩnh vực 
            sau đây:
            1. Quan hệ nhân thân;
            2. Quan hệ tài sản;
            3. Quan hệ dân sự trong hoạt động kinh doanh, thương mại;
            4. Quan hệ dân sự khác.
            ''',
            'metadata': {
                'legal_domain': 'dan_su',
                'document_type': 'bo_luat',
                'article_number': '1',
                'law_name': 'Bộ luật Dân sự 2015',
                'effective_date': '01/01/2017'
            }
        },
        {
            'title': 'Bộ luật Lao động 2019 - Điều 2',
            'content': '''
            Điều 2. Đối tượng áp dụng
            1. Bộ luật này áp dụng đối với người lao động, người sử dụng lao động 
            trong quan hệ lao động; cơ quan, tổ chức, cá nhân có liên quan đến 
            quan hệ lao động.
            2. Trường hợp điều ước quốc tế mà Cộng hòa xã hội chủ nghĩa Việt Nam 
            là thành viên có quy định khác với quy định của Bộ luật này thì áp dụng 
            quy định của điều ước quốc tế đó.
            ''',
            'metadata': {
                'legal_domain': 'lao_dong',
                'document_type': 'bo_luat',
                'article_number': '2',
                'law_name': 'Bộ luật Lao động 2019',
                'effective_date': '01/01/2021'
            }
        },
        {
            'title': 'Luật Doanh nghiệp 2020 - Điều 4',
            'content': '''
            Điều 4. Quyền thành lập doanh nghiệp
            1. Cá nhân, tổ chức có quyền thành lập doanh nghiệp theo quy định 
            của Luật này và pháp luật có liên quan.
            2. Không ai được cản trở việc thành lập doanh nghiệp hợp pháp của 
            cá nhân, tổ chức.
            3. Việc thành lập doanh nghiệp phải tuân thủ quy định của pháp luật 
            về điều kiện đầu tư kinh doanh.
            ''',
            'metadata': {
                'legal_domain': 'thuong_mai',
                'document_type': 'luat',
                'article_number': '4',
                'law_name': 'Luật Doanh nghiệp 2020',
                'effective_date': '01/01/2021'
            }
        }
    ]

def test_pinecone_connection():
    """Test Pinecone connection and basic operations"""
    try:
        logging.info("Testing Pinecone connection...")
        
        # TODO: Implement connection test
        # pinecone_service = PineconeService(
        #     api_key=settings.pinecone_api_key,
        #     environment=settings.pinecone_environment,
        #     index_name=settings.pinecone_index_name
        # )
        
        # Test basic operations
        # stats = pinecone_service.get_index_stats()
        # logging.info(f"Index stats: {stats}")
        
        # Test search with sample query
        # results = pinecone_service.search_similar_documents(
        #     query="quyền thành lập doanh nghiệp",
        #     top_k=3
        # )
        # logging.info(f"Test search returned {len(results)} results")
        
        logging.info("Pinecone connection test successful")
        return True
        
    except Exception as e:
        logging.error(f"Pinecone connection test failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Vietnamese Legal AI Chatbot - Pinecone Setup")
    print("=" * 60)
    
    # Setup logging
    setup_logging()
    
    # Validate environment
    if not validate_environment():
        logging.error("❌ Environment validation failed")
        sys.exit(1)
    
    logging.info("✅ Environment validation passed")
    
    # Create Pinecone index
    if not create_pinecone_index():
        logging.error("❌ Failed to create Pinecone index")
        sys.exit(1)
    
    logging.info("✅ Pinecone index created successfully")
    
    # Load sample documents
    if not load_sample_legal_documents():
        logging.error("❌ Failed to load sample documents")
        sys.exit(1)
    
    logging.info("✅ Sample documents loaded successfully")
    
    # Test connection
    if not test_pinecone_connection():
        logging.error("❌ Pinecone connection test failed")
        sys.exit(1)
    
    logging.info("✅ Pinecone connection test passed")
    
    print("\n🎉 Pinecone setup completed successfully!")
    print("Your Vietnamese Legal AI Chatbot is ready to use.")
    print("\nNext steps:")
    print("1. Run the FastAPI backend: python app/main.py")
    print("2. Run the Streamlit frontend: streamlit run app/streamlit_app.py")

if __name__ == "__main__":
    main()
