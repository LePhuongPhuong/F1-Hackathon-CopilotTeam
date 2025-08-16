"""
Vietnamese Legal RAG System
Hệ thống RAG Pháp lý Việt Nam

Retrieval-Augmented Generation system for Vietnamese legal documents.
Hệ thống tạo văn bản tăng cường truy xuất cho tài liệu pháp lý Việt Nam.
"""

import re
import json
import logging
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum

# Core dependencies
try:
    from langchain.chains import RetrievalQA
    from langchain.prompts import PromptTemplate
    from langchain.schema import Document
    from langchain_openai import OpenAIEmbeddings
    from langchain_community.vectorstores import Pinecone
except ImportError:
    # Fallback imports for development/testing
    class PromptTemplate:
        def __init__(self, input_variables=None, template=""):
            self.input_variables = input_variables or []
            self.template = template
            
        def format(self, **kwargs):
            result = self.template
            for key, value in kwargs.items():
                result = result.replace(f"{{{key}}}", str(value))
            return result
    
    OpenAIEmbeddings = None
    print("Warning: Using fallback PromptTemplate - LangChain not available")

# Internal imports
try:
    from app.services.pinecone_service import PineconeService, VietnameseLegalDomains
    from app.models.chat_model import BaseChatModel
    from app.utils.text_processing import VietnameseTextProcessor
except ImportError:
    # Fallback for development/testing
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # Mock classes for testing
    class PineconeService:
        pass
    
    class VietnameseLegalDomains:
        @staticmethod
        def get_all_domains():
            return ["dan_su", "hinh_su", "lao_dong", "thuong_mai", "hanh_chinh", "thue", "bat_dong_san", "hien_phap"]
    
    class BaseChatModel:
        pass
    
    class VietnameseTextProcessor:
        def normalize_vietnamese_text(self, text):
            return text
        
        def process_legal_document(self, text):
            return text
    
# Logger setup
logger = logging.getLogger(__name__)

class LegalQueryType(Enum):
    """Types of legal queries supported"""
    GENERAL = "general"
    SPECIFIC_LAW = "specific_law"
    CASE_ANALYSIS = "case_analysis"
    COMPLIANCE = "compliance"
    INTERPRETATION = "interpretation"
    PROCEDURE = "procedure"

class ConfidenceLevel(Enum):
    """Confidence levels for legal responses"""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    UNCERTAIN = "uncertain"

@dataclass
class LegalCitation:
    """Vietnamese legal citation structure"""
    document_type: str  # Luật, Nghị định, Thông tư, etc.
    document_name: str
    article: Optional[str] = None
    clause: Optional[str] = None
    point: Optional[str] = None
    year: Optional[int] = None
    number: Optional[str] = None
    effective_date: Optional[str] = None
    content: Optional[str] = None  # For SerpAPI documents
    law_type: Optional[str] = None  # For categorization
    authority: Optional[str] = None  # Source authority
    source: Optional[str] = None  # URL or source identifier
    confidence: Optional[float] = None  # Confidence score
    
    def __str__(self) -> str:
        """Format citation in Vietnamese legal standard"""
        parts = [self.document_type, self.document_name]
        if self.number:
            parts.append(f"số {self.number}")
        if self.year:
            parts.append(f"năm {self.year}")
        if self.article:
            parts.append(f"Điều {self.article}")
        if self.clause:
            parts.append(f"Khoản {self.clause}")
        if self.point:
            parts.append(f"Điểm {self.point}")
        return " ".join(parts)

@dataclass
class LegalQueryResult:
    """Comprehensive result structure for legal queries"""
    answer: str
    confidence_score: float
    confidence_level: ConfidenceLevel
    sources: List[Dict[str, Any]]
    legal_domain: str
    citations: List[LegalCitation]
    reasoning: str
    query_type: LegalQueryType
    timestamp: datetime = field(default_factory=datetime.now)
    warnings: List[str] = field(default_factory=list)
    related_topics: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "answer": self.answer,
            "confidence_score": self.confidence_score,
            "confidence_level": self.confidence_level.value,
            "sources": self.sources,
            "legal_domain": self.legal_domain,
            "citations": [str(citation) for citation in self.citations],
            "reasoning": self.reasoning,
            "query_type": self.query_type.value,
            "timestamp": self.timestamp.isoformat(),
            "warnings": self.warnings,
            "related_topics": self.related_topics
        }

@dataclass
class DocumentChunk:
    """Enhanced structure for Vietnamese legal document chunks"""
    content: str
    metadata: Dict[str, Any]
    legal_structure: Dict[str, Any] = field(default_factory=dict)
    embedding: Optional[List[float]] = None
    chunk_id: Optional[str] = None
    document_id: Optional[str] = None
    
    def get_legal_level(self) -> str:
        """Get legal hierarchical level (Điều, Khoản, Điểm)"""
        return self.legal_structure.get("level", "unknown")
    
    def get_legal_reference(self) -> str:
        """Get formatted legal reference"""
        structure = self.legal_structure
        if structure.get("article"):
            ref = f"Điều {structure['article']}"
            if structure.get("clause"):
                ref += f", Khoản {structure['clause']}"
            if structure.get("point"):
                ref += f", Điểm {structure['point']}"
            return ref
        return "Tài liệu pháp lý"

class ILegalRAGStrategy(ABC):
    """Strategy interface for different RAG approaches"""
    
    @abstractmethod
    def process_query(self, query: str, context: Dict[str, Any]) -> LegalQueryResult:
        """Process legal query using specific strategy"""
        pass
    
    @abstractmethod
    def get_strategy_name(self) -> str:
        """Get strategy identification"""
        pass

class VietnameseLegalPromptTemplates:
    """Vietnamese legal-specific prompt templates"""
    
    def __init__(self):
        """Initialize prompt templates"""
        logger.info("Initializing VietnameseLegalPromptTemplates...")
        logger.info(f"PromptTemplate class available: {PromptTemplate is not None}")
        
        if PromptTemplate is None:
            # Fallback for testing
            logger.warning("PromptTemplate is None - using fallback")
            self.GENERAL_LEGAL_QA = None
            self.LEGAL_INTERPRETATION = None
            self.COMPLIANCE_CHECK = None
            return
        
        try:
            logger.info("Creating GENERAL_LEGAL_QA template...")
            self.GENERAL_LEGAL_QA = PromptTemplate(
                input_variables=["context", "question"],
                template="""
Bạn là một chuyên gia pháp lý Việt Nam. Hãy trả lời câu hỏi dựa trên TẤT CẢ thông tin pháp lý được cung cấp từ nhiều nguồn khác nhau.

Bối cảnh pháp lý (bao gồm cả tài liệu từ cơ sở dữ liệu và tìm kiếm internet):
{context}

Câu hỏi: {question}

Hướng dẫn trả lời:
1. Trả lời chính xác dựa trên TẤT CẢ văn bản pháp luật được cung cấp
2. Tích hợp thông tin từ cả nguồn cơ sở dữ liệu và tìm kiếm internet
3. Trích dẫn điều, khoản, điểm cụ thể từ các tài liệu
4. Giải thích rõ ràng bằng tiếng Việt
5. Đưa ra cảnh báo nếu cần tư vấn chuyên sâu
6. Nêu rõ phạm vi áp dụng của quy định
7. Đề cập đến nguồn tài liệu (cơ sở dữ liệu hoặc tìm kiếm internet)

Trả lời:
"""
            )
            logger.info("GENERAL_LEGAL_QA template created successfully")
            
            logger.info("Creating LEGAL_INTERPRETATION template...")
            self.LEGAL_INTERPRETATION = PromptTemplate(
                input_variables=["context", "question", "legal_domain"],
                template="""
Với tư cách chuyên gia pháp lý lĩnh vực {legal_domain}, hãy giải thích vấn đề pháp lý sau:

Căn cứ pháp lý:
{context}

Vấn đề cần giải thích: {question}

Yêu cầu:
1. Phân tích điều luật áp dụng
2. Giải thích ý nghĩa và phạm vi
3. Đưa ra ví dụ minh họa (nếu có)
4. Chỉ ra các trường hợp ngoại lệ
5. Tham chiếu văn bản pháp luật liên quan

Giải thích chuyên môn:
"""
            )
            
            logger.info("Creating COMPLIANCE_CHECK template...")
            self.COMPLIANCE_CHECK = PromptTemplate(
                input_variables=["context", "situation", "legal_domain"],
                template="""
Kiểm tra tuân thủ pháp luật Việt Nam cho tình huống sau:

Quy định pháp luật liên quan:
{context}

Tình huống: {situation}
Lĩnh vực: {legal_domain}

Phân tích tuân thủ:
1. Các quy định áp dụng
2. Đánh giá mức độ tuân thủ
3. Rủi ro pháp lý (nếu có)
4. Khuyến nghị hành động
5. Tài liệu cần thiết

Kết luận tuân thủ:
"""
            )
            logger.info("All prompt templates created successfully")
            
        except Exception as e:
            logger.error(f"Failed to create prompt templates: {e}")
            self.GENERAL_LEGAL_QA = None
            self.LEGAL_INTERPRETATION = None
            self.COMPLIANCE_CHECK = None

class VietnameseLegalRAG:
    """Advanced RAG system for Vietnamese legal documents with OOP architecture"""
    
    def __init__(
        self,
        pinecone_service: PineconeService,
        chat_model: Any,
        embedding_model: Optional[OpenAIEmbeddings] = None,
        text_processor: Optional[Any] = None,
        embedding_api_key: Optional[str] = None,
        embedding_api_base: Optional[str] = None,
        serp_service: Optional[Any] = None
    ):
        """Initialize Vietnamese Legal RAG system with full OOP design"""
        self.pinecone_service = pinecone_service
        self.chat_model = chat_model
        self.serp_service = serp_service  # Add SerpAPI service
        
        # Initialize embedding model with separate API configuration
        if embedding_model:
            self.embedding_model = embedding_model
        elif OpenAIEmbeddings:
            # Use separate API key for embeddings if provided
            embedding_kwargs = {}
            if embedding_api_key:
                embedding_kwargs['openai_api_key'] = embedding_api_key
            if embedding_api_base:
                embedding_kwargs['openai_api_base'] = embedding_api_base
            
            try:
                # Use text-embedding-3-small (compatible with API key)
                self.embedding_model = OpenAIEmbeddings(
                    model="text-embedding-3-small",
                    **embedding_kwargs
                )
                logger.info("Successfully initialized text-embedding-3-small")
            except Exception as e:
                logger.error(f"Failed to initialize embedding model: {e}")
                self.embedding_model = None
        else:
            self.embedding_model = None
            
        self.text_processor = text_processor or VietnameseTextProcessor()
        
        # Initialize components
        self.prompt_templates = VietnameseLegalPromptTemplates()
        self.citation_extractor = LegalCitationExtractor()
        self.validator = VietnameseLegalValidator()
        self.legal_domains = VietnameseLegalDomains()
        
        # Strategy pattern implementation
        self._strategies: Dict[LegalQueryType, ILegalRAGStrategy] = {}
        self._init_strategies()
        
        # Performance tracking
        self.query_history: List[LegalQueryResult] = []
        self.performance_metrics = {
            "total_queries": 0,
            "avg_confidence": 0.0,
            "domain_distribution": {}
        }
        
        logger.info("VietnameseLegalRAG initialized successfully")
    
    def _init_strategies(self):
        """Initialize RAG strategies for different query types"""
        self._strategies = {
            LegalQueryType.GENERAL: GeneralLegalRAGStrategy(self),
            LegalQueryType.SPECIFIC_LAW: SpecificLawRAGStrategy(self),
            LegalQueryType.CASE_ANALYSIS: CaseAnalysisRAGStrategy(self),
            LegalQueryType.COMPLIANCE: ComplianceRAGStrategy(self),
            LegalQueryType.INTERPRETATION: InterpretationRAGStrategy(self),
            LegalQueryType.PROCEDURE: ProcedureRAGStrategy(self)
        }
    
    def query(
        self,
        question: str,
        legal_domain: Optional[str] = None,
        query_type: Optional[LegalQueryType] = None,
        max_results: int = 5,
        confidence_threshold: float = 0.7,
        include_related: bool = True
    ) -> LegalQueryResult:
        """
        Process comprehensive legal query with enhanced Vietnamese support
        
        Args:
            question: Vietnamese legal question
            legal_domain: Specific legal domain to focus on
            query_type: Type of legal query for strategy selection
            max_results: Maximum documents to retrieve
            confidence_threshold: Minimum confidence for results
            include_related: Include related topics in response
            
        Returns:
            LegalQueryResult: Comprehensive structured result
        """
        try:
            # Step 1: Preprocess and analyze query
            processed_query = self._preprocess_vietnamese_query(question)
            detected_domain = legal_domain or self._detect_legal_domain(question)
            detected_query_type = query_type or self._classify_query_type(question)
            
            logger.info(f"Processing query - Domain: {detected_domain}, Type: {detected_query_type}")
            
            # Step 2: Retrieve relevant documents using advanced search
            relevant_docs = self._retrieve_documents(
                processed_query,
                detected_domain,
                max_results,
                confidence_threshold
            )
            
            # Step 3: Select and execute appropriate strategy
            strategy = self._strategies.get(detected_query_type, self._strategies[LegalQueryType.GENERAL])
            
            context = {
                "original_query": question,
                "processed_query": processed_query,
                "documents": relevant_docs,
                "legal_domain": detected_domain,
                "query_type": detected_query_type
            }
            
            result = strategy.process_query(processed_query, context)
            
            # Step 4: Post-process and enhance result
            if include_related:
                result.related_topics = self._find_related_topics(question, detected_domain)
            
            # Step 5: Validate and add warnings
            validation_result = self.validator.validate_response(result.answer, relevant_docs)
            result.warnings.extend(validation_result.get("warnings", []))
            
            # Step 6: Update performance metrics
            self._update_metrics(result)
            self.query_history.append(result)
            
            logger.info(f"Query processed successfully - Confidence: {result.confidence_score}")
            return result
            
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            return self._create_error_result(question, str(e))
    
    def _preprocess_vietnamese_query(self, query: str) -> str:
        """Advanced Vietnamese legal query preprocessing"""
        try:
            # Normalize Vietnamese text
            normalized = self.text_processor.normalize_vietnamese_text(query)
            
            # Extract and expand legal terms
            legal_terms = self._extract_legal_terms(normalized)
            expanded_query = self._expand_legal_abbreviations(normalized)
            
            # Add context keywords based on detected intent
            context_keywords = self._add_context_keywords(expanded_query)
            
            return context_keywords
            
        except Exception as e:
            logger.warning(f"Query preprocessing failed: {e}")
            return query
    
    def _retrieve_documents(
        self,
        query: str,
        legal_domain: str,
        max_results: int,
        confidence_threshold: float
    ) -> List[Dict[str, Any]]:
        """Retrieve relevant documents with advanced filtering and ranking"""
        try:
            # Generate query embedding (handle missing embedding model)
            if self.embedding_model:
                query_embedding = self.embedding_model.embed_query(query)
            else:
                query_embedding = None
            
            # Prepare metadata filters
            metadata_filter = {
                "legal_domain": legal_domain,
                "language": "vietnamese"
            }
            
            # Search with multiple strategies
            results = []
            
            # Primary search: Exact domain match
            primary_results = self.pinecone_service.similarity_search(
                query_text=query,
                k=max_results,
                metadata_filter=metadata_filter
            )
            results.extend(primary_results)
            
            # Secondary search: Related domains if insufficient results
            if len(results) < max_results // 2:
                related_domains = self._get_related_domains(legal_domain)
                for domain in related_domains:
                    metadata_filter["legal_domain"] = domain
                    secondary_results = self.pinecone_service.similarity_search(
                        query_text=query,
                        k=max_results - len(results),
                        metadata_filter=metadata_filter
                    )
                    results.extend(secondary_results)
            
            # Filter by confidence and rank
            filtered_results = [
                doc for doc in results 
                if doc.get("score", 0) >= confidence_threshold
            ]
            
            # Sort by relevance score
            filtered_results.sort(key=lambda x: x.get("score", 0), reverse=True)
            
            # If vector search has insufficient results, use SerpAPI as fallback
            if len(filtered_results) < max_results // 2 and self.serp_service:
                logger.info(f"Vector search returned only {len(filtered_results)} results, using SerpAPI fallback")
                
                try:
                    # Search with SerpAPI for additional results
                    serp_results = self.serp_service.search_legal_documents(
                        question=query, 
                        max_results=max_results - len(filtered_results)
                    )
                    
                    # Convert SerpAPI results to compatible format
                    for serp_doc in serp_results:
                        formatted_doc = {
                            "page_content": serp_doc.get("content", ""),
                            "metadata": {
                                "document_name": serp_doc.get("title", ""),
                                "legal_reference": serp_doc.get("article", ""),
                                "source": serp_doc.get("source", ""),
                                "authority": serp_doc.get("authority", "SerpAPI"),
                                "legal_domain": legal_domain,
                                "search_type": "serp_api"
                            },
                            "score": serp_doc.get("relevance_score", 0.8),
                            "search_type": "serp_api"
                        }
                        filtered_results.append(formatted_doc)
                    
                    logger.info(f"Added {len(serp_results)} documents from SerpAPI search")
                    
                except Exception as serp_error:
                    logger.error(f"SerpAPI fallback search failed: {serp_error}")
            
            return filtered_results[:max_results]
            
        except Exception as e:
            logger.error(f"Document retrieval failed: {e}")
            return []
    
    def _generate_contextual_response(
        self,
        query: str,
        context_docs: List[Dict[str, Any]],
        legal_domain: str,
        query_type: LegalQueryType
    ) -> Tuple[str, str, float]:
        """Generate contextual response with reasoning and confidence"""
        try:
            # Build context from retrieved documents
            context = self._build_document_context(context_docs)
            logger.info(f"Built context from {len(context_docs)} documents, context length: {len(context)}")
            
            # Select appropriate prompt template
            template = self._select_prompt_template(query_type, legal_domain)
            
            # Generate response using LLM
            prompt = template.format(
                context=context,
                question=query,
                legal_domain=legal_domain
            )
            
            response = self.chat_model.generate_response(prompt)
            
            # Extract reasoning and calculate confidence
            reasoning = self._extract_reasoning(response, context_docs)
            confidence = self._calculate_confidence(response, context_docs)
            
            return response, reasoning, confidence
            
        except Exception as e:
            logger.error(f"Response generation failed: {e}")
            return "Xin lỗi, tôi không thể xử lý câu hỏi này hiện tại.", "Lỗi hệ thống", 0.0
    
    def _build_document_context(self, documents: List[Dict[str, Any]]) -> str:
        """Build structured context from retrieved documents"""
        if not documents:
            return "Không tìm thấy tài liệu pháp lý liên quan."
        
        logger.info(f"Building context from {len(documents)} documents")
        context_parts = []
        
        for i, doc in enumerate(documents, 1):
            content = doc.get("page_content", "")
            metadata = doc.get("metadata", {})
            search_type = doc.get("search_type", "vector")
            
            logger.info(f"Document {i}: type={search_type}, content_length={len(content)}, title={metadata.get('document_name', 'N/A')}")
            
            # Format document with legal structure
            doc_section = f"--- Tài liệu {i} "
            if search_type == "serp_api":
                doc_section += "(Nguồn: Tìm kiếm internet) ---\n"
            else:
                doc_section += "(Nguồn: Cơ sở dữ liệu) ---\n"
                
            if metadata.get("document_name"):
                doc_section += f"Tiêu đề: {metadata['document_name']}\n"
            if metadata.get("legal_reference"):
                doc_section += f"Tham chiếu: {metadata['legal_reference']}\n"
            if metadata.get("source"):
                doc_section += f"Link: {metadata['source']}\n"
            doc_section += f"Nội dung:\n{content}\n"
            
            context_parts.append(doc_section)
        
        built_context = "\n".join(context_parts)
        logger.info(f"Final context length: {len(built_context)}")
        return built_context
    
    def _select_prompt_template(self, query_type: LegalQueryType, legal_domain: str):
        """Select appropriate prompt template based on query type"""
        logger.info(f"Selecting template for query_type: {query_type}")
        logger.info(f"GENERAL_LEGAL_QA available: {self.prompt_templates.GENERAL_LEGAL_QA is not None}")
        
        if self.prompt_templates.GENERAL_LEGAL_QA is None:
            # Return mock template for testing
            logger.warning("Using MockTemplate because GENERAL_LEGAL_QA is None")
            class MockTemplate:
                def format(self, **kwargs):
                    context = kwargs.get('context', 'No context')
                    question = kwargs.get('question', 'No question')
                    return f"""Bạn là chuyên gia pháp lý Việt Nam. Trả lời câu hỏi dựa trên thông tin sau:

{context}

Câu hỏi: {question}

Trả lời chi tiết:"""
            return MockTemplate()
            
        template_map = {
            LegalQueryType.GENERAL: self.prompt_templates.GENERAL_LEGAL_QA,
            LegalQueryType.INTERPRETATION: self.prompt_templates.LEGAL_INTERPRETATION,
            LegalQueryType.COMPLIANCE: self.prompt_templates.COMPLIANCE_CHECK,
            LegalQueryType.SPECIFIC_LAW: self.prompt_templates.GENERAL_LEGAL_QA,
            LegalQueryType.CASE_ANALYSIS: self.prompt_templates.LEGAL_INTERPRETATION,
            LegalQueryType.PROCEDURE: self.prompt_templates.GENERAL_LEGAL_QA
        }
        selected_template = template_map.get(query_type, self.prompt_templates.GENERAL_LEGAL_QA)
        logger.info(f"Selected template: {type(selected_template).__name__}")
        return selected_template
    
    def _extract_reasoning(self, response: str, context_docs: List[Dict[str, Any]]) -> str:
        """Extract and format reasoning from response"""
        # Simple reasoning extraction - can be enhanced with NLP
        reasoning_markers = ["căn cứ", "dựa trên", "theo quy định", "điều luật"]
        
        sentences = response.split(". ")
        reasoning_sentences = []
        
        for sentence in sentences:
            if any(marker in sentence.lower() for marker in reasoning_markers):
                reasoning_sentences.append(sentence.strip())
        
        if reasoning_sentences:
            return ". ".join(reasoning_sentences)
        else:
            return f"Dựa trên {len(context_docs)} tài liệu pháp lý liên quan"
    
    def _calculate_confidence(
        self,
        response: str,
        source_docs: List[Dict[str, Any]]
    ) -> float:
        """Calculate comprehensive confidence score"""
        if not source_docs:
            return 0.1
        
        # Factor 1: Document relevance scores
        doc_scores = [doc.get("score", 0.5) for doc in source_docs]
        avg_doc_score = sum(doc_scores) / len(doc_scores) if doc_scores else 0.5
        
        # Factor 2: Number of sources
        source_factor = min(len(source_docs) / 3, 1.0)  # Optimal around 3 sources
        
        # Factor 3: Response completeness (based on length and structure)
        response_factor = min(len(response) / 500, 1.0)  # Reasonable response length
        
        # Factor 4: Citation presence
        citation_factor = 0.8 if self._has_legal_citations(response) else 0.6
        
        # Weighted combination
        confidence = (
            avg_doc_score * 0.4 +
            source_factor * 0.2 +
            response_factor * 0.2 +
            citation_factor * 0.2
        )
        
        return round(min(confidence, 1.0), 2)
    
    def _has_legal_citations(self, text: str) -> bool:
        """Check if text contains Vietnamese legal citations"""
        citation_patterns = [
            r"điều\s+\d+",
            r"khoản\s+\d+",
            r"điểm\s+[a-z]",
            r"luật\s+\w+",
            r"nghị định\s+\d+"
        ]
        
        text_lower = text.lower()
        return any(re.search(pattern, text_lower) for pattern in citation_patterns)
    
    def _extract_legal_terms(self, text: str) -> List[str]:
        """Extract Vietnamese legal terminology"""
        legal_terms = [
            "điều luật", "quy định", "nghị định", "thông tư", "quyết định",
            "bộ luật", "hiến pháp", "pháp luật", "văn bản pháp luật",
            "trách nhiệm", "quyền lợi", "nghĩa vụ", "xử phạt", "vi phạm"
        ]
        
        found_terms = []
        text_lower = text.lower()
        
        for term in legal_terms:
            if term in text_lower:
                found_terms.append(term)
        
        return found_terms
    
    def _expand_legal_abbreviations(self, text: str) -> str:
        """Expand Vietnamese legal abbreviations"""
        abbreviations = {
            "bldđ": "bộ luật lao động",
            "blhs": "bộ luật hình sự",
            "blds": "bộ luật dân sự",
            "hp": "hiến pháp",
            "nd": "nghị định",
            "tt": "thông tư",
            "qđ": "quyết định"
        }
        
        expanded_text = text.lower()
        for abbr, full_form in abbreviations.items():
            expanded_text = expanded_text.replace(abbr, full_form)
        
        return expanded_text
    
    def _add_context_keywords(self, query: str) -> str:
        """Add contextual keywords to enhance search"""
        # Detect query intent and add relevant keywords
        intent_keywords = {
            "quyền": ["quyền lợi", "nghĩa vụ", "bảo vệ"],
            "trách nhiệm": ["nghĩa vụ", "vi phạm", "xử phạt"],
            "thủ tục": ["quy trình", "hồ sơ", "điều kiện"],
            "hợp đồng": ["thỏa thuận", "cam kết", "nghĩa vụ"],
            "tranh chấp": ["giải quyết", "tòa án", "trọng tài"]
        }
        
        enhanced_query = query
        for keyword, related in intent_keywords.items():
            if keyword in query.lower():
                enhanced_query += " " + " ".join(related)
        
        return enhanced_query
    
    def _detect_legal_domain(self, query: str) -> str:
        """Detect legal domain from query content"""
        domain_keywords = {
            "dan_su": ["hợp đồng", "tài sản", "thừa kế", "kết hôn", "ly hôn"],
            "hinh_su": ["tội phạm", "án phạt", "tù giam", "vi phạm hình sự"],
            "lao_dong": ["lương", "bảo hiểm", "nghỉ việc", "sa thải", "hợp đồng lao động"],
            "thuong_mai": ["kinh doanh", "doanh nghiệp", "thương mại", "đầu tư"],
            "hanh_chinh": ["thủ tục", "giấy phép", "hành chính", "cơ quan nhà nước"],
            "thue": ["thuế", "khai thuế", "miễn thuế", "nộp thuế"],
            "bat_dong_san": ["nhà đất", "bất động sản", "quyền sử dụng đất"],
            "hien_phap": ["hiến pháp", "quyền công dân", "nghĩa vụ công dân"]
        }
        
        query_lower = query.lower()
        domain_scores = {}
        
        for domain, keywords in domain_keywords.items():
            score = sum(1 for keyword in keywords if keyword in query_lower)
            if score > 0:
                domain_scores[domain] = score
        
        if domain_scores:
            return max(domain_scores, key=domain_scores.get)
        else:
            return "general"
    
    def _classify_query_type(self, query: str) -> LegalQueryType:
        """Classify query type for strategy selection"""
        query_lower = query.lower()
        
        # Pattern-based classification
        if any(word in query_lower for word in ["là gì", "định nghĩa", "khái niệm"]):
            return LegalQueryType.INTERPRETATION
        elif any(word in query_lower for word in ["thủ tục", "quy trình", "làm thế nào"]):
            return LegalQueryType.PROCEDURE
        elif any(word in query_lower for word in ["vi phạm", "tuân thủ", "có được phép"]):
            return LegalQueryType.COMPLIANCE
        elif any(word in query_lower for word in ["điều", "luật", "quy định cụ thể"]):
            return LegalQueryType.SPECIFIC_LAW
        elif any(word in query_lower for word in ["trường hợp", "tình huống", "phân tích"]):
            return LegalQueryType.CASE_ANALYSIS
        else:
            return LegalQueryType.GENERAL
    
    def _get_related_domains(self, domain: str) -> List[str]:
        """Get related legal domains for enhanced search"""
        domain_relationships = {
            "dan_su": ["thuong_mai", "bat_dong_san"],
            "lao_dong": ["thue", "hanh_chinh"],
            "thuong_mai": ["dan_su", "thue"],
            "hinh_su": ["hanh_chinh"],
            "thue": ["thuong_mai", "lao_dong"],
            "bat_dong_san": ["dan_su", "thue"],
            "hanh_chinh": ["thue", "hinh_su"],
            "hien_phap": ["dan_su", "hinh_su"]
        }
        return domain_relationships.get(domain, [])
    
    def _find_related_topics(self, query: str, domain: str) -> List[str]:
        """Find related legal topics for enhanced user experience"""
        # This would typically use a more sophisticated NLP approach
        related_topics = []
        
        # Domain-based related topics
        domain_topics = {
            "dan_su": ["Quyền tài sản", "Hợp đồng", "Thừa kế", "Hôn nhân gia đình"],
            "lao_dong": ["Hợp đồng lao động", "Bảo hiểm xã hội", "An toàn lao động"],
            "thuong_mai": ["Đăng ký kinh doanh", "Thuế doanh nghiệp", "Hợp đồng thương mại"],
            "hinh_su": ["Các tội phạm", "Hình phạt", "Tố tụng hình sự"]
        }
        
        related_topics.extend(domain_topics.get(domain, []))
        
        # Query-based related topics
        if "hợp đồng" in query.lower():
            related_topics.extend(["Điều kiện hợp đồng", "Chấm dứt hợp đồng", "Tranh chấp hợp đồng"])
        
        return list(set(related_topics))  # Remove duplicates
    
    def _update_metrics(self, result: LegalQueryResult):
        """Update performance metrics"""
        self.performance_metrics["total_queries"] += 1
        
        # Update average confidence
        total_confidence = self.performance_metrics["avg_confidence"] * (self.performance_metrics["total_queries"] - 1)
        self.performance_metrics["avg_confidence"] = (total_confidence + result.confidence_score) / self.performance_metrics["total_queries"]
        
        # Update domain distribution
        domain = result.legal_domain
        if domain in self.performance_metrics["domain_distribution"]:
            self.performance_metrics["domain_distribution"][domain] += 1
        else:
            self.performance_metrics["domain_distribution"][domain] = 1
    
    def _create_error_result(self, query: str, error: str) -> LegalQueryResult:
        """Create error result for failed queries"""
        return LegalQueryResult(
            answer="Xin lỗi, đã có lỗi xảy ra khi xử lý câu hỏi của bạn. Vui lòng thử lại sau.",
            confidence_score=0.0,
            confidence_level=ConfidenceLevel.UNCERTAIN,
            sources=[],
            legal_domain="unknown",
            citations=[],
            reasoning=f"Lỗi hệ thống: {error}",
            query_type=LegalQueryType.GENERAL,
            warnings=[f"Lỗi xử lý: {error}"]
        )
    
    def add_legal_documents(self, documents: List[DocumentChunk]) -> bool:
        """Add new legal documents to the knowledge base"""
        try:
            processed_docs = []
            
            for doc in documents:
                # Process document content
                processed_content = self.text_processor.process_legal_document(doc.content)
                
                # Extract legal structure
                legal_structure = self._extract_legal_structure(processed_content)
                doc.legal_structure = legal_structure
                
                # Generate embedding (handle missing embedding model)
                if not doc.embedding and self.embedding_model:
                    doc.embedding = self.embedding_model.embed_documents([processed_content])[0]
                
                processed_docs.append(doc)
            
            # Store in Pinecone
            success = self.pinecone_service.upsert_documents(processed_docs)
            
            if success:
                logger.info(f"Successfully added {len(documents)} legal documents")
                return True
            else:
                logger.error("Failed to store documents in Pinecone")
                return False
                
        except Exception as e:
            logger.error(f"Error adding documents: {e}")
            return False
    
    def _extract_legal_structure(self, content: str) -> Dict[str, Any]:
        """Extract Vietnamese legal document structure"""
        structure = {}
        
        # Extract article numbers (Điều)
        article_match = re.search(r'điều\s+(\d+)', content.lower())
        if article_match:
            structure["article"] = article_match.group(1)
        
        # Extract clauses (Khoản)
        clause_match = re.search(r'khoản\s+(\d+)', content.lower())
        if clause_match:
            structure["clause"] = clause_match.group(1)
        
        # Extract points (Điểm)
        point_match = re.search(r'điểm\s+([a-z])', content.lower())
        if point_match:
            structure["point"] = point_match.group(1)
        
        # Determine legal level
        if "điểm" in structure:
            structure["level"] = "point"
        elif "khoản" in structure:
            structure["level"] = "clause"
        elif "điều" in structure:
            structure["level"] = "article"
        else:
            structure["level"] = "document"
        
        return structure
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get system performance metrics"""
        return {
            "metrics": self.performance_metrics,
            "recent_queries": len(self.query_history),
            "last_query_time": self.query_history[-1].timestamp.isoformat() if self.query_history else None
        }
    
    def clear_history(self):
        """Clear query history and reset metrics"""
        self.query_history.clear()
        self.performance_metrics = {
            "total_queries": 0,
            "avg_confidence": 0.0,
            "domain_distribution": {}
        }

# ============================================================================
# Strategy Pattern Implementation for Different RAG Approaches
# ============================================================================

class GeneralLegalRAGStrategy(ILegalRAGStrategy):
    """Strategy for general legal questions"""
    
    def __init__(self, rag_system: VietnameseLegalRAG):
        self.rag_system = rag_system
    
    def process_query(self, query: str, context: Dict[str, Any]) -> LegalQueryResult:
        """Process general legal query"""
        documents = context["documents"]
        legal_domain = context["legal_domain"]
        
        # Generate response using general template
        response, reasoning, confidence = self.rag_system._generate_contextual_response(
            query, documents, legal_domain, LegalQueryType.GENERAL
        )
        
        # Extract citations
        citations = self.rag_system.citation_extractor.extract_citations_from_documents(documents)
        
        # Determine confidence level
        confidence_level = self._get_confidence_level(confidence)
        
        return LegalQueryResult(
            answer=response,
            confidence_score=confidence,
            confidence_level=confidence_level,
            sources=documents,
            legal_domain=legal_domain,
            citations=citations,
            reasoning=reasoning,
            query_type=LegalQueryType.GENERAL
        )
    
    def get_strategy_name(self) -> str:
        return "GeneralLegalRAG"
    
    def _get_confidence_level(self, score: float) -> ConfidenceLevel:
        """Convert numeric confidence to level"""
        if score >= 0.8:
            return ConfidenceLevel.HIGH
        elif score >= 0.6:
            return ConfidenceLevel.MEDIUM
        elif score >= 0.4:
            return ConfidenceLevel.LOW
        else:
            return ConfidenceLevel.UNCERTAIN

class SpecificLawRAGStrategy(ILegalRAGStrategy):
    """Strategy for specific law and regulation queries"""
    
    def __init__(self, rag_system: VietnameseLegalRAG):
        self.rag_system = rag_system
    
    def process_query(self, query: str, context: Dict[str, Any]) -> LegalQueryResult:
        """Process specific law query with enhanced citation extraction"""
        documents = context["documents"]
        legal_domain = context["legal_domain"]
        
        # Enhanced document filtering for specific laws
        specific_docs = self._filter_specific_documents(documents, query)
        
        response, reasoning, confidence = self.rag_system._generate_contextual_response(
            query, specific_docs, legal_domain, LegalQueryType.SPECIFIC_LAW
        )
        
        # Enhanced citation extraction for specific laws
        citations = self.rag_system.citation_extractor.extract_detailed_citations(specific_docs, query)
        
        return LegalQueryResult(
            answer=response,
            confidence_score=confidence,
            confidence_level=self._get_confidence_level(confidence),
            sources=specific_docs,
            legal_domain=legal_domain,
            citations=citations,
            reasoning=reasoning,
            query_type=LegalQueryType.SPECIFIC_LAW
        )
    
    def _filter_specific_documents(self, documents: List[Dict], query: str) -> List[Dict]:
        """Filter documents for specific legal references"""
        # Look for specific law names, article numbers in query
        law_terms = ["luật", "bộ luật", "nghị định", "thông tư", "điều"]
        query_lower = query.lower()
        
        if any(term in query_lower for term in law_terms):
            # Prioritize documents with matching law references
            specific_docs = []
            for doc in documents:
                content = doc.get("page_content", "").lower()
                metadata = doc.get("metadata", {})
                
                # Check if document contains specific legal references
                if any(term in content for term in law_terms):
                    specific_docs.append(doc)
            
            return specific_docs if specific_docs else documents
        
        return documents
    
    def get_strategy_name(self) -> str:
        return "SpecificLawRAG"
    
    def _get_confidence_level(self, score: float) -> ConfidenceLevel:
        # Higher threshold for specific law queries
        if score >= 0.85:
            return ConfidenceLevel.HIGH
        elif score >= 0.7:
            return ConfidenceLevel.MEDIUM
        elif score >= 0.5:
            return ConfidenceLevel.LOW
        else:
            return ConfidenceLevel.UNCERTAIN

class CaseAnalysisRAGStrategy(ILegalRAGStrategy):
    """Strategy for legal case analysis queries"""
    
    def __init__(self, rag_system: VietnameseLegalRAG):
        self.rag_system = rag_system
    
    def process_query(self, query: str, context: Dict[str, Any]) -> LegalQueryResult:
        """Process case analysis with multi-perspective approach"""
        documents = context["documents"]
        legal_domain = context["legal_domain"]
        
        # Analyze case from multiple legal perspectives
        analysis_results = self._multi_perspective_analysis(query, documents, legal_domain)
        
        return LegalQueryResult(
            answer=analysis_results["answer"],
            confidence_score=analysis_results["confidence"],
            confidence_level=self._get_confidence_level(analysis_results["confidence"]),
            sources=documents,
            legal_domain=legal_domain,
            citations=analysis_results["citations"],
            reasoning=analysis_results["reasoning"],
            query_type=LegalQueryType.CASE_ANALYSIS,
            warnings=analysis_results.get("warnings", [])
        )
    
    def _multi_perspective_analysis(self, query: str, documents: List[Dict], domain: str) -> Dict[str, Any]:
        """Analyze case from multiple legal perspectives"""
        # This would implement sophisticated case analysis
        # For now, using enhanced general approach
        response, reasoning, confidence = self.rag_system._generate_contextual_response(
            query, documents, domain, LegalQueryType.CASE_ANALYSIS
        )
        
        citations = self.rag_system.citation_extractor.extract_citations_from_documents(documents)
        
        # Add case analysis specific warnings
        warnings = []
        if confidence < 0.7:
            warnings.append("Phân tích này cần được xem xét bởi chuyên gia pháp lý")
        
        return {
            "answer": response,
            "confidence": confidence,
            "reasoning": reasoning,
            "citations": citations,
            "warnings": warnings
        }
    
    def get_strategy_name(self) -> str:
        return "CaseAnalysisRAG"
    
    def _get_confidence_level(self, score: float) -> ConfidenceLevel:
        # More conservative confidence for case analysis
        if score >= 0.9:
            return ConfidenceLevel.HIGH
        elif score >= 0.75:
            return ConfidenceLevel.MEDIUM
        elif score >= 0.6:
            return ConfidenceLevel.LOW
        else:
            return ConfidenceLevel.UNCERTAIN

class ComplianceRAGStrategy(ILegalRAGStrategy):
    """Strategy for compliance and regulatory queries"""
    
    def __init__(self, rag_system: VietnameseLegalRAG):
        self.rag_system = rag_system
    
    def process_query(self, query: str, context: Dict[str, Any]) -> LegalQueryResult:
        """Process compliance query with risk assessment"""
        documents = context["documents"]
        legal_domain = context["legal_domain"]
        
        # Generate compliance-focused response
        response, reasoning, confidence = self.rag_system._generate_contextual_response(
            query, documents, legal_domain, LegalQueryType.COMPLIANCE
        )
        
        # Add compliance-specific analysis
        compliance_analysis = self._analyze_compliance_risk(query, documents)
        
        citations = self.rag_system.citation_extractor.extract_citations_from_documents(documents)
        
        return LegalQueryResult(
            answer=response + "\n\n" + compliance_analysis["summary"],
            confidence_score=confidence,
            confidence_level=self._get_confidence_level(confidence),
            sources=documents,
            legal_domain=legal_domain,
            citations=citations,
            reasoning=reasoning,
            query_type=LegalQueryType.COMPLIANCE,
            warnings=compliance_analysis["warnings"]
        )
    
    def _analyze_compliance_risk(self, query: str, documents: List[Dict]) -> Dict[str, Any]:
        """Analyze compliance risk factors"""
        warnings = []
        risk_indicators = ["vi phạm", "xử phạt", "cấm", "không được"]
        
        query_lower = query.lower()
        high_risk = any(indicator in query_lower for indicator in risk_indicators)
        
        if high_risk:
            warnings.append("Cần tham khảo ý kiến chuyên gia pháp lý trước khi hành động")
        
        summary = "Phân tích tuân thủ: " + ("Có yếu tố rủi ro cao" if high_risk else "Rủi ro thấp")
        
        return {
            "summary": summary,
            "warnings": warnings,
            "risk_level": "high" if high_risk else "low"
        }
    
    def get_strategy_name(self) -> str:
        return "ComplianceRAG"
    
    def _get_confidence_level(self, score: float) -> ConfidenceLevel:
        # Conservative approach for compliance
        if score >= 0.85:
            return ConfidenceLevel.HIGH
        elif score >= 0.7:
            return ConfidenceLevel.MEDIUM
        else:
            return ConfidenceLevel.LOW

class InterpretationRAGStrategy(ILegalRAGStrategy):
    """Strategy for legal interpretation and definition queries"""
    
    def __init__(self, rag_system: VietnameseLegalRAG):
        self.rag_system = rag_system
    
    def process_query(self, query: str, context: Dict[str, Any]) -> LegalQueryResult:
        """Process interpretation query with detailed explanation"""
        documents = context["documents"]
        legal_domain = context["legal_domain"]
        
        response, reasoning, confidence = self.rag_system._generate_contextual_response(
            query, documents, legal_domain, LegalQueryType.INTERPRETATION
        )
        
        # Add interpretation-specific enhancements
        enhanced_response = self._enhance_interpretation(response, documents)
        
        citations = self.rag_system.citation_extractor.extract_citations_from_documents(documents)
        
        return LegalQueryResult(
            answer=enhanced_response,
            confidence_score=confidence,
            confidence_level=self._get_confidence_level(confidence),
            sources=documents,
            legal_domain=legal_domain,
            citations=citations,
            reasoning=reasoning,
            query_type=LegalQueryType.INTERPRETATION
        )
    
    def _enhance_interpretation(self, response: str, documents: List[Dict]) -> str:
        """Enhance interpretation with examples and context"""
        # Add structured interpretation format
        enhanced = response
        
        if len(documents) > 1:
            enhanced += "\n\nTham khảo thêm từ các văn bản pháp luật liên quan:"
            for i, doc in enumerate(documents[:3], 1):
                metadata = doc.get("metadata", {})
                if metadata.get("document_name"):
                    enhanced += f"\n{i}. {metadata['document_name']}"
        
        return enhanced
    
    def get_strategy_name(self) -> str:
        return "InterpretationRAG"
    
    def _get_confidence_level(self, score: float) -> ConfidenceLevel:
        if score >= 0.8:
            return ConfidenceLevel.HIGH
        elif score >= 0.65:
            return ConfidenceLevel.MEDIUM
        elif score >= 0.45:
            return ConfidenceLevel.LOW
        else:
            return ConfidenceLevel.UNCERTAIN

class ProcedureRAGStrategy(ILegalRAGStrategy):
    """Strategy for legal procedure and process queries"""
    
    def __init__(self, rag_system: VietnameseLegalRAG):
        self.rag_system = rag_system
    
    def process_query(self, query: str, context: Dict[str, Any]) -> LegalQueryResult:
        """Process procedure query with step-by-step guidance"""
        documents = context["documents"]
        legal_domain = context["legal_domain"]
        
        response, reasoning, confidence = self.rag_system._generate_contextual_response(
            query, documents, legal_domain, LegalQueryType.PROCEDURE
        )
        
        # Structure response as step-by-step procedure
        structured_response = self._structure_procedure_response(response, documents)
        
        citations = self.rag_system.citation_extractor.extract_citations_from_documents(documents)
        
        return LegalQueryResult(
            answer=structured_response,
            confidence_score=confidence,
            confidence_level=self._get_confidence_level(confidence),
            sources=documents,
            legal_domain=legal_domain,
            citations=citations,
            reasoning=reasoning,
            query_type=LegalQueryType.PROCEDURE
        )
    
    def _structure_procedure_response(self, response: str, documents: List[Dict]) -> str:
        """Structure response as clear procedural steps"""
        # Simple structuring - can be enhanced with NLP
        sentences = response.split(". ")
        structured = []
        
        step_indicators = ["đầu tiên", "sau đó", "tiếp theo", "cuối cùng", "bước"]
        
        for i, sentence in enumerate(sentences):
            sentence = sentence.strip()
            if sentence:
                if any(indicator in sentence.lower() for indicator in step_indicators):
                    structured.append(f"🔸 {sentence}")
                else:
                    structured.append(sentence)
        
        base_response = ". ".join(structured)
        
        # Add source information if we have SerpAPI results
        serp_docs = [doc for doc in documents if doc.get("search_type") == "serp_api"]
        vector_docs = [doc for doc in documents if doc.get("search_type") != "serp_api"]
        
        if serp_docs:
            base_response += "\n\n📚 **Nguồn tham khảo bổ sung từ internet:**\n"
            for i, doc in enumerate(serp_docs, 1):
                metadata = doc.get("metadata", {})
                base_response += f"{i}. {metadata.get('document_name', 'Tài liệu pháp lý')}\n"
                if metadata.get('source'):
                    base_response += f"   🔗 {metadata['source']}\n"
        
        if len(documents) > 0:
            base_response += f"\n📊 **Thông tin nguồn:** {len(vector_docs)} tài liệu từ cơ sở dữ liệu, {len(serp_docs)} tài liệu từ tìm kiếm internet"
        
        return base_response
    
    def get_strategy_name(self) -> str:
        return "ProcedureRAG"
    
    def _get_confidence_level(self, score: float) -> ConfidenceLevel:
        if score >= 0.8:
            return ConfidenceLevel.HIGH
        elif score >= 0.6:
            return ConfidenceLevel.MEDIUM
        elif score >= 0.4:
            return ConfidenceLevel.LOW
        else:
            return ConfidenceLevel.UNCERTAIN

# ============================================================================
# Specialized Citation and Validation Classes
# ============================================================================

class LegalCitationExtractor:
    """Advanced Vietnamese legal citation extraction with OOP design"""
    
    def __init__(self):
        """Initialize citation extractor with Vietnamese legal patterns"""
        self.citation_patterns = self._init_citation_patterns()
        self.legal_document_types = [
            "Hiến pháp", "Luật", "Bộ luật", "Nghị định", 
            "Thông tư", "Quyết định", "Chỉ thị", "Công văn"
        ]
        
        logger.info("LegalCitationExtractor initialized")
    
    def _init_citation_patterns(self) -> Dict[str, str]:
        """Initialize regex patterns for Vietnamese legal citations"""
        return {
            "article": r'điều\s+(\d+)',
            "clause": r'khoản\s+(\d+)',
            "point": r'điểm\s+([a-z])',
            "law_with_number": r'(luật|bộ luật)\s+([^,.\n]+?)\s+số\s+(\d+[/\d\w\-]+)',
            "law_simple": r'(luật|bộ luật)\s+([a-záàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵđ\s]+)',
            "decree": r'nghị định\s+số\s+(\d+[/\d\w\-]+)',
            "circular": r'thông tư\s+số\s+(\d+[/\d\w\-]+)',
            "decision": r'quyết định\s+số\s+(\d+[/\d\w\-]+)',
            "constitution": r'hiến pháp\s+năm\s+(\d{4})'
        }
    
    def extract_citations_from_documents(self, documents: List[Dict[str, Any]]) -> List[LegalCitation]:
        """Extract structured citations from document list"""
        citations = []
        
        for doc in documents:
            content = doc.get("page_content", "")
            metadata = doc.get("metadata", {})
            search_type = doc.get("search_type", "vector")
            
            # For SerpAPI documents, create citation from metadata directly
            if search_type == "serp_api":
                serp_citation = LegalCitation(
                    document_type="Tài liệu internet",
                    document_name=metadata.get("document_name", "Tài liệu tìm kiếm"),
                    article=metadata.get("legal_reference", "N/A"),
                    content=content[:200] + "..." if len(content) > 200 else content,
                    law_type="Tài liệu internet",
                    year=None,
                    authority=metadata.get("authority", "SerpAPI"),
                    source=metadata.get("source", ""),
                    confidence=0.8
                )
                citations.append(serp_citation)
            else:
                # For vector database documents, extract using text patterns
                doc_citations = self.extract_citations_from_text(content)
                
                # Enhance with metadata information
                for citation in doc_citations:
                    if not citation.document_name and metadata.get("document_name"):
                        citation.document_name = metadata["document_name"]
                    if not citation.year and metadata.get("year"):
                        citation.year = metadata["year"]
                
                citations.extend(doc_citations)
        
        return citations
        
        # Remove duplicates and return unique citations
        return self._deduplicate_citations(citations)
    
    def extract_citations_from_text(self, text: str) -> List[LegalCitation]:
        """Extract citations from Vietnamese legal text"""
        citations = []
        text_lower = text.lower()
        
        # Extract law citations with numbers (high priority)
        law_matches = re.finditer(self.citation_patterns["law_with_number"], text_lower)
        for match in law_matches:
            citation = LegalCitation(
                document_type=match.group(1).title(),
                document_name=match.group(2).strip(),
                number=match.group(3)
            )
            citations.append(citation)
        
        # Extract simple law citations (without numbers)
        if not citations:  # Only if no numbered laws found
            law_simple_matches = re.finditer(self.citation_patterns["law_simple"], text_lower)
            for match in law_simple_matches:
                law_name = match.group(2).strip()
                # Filter out short matches that might be false positives
                if len(law_name) > 3 and not any(word in law_name for word in ["của", "theo", "tại"]):
                    citation = LegalCitation(
                        document_type=match.group(1).title(),
                        document_name=law_name.title(),
                        number=None
                    )
                    citations.append(citation)
        
        # Extract decree citations
        decree_matches = re.finditer(self.citation_patterns["decree"], text_lower)
        for match in decree_matches:
            citation = LegalCitation(
                document_type="Nghị định",
                document_name="",
                number=match.group(1)
            )
            citations.append(citation)
        
        # Extract article, clause, point references
        article_matches = re.finditer(self.citation_patterns["article"], text_lower)
        for match in article_matches:
            citation = LegalCitation(
                document_type="Điều luật",
                document_name="",
                article=match.group(1)
            )
            
            # Look for associated clause and point
            surrounding_text = text_lower[max(0, match.start()-50):match.end()+50]
            
            clause_match = re.search(self.citation_patterns["clause"], surrounding_text)
            if clause_match:
                citation.clause = clause_match.group(1)
            
            point_match = re.search(self.citation_patterns["point"], surrounding_text)
            if point_match:
                citation.point = point_match.group(1)
            
            citations.append(citation)
        
        return citations
    
    def extract_detailed_citations(self, documents: List[Dict], query: str) -> List[LegalCitation]:
        """Extract detailed citations with query context"""
        citations = self.extract_citations_from_documents(documents)
        
        # Filter and rank citations based on query relevance
        relevant_citations = []
        query_lower = query.lower()
        
        for citation in citations:
            relevance_score = self._calculate_citation_relevance(citation, query_lower)
            if relevance_score > 0:
                relevant_citations.append((citation, relevance_score))
        
        # Sort by relevance and return top citations
        relevant_citations.sort(key=lambda x: x[1], reverse=True)
        return [citation for citation, _ in relevant_citations[:10]]
    
    def _calculate_citation_relevance(self, citation: LegalCitation, query: str) -> float:
        """Calculate citation relevance to query"""
        score = 0.0
        
        # Check if citation elements appear in query
        if citation.article and f"điều {citation.article}" in query:
            score += 1.0
        if citation.document_name and citation.document_name.lower() in query:
            score += 0.8
        if citation.document_type and citation.document_type.lower() in query:
            score += 0.6
        if citation.clause and f"khoản {citation.clause}" in query:
            score += 0.5
        if citation.point and f"điểm {citation.point}" in query:
            score += 0.5
        
        return score
    
    def _deduplicate_citations(self, citations: List[LegalCitation]) -> List[LegalCitation]:
        """Remove duplicate citations"""
        seen = set()
        unique_citations = []
        
        for citation in citations:
            citation_key = (
                citation.document_type,
                citation.document_name,
                citation.article,
                citation.clause,
                citation.point,
                citation.number
            )
            
            if citation_key not in seen:
                seen.add(citation_key)
                unique_citations.append(citation)
        
        return unique_citations
    
    def format_citation_vietnamese(self, citation: LegalCitation) -> str:
        """Format citation according to Vietnamese legal standards"""
        return str(citation)  # Uses the __str__ method defined in LegalCitation class

class VietnameseLegalValidator:
    """Comprehensive validator for Vietnamese legal responses with OOP design"""
    
    def __init__(self):
        """Initialize validator with Vietnamese legal validation rules"""
        self.validation_rules = self._init_validation_rules()
        self.legal_terminology = self._load_legal_terminology()
        
        logger.info("VietnameseLegalValidator initialized")
    
    def _init_validation_rules(self) -> Dict[str, Any]:
        """Initialize validation rules for Vietnamese legal content"""
        return {
            "min_response_length": 50,
            "required_elements": ["căn cứ", "quy định", "theo"],
            "prohibited_terms": ["chắc chắn 100%", "hoàn toàn chính xác"],
            "citation_patterns": [r'điều\s+\d+', r'khoản\s+\d+', r'luật\s+\w+'],
            "legal_structure_indicators": ["điều", "khoản", "điểm", "chương", "mục"]
        }
    
    def _load_legal_terminology(self) -> List[str]:
        """Load Vietnamese legal terminology for validation"""
        return [
            "quyền", "nghĩa vụ", "trách nhiệm", "vi phạm", "xử phạt",
            "hợp đồng", "thỏa thuận", "tranh chấp", "giải quyết",
            "tòa án", "cơ quan", "thẩm quyền", "pháp luật", "văn bản"
        ]
    
    def validate_response(self, response: str, sources: List[Dict]) -> Dict[str, Any]:
        """Comprehensive validation of legal response"""
        validation_result = {
            "is_valid": True,
            "warnings": [],
            "confidence_adjustment": 0.0,
            "suggestions": []
        }
        
        # Length validation
        if len(response) < self.validation_rules["min_response_length"]:
            validation_result["warnings"].append("Phản hồi quá ngắn, có thể thiếu thông tin")
            validation_result["confidence_adjustment"] -= 0.1
        
        # Legal structure validation
        if not self._has_legal_structure(response):
            validation_result["warnings"].append("Thiếu cấu trúc pháp lý chuẩn (điều, khoản, điểm)")
            validation_result["confidence_adjustment"] -= 0.05
        
        # Citation validation
        citation_score = self._validate_citations(response, sources)
        if citation_score < 0.5:
            validation_result["warnings"].append("Thiếu trích dẫn hoặc tham chiếu pháp lý")
            validation_result["confidence_adjustment"] -= 0.1
        
        # Terminology validation
        if not self._has_appropriate_terminology(response):
            validation_result["warnings"].append("Thiếu thuật ngữ pháp lý chuyên môn")
            validation_result["confidence_adjustment"] -= 0.05
        
        # Prohibited terms check
        if self._has_prohibited_terms(response):
            validation_result["warnings"].append("Chứa các thuật ngữ tuyệt đối không phù hợp với tư vấn pháp lý")
            validation_result["confidence_adjustment"] -= 0.15
        
        # Overall validity assessment
        if len(validation_result["warnings"]) > 3:
            validation_result["is_valid"] = False
        
        # Add suggestions for improvement
        validation_result["suggestions"] = self._generate_improvement_suggestions(response, validation_result["warnings"])
        
        return validation_result
    
    def _has_legal_structure(self, text: str) -> bool:
        """Check if text contains proper Vietnamese legal structure"""
        text_lower = text.lower()
        structure_count = sum(
            1 for indicator in self.validation_rules["legal_structure_indicators"]
            if indicator in text_lower
        )
        return structure_count >= 1
    
    def _validate_citations(self, response: str, sources: List[Dict]) -> float:
        """Validate citation quality and relevance"""
        if not sources:
            return 0.0
        
        response_lower = response.lower()
        citation_score = 0.0
        
        # Check for citation patterns in response
        pattern_matches = sum(
            1 for pattern in self.validation_rules["citation_patterns"]
            if re.search(pattern, response_lower)
        )
        
        citation_score += pattern_matches * 0.3
        
        # Check for source document references
        source_references = 0
        for source in sources:
            metadata = source.get("metadata", {})
            if metadata.get("document_name"):
                doc_name = metadata["document_name"].lower()
                if any(word in response_lower for word in doc_name.split()[:3]):
                    source_references += 1
        
        citation_score += (source_references / len(sources)) * 0.7
        
        return min(citation_score, 1.0)
    
    def _has_appropriate_terminology(self, text: str) -> bool:
        """Check if text uses appropriate Vietnamese legal terminology"""
        text_lower = text.lower()
        terminology_count = sum(
            1 for term in self.legal_terminology
            if term in text_lower
        )
        return terminology_count >= 2
    
    def _has_prohibited_terms(self, text: str) -> bool:
        """Check for prohibited absolute terms in legal advice"""
        text_lower = text.lower()
        return any(
            prohibited in text_lower
            for prohibited in self.validation_rules["prohibited_terms"]
        )
    
    def _generate_improvement_suggestions(self, response: str, warnings: List[str]) -> List[str]:
        """Generate suggestions for improving response quality"""
        suggestions = []
        
        if "thiếu cấu trúc pháp lý" in " ".join(warnings).lower():
            suggestions.append("Thêm tham chiếu cụ thể đến điều, khoản, điểm của văn bản pháp luật")
        
        if "thiếu trích dẫn" in " ".join(warnings).lower():
            suggestions.append("Bổ sung trích dẫn từ văn bản pháp luật liên quan")
        
        if "phản hồi quá ngắn" in " ".join(warnings).lower():
            suggestions.append("Mở rộng giải thích với ví dụ và hướng dẫn cụ thể")
        
        if "thuật ngữ tuyệt đối" in " ".join(warnings).lower():
            suggestions.append("Sử dụng ngôn ngữ tư vấn phù hợp, tránh khẳng định tuyệt đối")
        
        return suggestions

# ============================================================================
# Factory and Builder Patterns for RAG System Creation
# ============================================================================

class VietnameseLegalRAGFactory:
    """Factory class for creating configured Vietnamese Legal RAG instances"""
    
    @staticmethod
    def create_standard_rag(
        pinecone_service: PineconeService,
        chat_model: Any,
        config: Optional[Dict[str, Any]] = None
    ) -> VietnameseLegalRAG:
        """Create standard configured RAG system"""
        default_config = {
            "embedding_model": "text-embedding-3-small",
            "max_results": 5,
            "confidence_threshold": 0.7
        }
        
        if config:
            default_config.update(config)
        
        embedding_model = OpenAIEmbeddings(model=default_config["embedding_model"]) if OpenAIEmbeddings else None
        
        rag = VietnameseLegalRAG(
            pinecone_service=pinecone_service,
            chat_model=chat_model,
            embedding_model=embedding_model
        )
        
        logger.info("Standard Vietnamese Legal RAG created")
        return rag
    
    @staticmethod
    def create_domain_specific_rag(
        pinecone_service: PineconeService,
        chat_model: Any,
        legal_domain: str,
        config: Optional[Dict[str, Any]] = None
    ) -> VietnameseLegalRAG:
        """Create domain-specific RAG system"""
        rag = VietnameseLegalRAGFactory.create_standard_rag(
            pinecone_service, chat_model, config
        )
        
        # Configure for specific domain
        rag.default_domain = legal_domain
        
        logger.info(f"Domain-specific RAG created for {legal_domain}")
        return rag
