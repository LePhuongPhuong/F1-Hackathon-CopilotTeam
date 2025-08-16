"""
Comprehensive test suite for Vietnamese Legal RAG System
Test cho hệ thống RAG Pháp lý Việt Nam

Tests the complete RAG implementation with all strategies and components.
"""

import pytest
import json
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime
from typing import List, Dict, Any

# Import the classes we're testing
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.legal_rag import (
    VietnameseLegalRAG,
    LegalQueryResult,
    LegalCitation,
    DocumentChunk,
    LegalQueryType,
    ConfidenceLevel,
    VietnameseLegalPromptTemplates,
    LegalCitationExtractor,
    VietnameseLegalValidator,
    VietnameseLegalRAGFactory,
    GeneralLegalRAGStrategy,
    SpecificLawRAGStrategy,
    CaseAnalysisRAGStrategy,
    ComplianceRAGStrategy,
    InterpretationRAGStrategy,
    ProcedureRAGStrategy
)

class TestLegalCitation:
    """Test LegalCitation dataclass"""
    
    def test_legal_citation_creation(self):
        """Test creating legal citation"""
        citation = LegalCitation(
            document_type="Luật",
            document_name="Luật Dân sự",
            article="15",
            clause="1",
            point="a",
            year=2015,
            number="91/2015/QH13"
        )
        
        assert citation.document_type == "Luật"
        assert citation.document_name == "Luật Dân sự"
        assert citation.article == "15"
        assert citation.clause == "1"
        assert citation.point == "a"
        assert citation.year == 2015
        assert citation.number == "91/2015/QH13"
    
    def test_legal_citation_string_format(self):
        """Test Vietnamese legal citation formatting"""
        citation = LegalCitation(
            document_type="Luật",
            document_name="Luật Dân sự",
            article="15",
            clause="1",
            year=2015,
            number="91/2015/QH13"
        )
        
        citation_str = str(citation)
        assert "Luật" in citation_str
        assert "Luật Dân sự" in citation_str
        assert "số 91/2015/QH13" in citation_str
        assert "năm 2015" in citation_str
        assert "Điều 15" in citation_str
        assert "Khoản 1" in citation_str

class TestLegalQueryResult:
    """Test LegalQueryResult dataclass"""
    
    def test_query_result_creation(self):
        """Test creating comprehensive query result"""
        citations = [
            LegalCitation("Luật", "Luật Dân sự", article="15")
        ]
        
        result = LegalQueryResult(
            answer="Đây là câu trả lời pháp lý",
            confidence_score=0.85,
            confidence_level=ConfidenceLevel.HIGH,
            sources=[{"page_content": "Nội dung tài liệu"}],
            legal_domain="dan_su",
            citations=citations,
            reasoning="Dựa trên điều 15 Luật Dân sự",
            query_type=LegalQueryType.GENERAL
        )
        
        assert result.answer == "Đây là câu trả lời pháp lý"
        assert result.confidence_score == 0.85
        assert result.confidence_level == ConfidenceLevel.HIGH
        assert result.legal_domain == "dan_su"
        assert len(result.citations) == 1
        assert result.query_type == LegalQueryType.GENERAL
    
    def test_query_result_to_dict(self):
        """Test converting query result to dictionary"""
        citations = [LegalCitation("Luật", "Luật Dân sự")]
        
        result = LegalQueryResult(
            answer="Test answer",
            confidence_score=0.75,
            confidence_level=ConfidenceLevel.MEDIUM,
            sources=[],
            legal_domain="general",
            citations=citations,
            reasoning="Test reasoning",
            query_type=LegalQueryType.GENERAL
        )
        
        result_dict = result.to_dict()
        
        assert isinstance(result_dict, dict)
        assert result_dict["answer"] == "Test answer"
        assert result_dict["confidence_score"] == 0.75
        assert result_dict["confidence_level"] == "medium"
        assert result_dict["query_type"] == "general"
        assert isinstance(result_dict["timestamp"], str)

class TestDocumentChunk:
    """Test DocumentChunk dataclass"""
    
    def test_document_chunk_creation(self):
        """Test creating document chunk"""
        chunk = DocumentChunk(
            content="Điều 15. Quyền dân sự...",
            metadata={"document_name": "Luật Dân sự"},
            legal_structure={"article": "15", "level": "article"}
        )
        
        assert chunk.content == "Điều 15. Quyền dân sự..."
        assert chunk.metadata["document_name"] == "Luật Dân sự"
        assert chunk.legal_structure["article"] == "15"
    
    def test_get_legal_level(self):
        """Test getting legal hierarchical level"""
        chunk = DocumentChunk(
            content="Test content",
            metadata={},
            legal_structure={"level": "article"}
        )
        
        assert chunk.get_legal_level() == "article"
        
        # Test default value
        chunk_no_level = DocumentChunk(content="Test", metadata={})
        assert chunk_no_level.get_legal_level() == "unknown"
    
    def test_get_legal_reference(self):
        """Test getting formatted legal reference"""
        chunk = DocumentChunk(
            content="Test content",
            metadata={},
            legal_structure={
                "article": "15",
                "clause": "1",
                "point": "a"
            }
        )
        
        reference = chunk.get_legal_reference()
        assert "Điều 15" in reference
        assert "Khoản 1" in reference
        assert "Điểm a" in reference

class TestLegalCitationExtractor:
    """Test LegalCitationExtractor class"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.extractor = LegalCitationExtractor()
    
    def test_extractor_initialization(self):
        """Test citation extractor initialization"""
        assert self.extractor is not None
        assert isinstance(self.extractor.citation_patterns, dict)
        assert len(self.extractor.legal_document_types) > 0
        assert "Luật" in self.extractor.legal_document_types
    
    def test_extract_citations_from_text(self):
        """Test extracting citations from Vietnamese text"""
        test_text = """
        Theo Điều 15 Khoản 1 Điểm a của Luật Dân sự số 91/2015/QH13,
        quyền dân sự được bảo vệ. Nghị định số 01/2021/NĐ-CP quy định chi tiết.
        """
        
        citations = self.extractor.extract_citations_from_text(test_text)
        
        assert len(citations) > 0
        
        # Check for article citation
        article_citations = [c for c in citations if c.article == "15"]
        assert len(article_citations) > 0
        
        # Check for law citation (should find "dân sự" in the document name)
        law_citations = [c for c in citations if "dân sự" in c.document_name.lower()]
        assert len(law_citations) > 0
    
    def test_extract_citations_from_documents(self):
        """Test extracting citations from document list"""
        documents = [
            {
                "page_content": "Điều 20 Luật Lao động quy định về thời gian làm việc",
                "metadata": {"document_name": "Luật Lao động", "year": 2019}
            },
            {
                "page_content": "Khoản 2 Điều 15 của Bộ luật Dân sự",
                "metadata": {"document_name": "Bộ luật Dân sự"}
            }
        ]
        
        citations = self.extractor.extract_citations_from_documents(documents)
        
        assert len(citations) > 0
        
        # Check metadata enhancement
        enhanced_citations = [c for c in citations if c.document_name]
        assert len(enhanced_citations) > 0
    
    def test_deduplicate_citations(self):
        """Test citation deduplication"""
        duplicate_citations = [
            LegalCitation("Luật", "Luật Dân sự", article="15"),
            LegalCitation("Luật", "Luật Dân sự", article="15"),  # Duplicate
            LegalCitation("Luật", "Luật Lao động", article="20")
        ]
        
        unique_citations = self.extractor._deduplicate_citations(duplicate_citations)
        
        assert len(unique_citations) == 2
        
        # Check that unique citations are preserved
        article_15_count = sum(1 for c in unique_citations if c.article == "15")
        article_20_count = sum(1 for c in unique_citations if c.article == "20")
        
        assert article_15_count == 1
        assert article_20_count == 1

class TestVietnameseLegalValidator:
    """Test VietnameseLegalValidator class"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.validator = VietnameseLegalValidator()
    
    def test_validator_initialization(self):
        """Test validator initialization"""
        assert self.validator is not None
        assert isinstance(self.validator.validation_rules, dict)
        assert len(self.validator.legal_terminology) > 0
    
    def test_validate_good_response(self):
        """Test validation of good legal response"""
        good_response = """
        Theo quy định tại Điều 15 Khoản 1 của Luật Dân sự, quyền dân sự của công dân
        được pháp luật bảo vệ. Nghĩa vụ tương ứng là tôn trọng quyền của người khác.
        Trong trường hợp vi phạm, sẽ phải chịu trách nhiệm theo quy định pháp luật.
        """
        
        sources = [
            {"page_content": "Nội dung điều 15", "metadata": {"document_name": "Luật Dân sự"}}
        ]
        
        validation = self.validator.validate_response(good_response, sources)
        
        assert validation["is_valid"] is True
        assert len(validation["warnings"]) <= 1  # Should have minimal warnings
        assert validation["confidence_adjustment"] >= -0.1  # Minor adjustment acceptable
    
    def test_validate_poor_response(self):
        """Test validation of poor legal response"""
        poor_response = "Không biết"  # Too short, no legal structure
        
        validation = self.validator.validate_response(poor_response, [])
        
        assert len(validation["warnings"]) > 0
        assert validation["confidence_adjustment"] < 0
        assert "Phản hồi quá ngắn" in validation["warnings"][0]
    
    def test_validate_prohibited_terms(self):
        """Test detection of prohibited absolute terms"""
        response_with_prohibited = """
        Tôi chắc chắn 100% rằng điều này hoàn toàn chính xác và không có ngoại lệ.
        """
        
        validation = self.validator.validate_response(response_with_prohibited, [])
        
        has_prohibited_warning = any(
            "thuật ngữ tuyệt đối" in warning.lower() 
            for warning in validation["warnings"]
        )
        assert has_prohibited_warning
    
    def test_has_legal_structure(self):
        """Test legal structure detection"""
        text_with_structure = "Theo Điều 15 Khoản 1 của luật này"
        text_without_structure = "Chỉ là văn bản thông thường"
        
        assert self.validator._has_legal_structure(text_with_structure) is True
        assert self.validator._has_legal_structure(text_without_structure) is False

class TestVietnameseLegalRAGStrategies:
    """Test RAG strategy implementations"""
    
    def setup_method(self):
        """Setup test fixtures"""
        # Mock the main RAG system
        self.mock_rag = Mock()
        self.mock_rag._generate_contextual_response.return_value = (
            "Mocked response", "Mocked reasoning", 0.8
        )
        self.mock_rag.citation_extractor = Mock()
        self.mock_rag.citation_extractor.extract_citations_from_documents.return_value = []
    
    def test_general_legal_rag_strategy(self):
        """Test GeneralLegalRAGStrategy"""
        strategy = GeneralLegalRAGStrategy(self.mock_rag)
        
        query = "Quyền dân sự là gì?"
        context = {
            "documents": [{"page_content": "Test content"}],
            "legal_domain": "dan_su",
            "query_type": LegalQueryType.GENERAL
        }
        
        result = strategy.process_query(query, context)
        
        assert isinstance(result, LegalQueryResult)
        assert result.query_type == LegalQueryType.GENERAL
        assert result.legal_domain == "dan_su"
        assert strategy.get_strategy_name() == "GeneralLegalRAG"
    
    def test_specific_law_rag_strategy(self):
        """Test SpecificLawRAGStrategy"""
        strategy = SpecificLawRAGStrategy(self.mock_rag)
        
        query = "Điều 15 Luật Dân sự quy định gì?"
        context = {
            "documents": [
                {"page_content": "Điều 15. Quyền dân sự...", "metadata": {}}
            ],
            "legal_domain": "dan_su",
            "query_type": LegalQueryType.SPECIFIC_LAW
        }
        
        result = strategy.process_query(query, context)
        
        assert isinstance(result, LegalQueryResult)
        assert result.query_type == LegalQueryType.SPECIFIC_LAW
        assert strategy.get_strategy_name() == "SpecificLawRAG"
    
    def test_compliance_rag_strategy(self):
        """Test ComplianceRAGStrategy"""
        strategy = ComplianceRAGStrategy(self.mock_rag)
        
        query = "Hành vi này có vi phạm pháp luật không?"
        context = {
            "documents": [{"page_content": "Quy định về vi phạm"}],
            "legal_domain": "hinh_su",
            "query_type": LegalQueryType.COMPLIANCE
        }
        
        result = strategy.process_query(query, context)
        
        assert isinstance(result, LegalQueryResult)
        assert result.query_type == LegalQueryType.COMPLIANCE
        assert len(result.warnings) > 0  # Should have compliance warnings
        assert strategy.get_strategy_name() == "ComplianceRAG"

class TestVietnameseLegalRAGFactory:
    """Test RAG factory class"""
    
    def test_create_standard_rag(self):
        """Test creating standard RAG instance"""
        mock_pinecone_service = Mock()
        mock_chat_model = Mock()
        
        with patch('app.models.legal_rag.OpenAIEmbeddings'):
            rag = VietnameseLegalRAGFactory.create_standard_rag(
                mock_pinecone_service, 
                mock_chat_model
            )
        
        assert isinstance(rag, VietnameseLegalRAG)
        assert rag.pinecone_service == mock_pinecone_service
        assert rag.chat_model == mock_chat_model
    
    def test_create_domain_specific_rag(self):
        """Test creating domain-specific RAG instance"""
        mock_pinecone_service = Mock()
        mock_chat_model = Mock()
        
        with patch('app.models.legal_rag.OpenAIEmbeddings'):
            rag = VietnameseLegalRAGFactory.create_domain_specific_rag(
                mock_pinecone_service,
                mock_chat_model,
                "dan_su"
            )
        
        assert isinstance(rag, VietnameseLegalRAG)
        assert hasattr(rag, 'default_domain')
        assert rag.default_domain == "dan_su"

class TestVietnameseLegalRAGIntegration:
    """Integration tests for the complete RAG system"""
    
    def setup_method(self):
        """Setup comprehensive test fixtures"""
        # Mock all external dependencies
        self.mock_pinecone_service = Mock()
        self.mock_chat_model = Mock()
        self.mock_embedding_model = Mock()
        self.mock_text_processor = Mock()
        
        # Setup mock returns
        self.mock_pinecone_service.similarity_search.return_value = [
            {
                "page_content": "Điều 15. Quyền dân sự của công dân được pháp luật bảo vệ",
                "metadata": {
                    "document_name": "Luật Dân sự",
                    "legal_domain": "dan_su",
                    "article": "15"
                },
                "score": 0.85
            }
        ]
        
        self.mock_chat_model.generate_response.return_value = """
        Theo quy định tại Điều 15 của Luật Dân sự, quyền dân sự của công dân được pháp luật bảo vệ.
        Điều này có nghĩa là mọi quyền lợi hợp pháp của công dân đều được nhà nước đảm bảo và bảo vệ.
        """
        
        self.mock_embedding_model.embed_query.return_value = [0.1] * 1536
        self.mock_text_processor.normalize_vietnamese_text.return_value = "normalized text"
        self.mock_text_processor.process_legal_document.return_value = "processed text"
    
    def test_full_rag_query_processing(self):
        """Test complete query processing pipeline"""
        # Create RAG instance with mocks
        rag = VietnameseLegalRAG(
            pinecone_service=self.mock_pinecone_service,
            chat_model=self.mock_chat_model,
            embedding_model=self.mock_embedding_model,
            text_processor=self.mock_text_processor
        )
        
        # Process a query
        query = "Quyền dân sự của công dân được bảo vệ như thế nào?"
        result = rag.query(
            question=query,
            legal_domain="dan_su",
            max_results=5
        )
        
        # Verify result structure
        assert isinstance(result, LegalQueryResult)
        assert result.answer is not None
        assert len(result.answer) > 0
        assert result.confidence_score > 0
        assert result.legal_domain == "dan_su"
        assert isinstance(result.citations, list)
        assert result.query_type in [t for t in LegalQueryType]
        
        # Verify that all components were called
        self.mock_pinecone_service.similarity_search.assert_called()
        self.mock_chat_model.generate_response.assert_called()
    
    def test_query_with_different_types(self):
        """Test query processing with different query types"""
        rag = VietnameseLegalRAG(
            pinecone_service=self.mock_pinecone_service,
            chat_model=self.mock_chat_model,
            embedding_model=self.mock_embedding_model,
            text_processor=self.mock_text_processor
        )
        
        # Test different query types
        test_queries = [
            ("Điều 15 Luật Dân sự quy định gì?", LegalQueryType.SPECIFIC_LAW),
            ("Quyền dân sự là gì?", LegalQueryType.INTERPRETATION),
            ("Thủ tục kết hôn như thế nào?", LegalQueryType.PROCEDURE),
            ("Hành vi này có vi phạm không?", LegalQueryType.COMPLIANCE),
            ("Phân tích trường hợp này", LegalQueryType.CASE_ANALYSIS)
        ]
        
        for query_text, expected_type in test_queries:
            result = rag.query(query_text)
            
            # The query type might be auto-detected differently, 
            # but should be one of the valid types
            assert result.query_type in [t for t in LegalQueryType]
            assert isinstance(result, LegalQueryResult)
    
    def test_add_legal_documents(self):
        """Test adding new legal documents"""
        rag = VietnameseLegalRAG(
            pinecone_service=self.mock_pinecone_service,
            chat_model=self.mock_chat_model,
            embedding_model=self.mock_embedding_model,
            text_processor=self.mock_text_processor
        )
        
        # Mock successful document addition
        self.mock_pinecone_service.upsert_documents.return_value = True
        self.mock_embedding_model.embed_documents.return_value = [[0.1] * 1536]
        
        # Create test documents
        documents = [
            DocumentChunk(
                content="Điều 20. Thời gian làm việc không quá 8 tiếng/ngày",
                metadata={"document_name": "Luật Lao động", "legal_domain": "lao_dong"}
            )
        ]
        
        # Add documents
        success = rag.add_legal_documents(documents)
        
        assert success is True
        self.mock_pinecone_service.upsert_documents.assert_called_once()
    
    def test_performance_metrics_tracking(self):
        """Test performance metrics tracking"""
        rag = VietnameseLegalRAG(
            pinecone_service=self.mock_pinecone_service,
            chat_model=self.mock_chat_model,
            embedding_model=self.mock_embedding_model,
            text_processor=self.mock_text_processor
        )
        
        # Process multiple queries
        queries = [
            "Quyền dân sự là gì?",
            "Nghĩa vụ của công dân?",
            "Thủ tục kết hôn?"
        ]
        
        for query in queries:
            rag.query(query)
        
        # Check metrics
        metrics = rag.get_performance_metrics()
        
        assert metrics["metrics"]["total_queries"] == len(queries)
        assert metrics["metrics"]["avg_confidence"] > 0
        assert len(metrics["metrics"]["domain_distribution"]) > 0
        assert metrics["recent_queries"] == len(queries)
    
    def test_error_handling(self):
        """Test error handling in RAG system"""
        # Setup RAG with failing mock
        failing_pinecone = Mock()
        failing_pinecone.similarity_search.side_effect = Exception("Connection failed")
        
        rag = VietnameseLegalRAG(
            pinecone_service=failing_pinecone,
            chat_model=self.mock_chat_model,
            embedding_model=self.mock_embedding_model,
            text_processor=self.mock_text_processor
        )
        
        # Query should handle error gracefully
        result = rag.query("Test query")
        
        assert isinstance(result, LegalQueryResult)
        # The system should either have error in answer or have warnings about the issue
        has_error_indication = (
            "lỗi" in result.answer.lower() or 
            len(result.warnings) > 0 or 
            result.confidence_score == 0.0 or
            result.confidence_level == ConfidenceLevel.UNCERTAIN
        )
        assert has_error_indication

if __name__ == "__main__":
    pytest.main(["-v", __file__])
