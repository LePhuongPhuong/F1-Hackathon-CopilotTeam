"""
Test cases for PineconeService
Test cho dịch vụ Pinecone
"""

import pytest
import os
from unittest.mock import Mock, patch, MagicMock
from typing import List, Dict, Any

from app.services.pinecone_service import (
    PineconeService,
    PineconeServiceError,
    DocumentMetadata,
    VectorSearchResult,
    LegalDocumentProcessor,
    VietnameseLegalMetadataBuilder,
    PineconeServiceFactory
)
from app.utils.config import Settings


class TestPineconeService:
    """Test class for PineconeService"""
    
    @pytest.fixture
    def mock_settings(self):
        """Mock settings for testing"""
        return Settings(
            pinecone_api_key="test-api-key",
            pinecone_environment="us-west1-gcp",
            pinecone_index_name="test-legal-docs",
            pinecone_dimension=1536,
            openai_api_key="test-openai-key"
        )
    
    @pytest.fixture
    def sample_metadata(self):
        """Sample document metadata"""
        return DocumentMetadata(
            document_id="test-doc-1",
            title="Bộ luật Dân sự 2015",
            legal_domain="dan_su",
            document_type="Bộ luật",
            article_number="123",
            chapter="V",
            issuing_authority="Quốc hội",
            effective_date="2017-01-01"
        )
    
    def test_supported_legal_domains(self):
        """Test supported legal domains"""
        expected_domains = {
            "hien_phap": "Hiến pháp",
            "dan_su": "Bộ luật Dân sự", 
            "hinh_su": "Bộ luật Hình sự",
            "lao_dong": "Bộ luật Lao động",
            "thuong_mai": "Luật Thương mại",
            "hanh_chinh": "Luật Hành chính",
            "thue": "Luật Thuế",
            "bat_dong_san": "Luật Bất động sản"
        }
        
        assert PineconeService.SUPPORTED_LEGAL_DOMAINS == expected_domains
    
    @patch('app.services.pinecone_service.PINECONE_AVAILABLE', False)
    def test_pinecone_unavailable_error(self, mock_settings):
        """Test error when Pinecone dependencies unavailable"""
        with pytest.raises(PineconeServiceError) as exc_info:
            PineconeService(
                api_key=mock_settings.pinecone_api_key,
                environment=mock_settings.pinecone_environment,
                index_name=mock_settings.pinecone_index_name,
                openai_api_key=mock_settings.openai_api_key
            )
        
        assert exc_info.value.error_code == "DEPENDENCY_ERROR"
        assert "thiếu dependencies" in exc_info.value.message
    
    @patch('app.services.pinecone_service.Pinecone')
    @patch('app.services.pinecone_service.OpenAIEmbeddings')
    def test_service_initialization(self, mock_embeddings, mock_pinecone, mock_settings):
        """Test service initialization"""
        # Mock Pinecone client
        mock_client = Mock()
        mock_index = Mock()
        mock_pinecone.return_value = mock_client
        mock_client.list_indexes.return_value = [Mock(name="test-legal-docs")]
        mock_client.Index.return_value = mock_index
        
        # Mock embeddings
        mock_embeddings_instance = Mock()
        mock_embeddings.return_value = mock_embeddings_instance
        
        # Create service
        service = PineconeService(
            api_key=mock_settings.pinecone_api_key,
            environment=mock_settings.pinecone_environment,
            index_name=mock_settings.pinecone_index_name,
            openai_api_key=mock_settings.openai_api_key
        )
        
        # Assertions
        assert service.api_key == mock_settings.pinecone_api_key
        assert service.index_name == mock_settings.pinecone_index_name
        assert service.dimension == 1536
        assert service.pinecone_client == mock_client
        assert service.index == mock_index
        assert service.embeddings == mock_embeddings_instance
    
    def test_validate_legal_domain(self):
        """Test legal domain validation"""
        # Test với Pinecone mock để tránh dependency error
        with patch('app.services.pinecone_service.PINECONE_AVAILABLE', True), \
             patch('app.services.pinecone_service.Pinecone'), \
             patch('app.services.pinecone_service.OpenAIEmbeddings'):
            
            service = PineconeService("test", "test", "test")
            
            # Valid domains
            assert service._validate_legal_domain("dan_su") == True
            assert service._validate_legal_domain("hinh_su") == True
            
            # Invalid domain
            assert service._validate_legal_domain("invalid_domain") == False
    
    def test_build_citation(self):
        """Test citation building"""
        with patch('app.services.pinecone_service.PINECONE_AVAILABLE', True), \
             patch('app.services.pinecone_service.Pinecone'), \
             patch('app.services.pinecone_service.OpenAIEmbeddings'):
            
            service = PineconeService("test", "test", "test")
            
            metadata = {
                "title": "Bộ luật Dân sự",
                "article_number": "123",
                "clause": "2",
                "chapter": "V",
                "issuing_authority": "Quốc hội"
            }
            
            citation = service._build_citation(metadata)
            expected = "Bộ luật Dân sự, Điều 123, Khoản 2, Chương V, (Quốc hội)"
            
            assert citation == expected
    
    def test_health_check(self):
        """Test health check functionality"""
        with patch('app.services.pinecone_service.PINECONE_AVAILABLE', True), \
             patch('app.services.pinecone_service.Pinecone') as mock_pinecone, \
             patch('app.services.pinecone_service.OpenAIEmbeddings'):
            
            # Mock successful setup
            mock_client = Mock()
            mock_index = Mock()
            mock_pinecone.return_value = mock_client
            mock_client.list_indexes.return_value = [Mock(name="test-index")]
            mock_client.Index.return_value = mock_index
            
            service = PineconeService("test", "test", "test-index")
            
            # Mock get_index_stats
            service.get_index_stats = Mock(return_value={"total_vectors": 100})
            
            health = service.health_check()
            
            assert health["service"] == "PineconeService"
            assert health["status"] == "healthy"
            assert health["index_ready"] == True
            assert health["embeddings_ready"] == False  # No OpenAI key provided
            assert "timestamp" in health


class TestLegalDocumentProcessor:
    """Test class for LegalDocumentProcessor"""
    
    @pytest.fixture
    def processor(self):
        """Create processor instance"""
        return LegalDocumentProcessor(chunk_size=500, chunk_overlap=50)
    
    @pytest.fixture
    def sample_legal_content(self):
        """Sample Vietnamese legal document content"""
        return """
        CHƯƠNG I
        QUY ĐỊNH CHUNG
        
        Điều 1. Phạm vi điều chỉnh
        1. Bộ luật này quy định về quan hệ dân sự.
        2. Quan hệ dân sự là quan hệ tài sản và quan hệ nhân thân.
        
        Điều 2. Nguyên tắc cơ bản
        1. Bình đẳng trong quan hệ dân sự.
        a) Các chủ thể có quyền bình đẳng;
        b) Không phân biệt đối xử.
        """
    
    def test_extract_legal_structure(self, processor, sample_legal_content):
        """Test extraction of legal document structure"""
        structure = processor.extract_legal_structure(sample_legal_content)
        
        # Check chapters
        assert len(structure["chapters"]) == 1
        assert structure["chapters"][0]["number"] == "I"
        assert "QUY ĐỊNH CHUNG" in structure["chapters"][0]["title"]
        
        # Check articles
        assert len(structure["articles"]) == 2
        assert structure["articles"][0]["number"] == "1"
        assert "Phạm vi điều chỉnh" in structure["articles"][0]["title"]
    
    def test_identify_chunk_type(self, processor):
        """Test chunk type identification"""
        assert processor._identify_chunk_type("CHƯƠNG I") == "chapter"
        assert processor._identify_chunk_type("Điều 1. Test") == "article"
        assert processor._identify_chunk_type("1. This is a clause") == "clause"
        assert processor._identify_chunk_type("a) This is a point") == "point"
        assert processor._identify_chunk_type("Regular content") == "content"
    
    def test_extract_article_from_chunk(self, processor):
        """Test article information extraction from chunk"""
        # Test article extraction
        article_chunk = "Điều 123. Nghĩa vụ của cá nhân"
        article_info = processor._extract_article_from_chunk(article_chunk)
        assert article_info == {"article_number": "123"}
        
        # Test clause extraction
        clause_chunk = "1. Đây là khoản đầu tiên"
        clause_info = processor._extract_article_from_chunk(clause_chunk)
        assert clause_info == {"clause": "1"}
        
        # Test no match
        normal_chunk = "Nội dung bình thường"
        normal_info = processor._extract_article_from_chunk(normal_chunk)
        assert normal_info is None


class TestVietnameseLegalMetadataBuilder:
    """Test class for VietnameseLegalMetadataBuilder"""
    
    def test_build_metadata(self):
        """Test metadata building"""
        metadata = VietnameseLegalMetadataBuilder.build_metadata(
            document_type="bo_luat",
            title="Bộ luật Dân sự 2015",
            legal_domain="dan_su",
            issuing_authority="quoc_hoi",
            article_number="123",
            effective_date="2017-01-01"
        )
        
        assert metadata.title == "Bộ luật Dân sự 2015"
        assert metadata.legal_domain == "dan_su"
        assert metadata.document_type == "Bộ luật"
        assert metadata.issuing_authority == "Quốc hội"
        assert metadata.article_number == "123"
        assert metadata.language == "vietnamese"
    
    def test_validate_legal_domain(self):
        """Test legal domain validation"""
        assert VietnameseLegalMetadataBuilder.validate_legal_domain("dan_su") == True
        assert VietnameseLegalMetadataBuilder.validate_legal_domain("invalid") == False
    
    def test_validate_document_type(self):
        """Test document type validation"""
        assert VietnameseLegalMetadataBuilder.validate_document_type("bo_luat") == True
        assert VietnameseLegalMetadataBuilder.validate_document_type("invalid") == False
    
    def test_extract_metadata_from_title(self):
        """Test metadata extraction from title"""
        title = "Bộ luật Dân sự số 91/2015/QH13"
        extracted = VietnameseLegalMetadataBuilder.extract_metadata_from_title(title)
        
        assert extracted["document_type"] == "bo_luat"
        assert extracted["legal_domain"] == "dan_su"
        assert extracted["document_number"] == "91/2015/QH13"
        assert extracted["year"] == "2015"


class TestPineconeServiceFactory:
    """Test class for PineconeServiceFactory"""
    
    @patch('app.services.pinecone_service.Settings')
    def test_create_from_env(self, mock_settings_class):
        """Test creating service from environment"""
        # Mock Settings
        mock_settings = Mock()
        mock_settings.pinecone_api_key = "test-key"
        mock_settings.pinecone_environment = "test-env"
        mock_settings.pinecone_index_name = "test-index"
        mock_settings.pinecone_dimension = 1536
        mock_settings.openai_api_key = "test-openai"
        mock_settings_class.return_value = mock_settings
        
        with patch('app.services.pinecone_service.PineconeService') as mock_service:
            PineconeServiceFactory.create_from_env()
            
            mock_service.assert_called_once_with(
                api_key="test-key",
                environment="test-env",
                index_name="test-index",
                dimension=1536,
                openai_api_key="test-openai"
            )


if __name__ == "__main__":
    # Run a simple test
    print("Running basic tests for PineconeService...")
    
    # Test supported domains
    domains = PineconeService.SUPPORTED_LEGAL_DOMAINS
    print(f"Supported legal domains: {len(domains)}")
    for code, name in domains.items():
        print(f"  {code}: {name}")
    
    # Test metadata builder
    print("\nTesting metadata builder...")
    metadata = VietnameseLegalMetadataBuilder.build_metadata(
        document_type="bo_luat",
        title="Bộ luật Dân sự 2015",
        legal_domain="dan_su",
        issuing_authority="quoc_hoi"
    )
    print(f"Created metadata: {metadata.title} - {metadata.document_type}")
    
    # Test document processor
    print("\nTesting document processor...")
    processor = LegalDocumentProcessor()
    sample_content = "Điều 1. Test content\n1. First clause\na) First point"
    structure = processor.extract_legal_structure(sample_content)
    print(f"Extracted structure: {len(structure['articles'])} articles")
    
    print("\nAll basic tests completed successfully!")
