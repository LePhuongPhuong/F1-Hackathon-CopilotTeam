"""
Example usage of PineconeService for Vietnamese Legal AI Chatbot
Ví dụ sử dụng PineconeService cho Chatbot AI Pháp lý Việt Nam

This script demonstrates how to use the PineconeService class to:
1. Initialize the service
2. Process and upsert legal documents
3. Search for similar documents
4. Manage document metadata

Script này minh họa cách sử dụng class PineconeService để:
1. Khởi tạo dịch vụ
2. Xử lý và upsert tài liệu pháp lý  
3. Tìm kiếm tài liệu tương tự
4. Quản lý metadata tài liệu
"""

import os
import logging
from typing import List, Dict, Any
import sys
import asyncio

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.services.pinecone_service import (
    PineconeService,
    PineconeServiceFactory,
    LegalDocumentProcessor,
    VietnameseLegalMetadataBuilder,
    DocumentMetadata,
    VectorSearchResult,
    PineconeServiceError
)
from app.utils.config import Settings

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def setup_environment():
    """
    Setup environment variables for testing
    Thiết lập biến môi trường cho testing
    """
    # Set environment variables if not already set
    if not os.getenv("PINECONE_API_KEY"):
        os.environ["PINECONE_API_KEY"] = "your-pinecone-api-key-here"
    
    if not os.getenv("PINECONE_ENVIRONMENT"):
        os.environ["PINECONE_ENVIRONMENT"] = "us-west1-gcp"
    
    if not os.getenv("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = "your-openai-api-key-here"
    
    if not os.getenv("PINECONE_INDEX_NAME"):
        os.environ["PINECONE_INDEX_NAME"] = "vietnamese-legal-docs-demo"


def create_sample_legal_documents() -> List[Dict[str, Any]]:
    """
    Tạo dữ liệu mẫu cho tài liệu pháp lý Việt Nam
    Create sample Vietnamese legal documents data
    
    Returns:
        List[Dict[str, Any]]: Danh sách tài liệu mẫu
    """
    sample_documents = [
        {
            "title": "Bộ luật Dân sự 2015",
            "content": """
            CHƯƠNG I - QUY ĐỊNH CHUNG
            
            Điều 1. Phạm vi điều chỉnh
            1. Bộ luật này quy định về quan hệ dân sự.
            2. Quan hệ dân sự là quan hệ tài sản và quan hệ nhân thân giữa các chủ thể trong một vị trí bình đẳng.
            3. Quan hệ tài sản là quan hệ phát sinh về tài sản.
            
            Điều 2. Nguyên tắc cơ bản của pháp luật dân sự
            1. Bình đẳng trong quan hệ dân sự.
            2. Tự do, tự nguyện thỏa thuận trong quan hệ dân sự.
            3. Thiện chí trong việc thực hiện quyền dân sự, nghĩa vụ dân sự.
            """,
            "legal_domain": "dan_su",
            "document_type": "bo_luat",
            "issuing_authority": "quoc_hoi",
            "effective_date": "2017-01-01"
        },
        {
            "title": "Bộ luật Hình sự 2015",
            "content": """
            CHƯƠNG I - NHỮNG QUY ĐỊNH CHUNG
            
            Điều 1. Nhiệm vụ của Bộ luật hình sự
            Bảo vệ độc lập, chủ quyền, thống nhất, toàn vẹn lãnh thổ của Tổ quốc, bảo vệ chế độ chính trị.
            
            Điều 2. Căn cứ trách nhiệm hình sự
            1. Chỉ người nào phạm tội mới phải chịu trách nhiệm hình sự.
            2. Việc xác định tội phạm và hình phạt phải căn cứ vào Bộ luật này và luật khác có quy định về tội phạm và hình phạt.
            """,
            "legal_domain": "hinh_su", 
            "document_type": "bo_luat",
            "issuing_authority": "quoc_hoi",
            "effective_date": "2018-01-01"
        },
        {
            "title": "Bộ luật Lao động 2019",
            "content": """
            CHƯƠNG I - QUY ĐỊNH CHUNG
            
            Điều 1. Phạm vi điều chỉnh
            1. Bộ luật này quy định về quan hệ lao động, quan hệ gắn liền với quan hệ lao động.
            2. Quan hệ lao động là quan hệ xã hội phát sinh trong quá trình tuyển dụng và sử dụng lao động.
            
            Điều 2. Đối tượng áp dụng
            1. Người lao động là người từ đủ 15 tuổi trở lên, có khả năng lao động.
            2. Người sử dụng lao động là doanh nghiệp, cơ quan, tổ chức, cá nhân có thuê mướn, sử dụng lao động.
            """,
            "legal_domain": "lao_dong",
            "document_type": "bo_luat", 
            "issuing_authority": "quoc_hoi",
            "effective_date": "2021-01-01"
        }
    ]
    
    return sample_documents


def demonstrate_service_initialization():
    """
    Minh họa khởi tạo PineconeService
    Demonstrate PineconeService initialization
    """
    logger.info("=== DEMO: Khởi tạo PineconeService ===")
    
    try:
        # Method 1: Tạo từ environment variables
        logger.info("1. Tạo service từ environment variables...")
        # service = PineconeServiceFactory.create_from_env()
        
        # Method 2: Tạo trực tiếp với parameters (cho demo)
        logger.info("2. Tạo service với parameters trực tiếp...")
        service = PineconeService(
            api_key=os.getenv("PINECONE_API_KEY", "demo-key"),
            environment=os.getenv("PINECONE_ENVIRONMENT", "us-west1-gcp"),
            index_name=os.getenv("PINECONE_INDEX_NAME", "vietnamese-legal-docs-demo"),
            dimension=1536,
            openai_api_key=os.getenv("OPENAI_API_KEY", "demo-openai-key")
        )
        
        logger.info(f"✅ Service đã được tạo: {service.index_name}")
        
        # Kiểm tra health
        logger.info("3. Kiểm tra health check...")
        health = service.health_check()
        logger.info(f"Health status: {health['status']}")
        
        # Hiển thị supported domains
        logger.info("4. Các legal domains được hỗ trợ:")
        domains = service.get_supported_domains()
        for code, name in domains.items():
            logger.info(f"   {code}: {name}")
        
        return service
        
    except PineconeServiceError as e:
        logger.error(f"❌ Lỗi PineconeService: {e.message} (Code: {e.error_code})")
        return None
    except Exception as e:
        logger.error(f"❌ Lỗi khác: {str(e)}")
        return None


def demonstrate_document_processing():
    """
    Minh họa xử lý tài liệu pháp lý
    Demonstrate legal document processing
    """
    logger.info("\n=== DEMO: Xử lý tài liệu pháp lý ===")
    
    try:
        # Tạo document processor
        processor = LegalDocumentProcessor(chunk_size=500, chunk_overlap=50)
        
        # Lấy dữ liệu mẫu
        sample_docs = create_sample_legal_documents()
        processed_documents = []
        
        for doc_data in sample_docs:
            logger.info(f"Xử lý tài liệu: {doc_data['title']}")
            
            # Tạo metadata
            metadata = VietnameseLegalMetadataBuilder.build_metadata(
                document_type=doc_data["document_type"],
                title=doc_data["title"],
                legal_domain=doc_data["legal_domain"],
                issuing_authority=doc_data["issuing_authority"],
                effective_date=doc_data["effective_date"]
            )
            
            # Xử lý tài liệu thành chunks
            chunks = processor.process_legal_document(doc_data["content"], metadata)
            processed_documents.extend(chunks)
            
            logger.info(f"   ✅ Chia thành {len(chunks)} chunks")
            
            # Hiển thị thông tin cấu trúc
            structure = processor.extract_legal_structure(doc_data["content"])
            logger.info(f"   📄 Cấu trúc: {len(structure['chapters'])} chương, "
                       f"{len(structure['articles'])} điều")
        
        logger.info(f"✅ Tổng cộng xử lý {len(processed_documents)} chunks từ {len(sample_docs)} tài liệu")
        return processed_documents
        
    except Exception as e:
        logger.error(f"❌ Lỗi xử lý tài liệu: {str(e)}")
        return []


def demonstrate_metadata_building():
    """
    Minh họa xây dựng metadata
    Demonstrate metadata building
    """
    logger.info("\n=== DEMO: Xây dựng metadata ===")
    
    try:
        # Test metadata builder
        logger.info("1. Tạo metadata từ thông tin cơ bản...")
        metadata = VietnameseLegalMetadataBuilder.build_metadata(
            document_type="bo_luat",
            title="Bộ luật Dân sự 2015",
            legal_domain="dan_su",
            issuing_authority="quoc_hoi",
            article_number="123",
            chapter="V",
            effective_date="2017-01-01"
        )
        
        logger.info(f"   📋 Title: {metadata.title}")
        logger.info(f"   🏛️ Authority: {metadata.issuing_authority}")
        logger.info(f"   📑 Article: {metadata.article_number}")
        logger.info(f"   📅 Effective: {metadata.effective_date}")
        
        # Test extraction from title
        logger.info("2. Trích xuất metadata từ tiêu đề...")
        title = "Nghị định số 123/2020/NĐ-CP về quản lý thuế"
        extracted = VietnameseLegalMetadataBuilder.extract_metadata_from_title(title)
        logger.info(f"   📝 Extracted: {extracted}")
        
        # Test validation
        logger.info("3. Kiểm tra validation...")
        valid_domain = VietnameseLegalMetadataBuilder.validate_legal_domain("dan_su")
        invalid_domain = VietnameseLegalMetadataBuilder.validate_legal_domain("invalid")
        logger.info(f"   ✅ 'dan_su' valid: {valid_domain}")
        logger.info(f"   ❌ 'invalid' valid: {invalid_domain}")
        
        # Show supported types
        logger.info("4. Các loại tài liệu được hỗ trợ:")
        doc_types = VietnameseLegalMetadataBuilder.get_supported_document_types()
        for code, name in doc_types.items():
            logger.info(f"   {code}: {name}")
        
        return metadata
        
    except Exception as e:
        logger.error(f"❌ Lỗi xây dựng metadata: {str(e)}")
        return None


def demonstrate_search_simulation():
    """
    Minh họa mô phỏng tìm kiếm (không cần Pinecone thật)
    Demonstrate search simulation (without real Pinecone)
    """
    logger.info("\n=== DEMO: Mô phỏng tìm kiếm ===")
    
    try:
        # Tạo mock search results
        mock_results = [
            VectorSearchResult(
                id="doc1_chunk_0",
                score=0.95,
                metadata={
                    "title": "Bộ luật Dân sự 2015",
                    "legal_domain": "dan_su",
                    "article_number": "1",
                    "chapter": "I"
                },
                content="Bộ luật này quy định về quan hệ dân sự...",
                legal_domain="dan_su",
                article_number="1",
                citation="Bộ luật Dân sự 2015, Điều 1, Chương I"
            ),
            VectorSearchResult(
                id="doc1_chunk_1", 
                score=0.87,
                metadata={
                    "title": "Bộ luật Dân sự 2015",
                    "legal_domain": "dan_su",
                    "article_number": "2"
                },
                content="Nguyên tắc cơ bản của pháp luật dân sự...",
                legal_domain="dan_su",
                article_number="2",
                citation="Bộ luật Dân sự 2015, Điều 2"
            )
        ]
        
        # Hiển thị kết quả tìm kiếm
        query = "quan hệ dân sự là gì?"
        logger.info(f"🔍 Query: '{query}'")
        logger.info(f"📊 Tìm thấy {len(mock_results)} kết quả:")
        
        for i, result in enumerate(mock_results, 1):
            logger.info(f"   {i}. Score: {result.score:.2f}")
            logger.info(f"      📄 {result.citation}")
            logger.info(f"      📝 {result.content[:100]}...")
            logger.info(f"      🏷️ Domain: {result.legal_domain}")
        
        return mock_results
        
    except Exception as e:
        logger.error(f"❌ Lỗi mô phỏng tìm kiếm: {str(e)}")
        return []


def main():
    """
    Chạy demo chính
    Run main demo
    """
    logger.info("🚀 Bắt đầu Demo PineconeService cho Vietnamese Legal AI Chatbot")
    logger.info("=" * 70)
    
    # Setup environment
    setup_environment()
    
    # 1. Demo khởi tạo service
    service = demonstrate_service_initialization()
    
    # 2. Demo xử lý tài liệu
    processed_docs = demonstrate_document_processing()
    
    # 3. Demo xây dựng metadata
    metadata = demonstrate_metadata_building()
    
    # 4. Demo mô phỏng tìm kiếm
    search_results = demonstrate_search_simulation()
    
    # Summary
    logger.info("\n" + "=" * 70)
    logger.info("📊 TÓNG KẾT DEMO:")
    logger.info(f"✅ Service initialization: {'Thành công' if service else 'Thất bại'}")
    logger.info(f"✅ Document processing: {len(processed_docs)} chunks processed")
    logger.info(f"✅ Metadata building: {'Thành công' if metadata else 'Thất bại'}")
    logger.info(f"✅ Search simulation: {len(search_results)} results")
    
    logger.info("\n🎉 Demo hoàn thành!")
    logger.info("💡 Để sử dụng thực tế, cần cung cấp:")
    logger.info("   - PINECONE_API_KEY")
    logger.info("   - OPENAI_API_KEY") 
    logger.info("   - PINECONE_ENVIRONMENT")
    logger.info("   - Cài đặt dependencies: pip install pinecone-client openai langchain")


if __name__ == "__main__":
    main()
