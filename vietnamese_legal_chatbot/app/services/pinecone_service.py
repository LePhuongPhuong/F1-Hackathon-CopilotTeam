"""
Pinecone Service for Vietnamese Legal AI Chatbot
Dịch vụ Pinecone cho Chatbot AI Pháp lý Việt Nam

Handles all Pinecone vector database operations for legal documents.
Xử lý tất cả các thao tác cơ sở dữ liệu vector Pinecone cho tài liệu pháp lý.
"""

from typing import List, Dict, Optional, Tuple, Any, Union
import logging
from dataclasses import dataclass, asdict
import json
import time
import uuid
from datetime import datetime

try:
    import pinecone
    from pinecone import Pinecone, ServerlessSpec
    from langchain_community.embeddings import OpenAIEmbeddings
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    import openai
    PINECONE_AVAILABLE = True
except ImportError as e:
    PINECONE_AVAILABLE = False
    logging.warning(f"Pinecone dependencies not available: {e}")

# Conditional import để tránh config issues
try:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    
    from utils.demo_config import DemoSettings
    CONFIG_AVAILABLE = True
    config = DemoSettings()
except Exception as e:
    CONFIG_AVAILABLE = False
    logging.warning(f"Demo config not available: {e}")
    # Create a simple Settings class for testing
    class DemoSettings:
        def __init__(self):
            self.pinecone_api_key = "test-key"
            self.pinecone_environment = "us-west1-gcp"
            self.pinecone_index_name = "vietnamese-legal-docs"
            self.pinecone_dimension = 1536
            self.openai_embedding_api_key = "test-openai-key"

@dataclass
class VectorSearchResult:
    """
    Cấu trúc kết quả tìm kiếm vector
    Structure for vector search results
    """
    id: str
    score: float
    metadata: Dict[str, Any]
    content: str
    legal_domain: Optional[str] = None
    article_number: Optional[str] = None
    citation: Optional[str] = None

@dataclass
class DocumentMetadata:
    """
    Cấu trúc metadata cho tài liệu pháp lý
    Metadata structure for legal documents
    """
    document_id: str
    title: str
    legal_domain: str
    document_type: str  # Luật, Bộ luật, Nghị định, etc.
    article_number: Optional[str] = None
    chapter: Optional[str] = None
    clause: Optional[str] = None
    effective_date: Optional[str] = None
    issuing_authority: str = ""
    language: str = "vietnamese"
    source_url: Optional[str] = None
    created_at: str = ""
    
    def __post_init__(self):
        """Khởi tạo các giá trị mặc định"""
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        if not self.document_id:
            self.document_id = str(uuid.uuid4())

class PineconeServiceError(Exception):
    """Lỗi tùy chỉnh cho PineconeService"""
    def __init__(self, message: str, error_code: str = "PINECONE_ERROR"):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)

class PineconeService:
    """
    Dịch vụ Pinecone cho cơ sở dữ liệu vector tài liệu pháp lý
    Service class for Pinecone vector database operations
    """
    
    # Các domain pháp lý được hỗ trợ
    SUPPORTED_LEGAL_DOMAINS = {
        "hien_phap": "Hiến pháp",
        "dan_su": "Bộ luật Dân sự", 
        "hinh_su": "Bộ luật Hình sự",
        "lao_dong": "Bộ luật Lao động",
        "thuong_mai": "Luật Thương mại",
        "hanh_chinh": "Luật Hành chính",
        "thue": "Luật Thuế",
        "bat_dong_san": "Luật Bất động sản"
    }
    
    def __init__(
        self,
        api_key: str,
        environment: str,
        index_name: str,
        dimension: int = 1536,
        metric: str = "cosine",
        openai_api_key: Optional[str] = None
    ):
        """
        Khởi tạo dịch vụ Pinecone
        Initialize Pinecone service
        
        Args:
            api_key: Pinecone API key
            environment: Pinecone environment
            index_name: Tên index
            dimension: Số chiều vector (mặc định 1536 cho OpenAI)
            metric: Metric cho similarity (cosine, euclidean, dotproduct)
            openai_api_key: OpenAI API key cho embeddings
        """
        if not PINECONE_AVAILABLE:
            raise PineconeServiceError(
                "Không thể khởi tạo Pinecone Service: thiếu dependencies",
                "DEPENDENCY_ERROR"
            )
            
        self.api_key = api_key
        self.environment = environment
        self.index_name = index_name
        self.dimension = dimension
        self.metric = metric
        
        # Khởi tạo logging
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Khởi tạo clients
        self.pinecone_client: Optional[Pinecone] = None
        self.index = None
        self.embeddings: Optional[OpenAIEmbeddings] = None
        
        # Khởi tạo OpenAI embeddings nếu có API key
        if openai_api_key:
            try:
                # Use text-embedding-3-small (compatible with API key)
                self.embeddings = OpenAIEmbeddings(
                    openai_api_key=openai_api_key,
                    model="text-embedding-3-small"
                )
                self.logger.info(f"Đã khởi tạo OpenAI embeddings với model: text-embedding-3-small")
            except Exception as e:
                self.logger.error(f"Không thể khởi tạo OpenAI embeddings: {e}")
        
        # Initialize the client
        self._initialize_client()
    
    def _convert_environment_to_region(self, environment: str) -> str:
        """
        Convert environment name to proper region format for serverless
        """
        # Map old format to new format
        environment_map = {
            "us-east-1-aws": "us-east-1",
            "us-west1-gcp": "us-west1",
            "us-west-1": "us-west1",
            "us-central1-gcp": "us-central1",
            "asia-northeast1-gcp": "asia-northeast1",
            "eu-west1-gcp": "eu-west1"
        }
        
        # Return mapped value or original if no mapping found
        return environment_map.get(environment, environment)
    
    def _initialize_client(self) -> None:
        """
        Khởi tạo Pinecone client và index
        Initialize Pinecone client and index
        """
        try:
            # Khởi tạo Pinecone client
            self.pinecone_client = Pinecone(api_key=self.api_key)
            
            # Kiểm tra và tạo index nếu cần
            if self.index_name not in [index.name for index in self.pinecone_client.list_indexes()]:
                self.create_index()
            
            # Kết nối đến index
            self.index = self.pinecone_client.Index(self.index_name)
            
            self.logger.info(f"Đã khởi tạo thành công Pinecone client cho index: {self.index_name}")
            
        except Exception as e:
            error_msg = f"Lỗi khởi tạo Pinecone client: {str(e)}"
            self.logger.error(error_msg)
            raise PineconeServiceError(error_msg, "INITIALIZATION_ERROR")
    
    def index_exists(self) -> bool:
        """
        Kiểm tra xem index có tồn tại không
        Check if index exists
        
        Returns:
            bool: True nếu index tồn tại
        """
        try:
            existing_indexes = [index.name for index in self.pinecone_client.list_indexes()]
            return self.index_name in existing_indexes
        except Exception as e:
            self.logger.error(f"Lỗi kiểm tra index existence: {str(e)}")
            return False
    
    def create_index(self, dimension: int = 1536, metric: str = 'cosine', wait_until_ready: bool = True) -> bool:
        """
        Tạo Pinecone index nếu chưa tồn tại
        Create Pinecone index if it doesn't exist
        
        Args:
            dimension: Vector dimension (default 1536 for OpenAI embeddings)
            metric: Distance metric (default cosine)
            wait_until_ready: Chờ index sẵn sàng
            
        Returns:
            bool: True nếu tạo thành công
        """
        try:
            # Kiểm tra xem index đã tồn tại chưa
            if self.index_exists():
                self.logger.info(f"Index {self.index_name} đã tồn tại")
                return True
            
            # Tạo index mới với cấu hình serverless
            region = self._convert_environment_to_region(self.environment)
            self.pinecone_client.create_index(
                name=self.index_name,
                dimension=dimension,
                metric=metric,
                spec=ServerlessSpec(
                    cloud="aws",
                    region=region
                )
            )
            
            self.logger.info(f"Đã tạo index {self.index_name} với dimension {self.dimension}")
            
            # Chờ index sẵn sàng
            if wait_until_ready:
                self._wait_for_index_ready()
            
            return True
            
        except Exception as e:
            error_msg = f"Lỗi tạo index: {str(e)}"
            self.logger.error(error_msg)
            raise PineconeServiceError(error_msg, "INDEX_CREATION_ERROR")
    
    def _wait_for_index_ready(self, timeout: int = 60) -> None:
        """
        Chờ index sẵn sàng
        Wait for index to be ready
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                index_description = self.pinecone_client.describe_index(self.index_name)
                if index_description.status.ready:
                    self.logger.info(f"Index {self.index_name} đã sẵn sàng")
                    return
                time.sleep(2)
            except Exception as e:
                self.logger.warning(f"Lỗi kiểm tra trạng thái index: {e}")
                time.sleep(2)
        
        raise PineconeServiceError(
            f"Index {self.index_name} không sẵn sàng sau {timeout} giây",
            "INDEX_TIMEOUT_ERROR"
        )
    
    def upsert_documents(
        self, 
        documents: List[Dict[str, Any]], 
        batch_size: int = 100,
        namespace: str = ""
    ) -> bool:
        """
        Upsert tài liệu vào Pinecone theo batch
        Upsert documents to Pinecone in batches
        
        Args:
            documents: Danh sách tài liệu với content và metadata
            batch_size: Kích thước batch
            namespace: Namespace để tổ chức dữ liệu
            
        Returns:
            bool: True nếu thành công
        """
        try:
            if not self.index:
                raise PineconeServiceError("Index chưa được khởi tạo", "INDEX_NOT_INITIALIZED")
            
            if not self.embeddings:
                raise PineconeServiceError("Embeddings chưa được khởi tạo", "EMBEDDINGS_NOT_INITIALIZED")
            
            total_docs = len(documents)
            self.logger.info(f"Bắt đầu upsert {total_docs} tài liệu với batch size {batch_size}")
            
            # Xử lý documents theo batch
            for i in range(0, total_docs, batch_size):
                batch = documents[i:i + batch_size]
                vectors_to_upsert = []
                
                for doc in batch:
                    try:
                        # Tạo embedding cho content
                        content = doc.get("content", "")
                        if not content:
                            self.logger.warning(f"Document {doc.get('id', 'unknown')} không có content")
                            continue
                        
                        # Tạo vector embedding
                        embedding = self.embeddings.embed_query(content)
                        
                        # Chuẩn bị metadata
                        metadata = doc.get("metadata", {})
                        metadata.update({
                            "content": content[:1000],  # Lưu một phần content trong metadata
                            "content_length": len(content),
                            "upserted_at": datetime.now().isoformat()
                        })
                        
                        # Validate legal domain
                        legal_domain = metadata.get("legal_domain")
                        if legal_domain and not self._validate_legal_domain(legal_domain):
                            self.logger.warning(f"Legal domain không hợp lệ: {legal_domain}")
                        
                        vectors_to_upsert.append({
                            "id": doc.get("id", str(uuid.uuid4())),
                            "values": embedding,
                            "metadata": metadata
                        })
                        
                    except Exception as e:
                        self.logger.error(f"Lỗi xử lý document {doc.get('id', 'unknown')}: {e}")
                        continue
                
                # Upsert batch vào Pinecone
                if vectors_to_upsert:
                    self.index.upsert(vectors=vectors_to_upsert, namespace=namespace)
                    self.logger.info(f"Đã upsert batch {i//batch_size + 1}: {len(vectors_to_upsert)} vectors")
            
            self.logger.info(f"Hoàn thành upsert {total_docs} tài liệu")
            return True
            
        except Exception as e:
            error_msg = f"Lỗi upsert documents: {str(e)}"
            self.logger.error(error_msg)
            raise PineconeServiceError(error_msg, "UPSERT_ERROR")
    
    def search_similar_documents(
        self,
        query: str,
        legal_domain: Optional[str] = None,
        top_k: int = 5,
        score_threshold: float = 0.7,
        namespace: str = "",
        include_metadata: bool = True
    ) -> List[VectorSearchResult]:
        """
        Tìm kiếm tài liệu tương tự dựa trên query
        Search for similar documents based on query
        
        Args:
            query: Câu hỏi hoặc nội dung tìm kiếm
            legal_domain: Lọc theo domain pháp lý
            top_k: Số lượng kết quả trả về
            score_threshold: Ngưỡng điểm similarity
            namespace: Namespace để tìm kiếm
            include_metadata: Có trả về metadata không
            
        Returns:
            List[VectorSearchResult]: Danh sách kết quả tìm kiếm
        """
        try:
            if not self.index:
                raise PineconeServiceError("Index chưa được khởi tạo", "INDEX_NOT_INITIALIZED")
            
            if not self.embeddings:
                raise PineconeServiceError("Embeddings chưa được khởi tạo", "EMBEDDINGS_NOT_INITIALIZED")
            
            self.logger.info(f"Tìm kiếm: '{query[:50]}...' trong domain: {legal_domain}")
            
            # Tạo query embedding
            query_embedding = self.embeddings.embed_query(query)
            
            # Chuẩn bị metadata filter
            metadata_filter = {}
            if legal_domain:
                if not self._validate_legal_domain(legal_domain):
                    self.logger.warning(f"Legal domain không hợp lệ: {legal_domain}")
                else:
                    metadata_filter["legal_domain"] = legal_domain
            
            # Thực hiện tìm kiếm
            search_response = self.index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=include_metadata,
                include_values=False,
                namespace=namespace,
                filter=metadata_filter if metadata_filter else None
            )
            
            # Xử lý kết quả
            results = []
            for match in search_response.matches:
                if match.score >= score_threshold:
                    metadata = match.metadata or {}
                    
                    result = VectorSearchResult(
                        id=match.id,
                        score=match.score,
                        metadata=metadata,
                        content=metadata.get("content", ""),
                        legal_domain=metadata.get("legal_domain"),
                        article_number=metadata.get("article_number"),
                        citation=self._build_citation(metadata)
                    )
                    results.append(result)
            
            self.logger.info(f"Tìm thấy {len(results)} kết quả phù hợp (score >= {score_threshold})")
            return results
            
        except Exception as e:
            error_msg = f"Lỗi tìm kiếm: {str(e)}"
            self.logger.error(error_msg)
            raise PineconeServiceError(error_msg, "SEARCH_ERROR")
    
    def similarity_search(
        self,
        query_text: str = None,
        query: str = None,
        k: int = 5,
        score_threshold: float = 0.7,
        filter: Optional[Dict[str, Any]] = None,
        metadata_filter: Optional[Dict[str, Any]] = None,
        namespace: str = ""
    ) -> List[str]:
        """
        Tìm kiếm tương tự theo chuẩn LangChain interface
        LangChain-compatible similarity search
        
        Args:
            query_text: Câu hỏi hoặc nội dung tìm kiếm (legacy parameter)
            query: Câu hỏi hoặc nội dung tìm kiếm (new parameter)
            k: Số lượng kết quả trả về
            score_threshold: Ngưỡng điểm similarity
            filter: Bộ lọc metadata (LangChain style)
            metadata_filter: Bộ lọc metadata (legacy parameter)
            namespace: Namespace để tìm kiếm
            
        Returns:
            List[str]: Danh sách nội dung tài liệu tương tự
        """
        try:
            # Handle backward compatibility for parameter names
            search_query = query_text or query
            search_filter = metadata_filter or filter
            
            if not search_query:
                raise PineconeServiceError("Query text is required", "MISSING_QUERY")
            
            if not self.index:
                raise PineconeServiceError("Index chưa được khởi tạo", "INDEX_NOT_INITIALIZED")
            
            if not self.embeddings:
                raise PineconeServiceError("Embeddings chưa được khởi tạo", "EMBEDDINGS_NOT_INITIALIZED")
            
            self.logger.info(f"LangChain similarity search: '{search_query[:50]}...'")
            
            # Tạo query embedding
            query_embedding = self.embeddings.embed_query(search_query)
            
            # Thực hiện tìm kiếm
            search_response = self.index.query(
                vector=query_embedding,
                top_k=k,
                include_metadata=True,
                include_values=False,
                namespace=namespace,
                filter=search_filter
            )
            
            # Xử lý kết quả - chỉ trả về content
            results = []
            for match in search_response.matches:
                if match.score >= score_threshold:
                    metadata = match.metadata or {}
                    content = metadata.get("content", "")
                    if content:
                        results.append(content)
            
            self.logger.info(f"LangChain search: Tìm thấy {len(results)} tài liệu phù hợp")
            return results
            
        except Exception as e:
            error_msg = f"Lỗi LangChain similarity search: {str(e)}"
            self.logger.error(error_msg)
            # Fallback - return empty list instead of raising error for LangChain compatibility
            self.logger.warning("Returning empty results for LangChain compatibility")
            return []
    
    def search_by_metadata(
        self,
        filters: Dict[str, Any],
        top_k: int = 10,
        namespace: str = ""
    ) -> List[VectorSearchResult]:
        """
        Tìm kiếm tài liệu theo metadata
        Search documents by metadata filters
        
        Args:
            filters: Bộ lọc metadata
            top_k: Số lượng kết quả
            namespace: Namespace để tìm kiếm
            
        Returns:
            List[VectorSearchResult]: Danh sách kết quả
        """
        try:
            if not self.index:
                raise PineconeServiceError("Index chưa được khởi tạo", "INDEX_NOT_INITIALIZED")
            
            self.logger.info(f"Tìm kiếm theo metadata: {filters}")
            
            # Tạo dummy vector (vì Pinecone yêu cầu vector cho query)
            dummy_vector = [0.0] * self.dimension
            
            # Thực hiện tìm kiếm với filter
            search_response = self.index.query(
                vector=dummy_vector,
                top_k=top_k,
                include_metadata=True,
                include_values=False,
                namespace=namespace,
                filter=filters
            )
            
            # Xử lý kết quả
            results = []
            for match in search_response.matches:
                metadata = match.metadata or {}
                
                result = VectorSearchResult(
                    id=match.id,
                    score=match.score,
                    metadata=metadata,
                    content=metadata.get("content", ""),
                    legal_domain=metadata.get("legal_domain"),
                    article_number=metadata.get("article_number"),
                    citation=self._build_citation(metadata)
                )
                results.append(result)
            
            self.logger.info(f"Tìm thấy {len(results)} kết quả theo metadata")
            return results
            
        except Exception as e:
            error_msg = f"Lỗi tìm kiếm theo metadata: {str(e)}"
            self.logger.error(error_msg)
            raise PineconeServiceError(error_msg, "METADATA_SEARCH_ERROR")
    
    def delete_documents(self, document_ids: List[str], namespace: str = "") -> bool:
        """
        Xóa tài liệu theo ID
        Delete documents by IDs
        
        Args:
            document_ids: Danh sách ID tài liệu cần xóa
            namespace: Namespace chứa tài liệu
            
        Returns:
            bool: True nếu xóa thành công
        """
        try:
            if not self.index:
                raise PineconeServiceError("Index chưa được khởi tạo", "INDEX_NOT_INITIALIZED")
            
            if not document_ids:
                self.logger.warning("Không có document IDs để xóa")
                return True
            
            self.logger.info(f"Xóa {len(document_ids)} tài liệu")
            
            # Xóa documents khỏi Pinecone
            self.index.delete(ids=document_ids, namespace=namespace)
            
            self.logger.info(f"Đã xóa thành công {len(document_ids)} tài liệu")
            return True
            
        except Exception as e:
            error_msg = f"Lỗi xóa tài liệu: {str(e)}"
            self.logger.error(error_msg)
            raise PineconeServiceError(error_msg, "DELETE_ERROR")
    
    def delete_by_filter(self, filter_dict: Dict[str, Any], namespace: str = "") -> bool:
        """
        Xóa tài liệu theo filter
        Delete documents by metadata filter
        
        Args:
            filter_dict: Bộ lọc metadata
            namespace: Namespace chứa tài liệu
            
        Returns:
            bool: True nếu xóa thành công
        """
        try:
            if not self.index:
                raise PineconeServiceError("Index chưa được khởi tạo", "INDEX_NOT_INITIALIZED")
            
            self.logger.info(f"Xóa tài liệu theo filter: {filter_dict}")
            
            # Xóa theo filter
            self.index.delete(filter=filter_dict, namespace=namespace)
            
            self.logger.info("Đã xóa tài liệu theo filter thành công")
            return True
            
        except Exception as e:
            error_msg = f"Lỗi xóa tài liệu theo filter: {str(e)}"
            self.logger.error(error_msg)
            raise PineconeServiceError(error_msg, "DELETE_FILTER_ERROR")
    
    def get_index_stats(self, namespace: str = "") -> Dict[str, Any]:
        """
        Lấy thống kê index
        Get index statistics
        
        Args:
            namespace: Namespace để lấy thống kê
            
        Returns:
            Dict[str, Any]: Thống kê index
        """
        try:
            if not self.index:
                raise PineconeServiceError("Index chưa được khởi tạo", "INDEX_NOT_INITIALIZED")
            
            # Lấy thống kê từ Pinecone
            stats = self.index.describe_index_stats()
            
            result = {
                "total_vectors": stats.total_vector_count,
                "dimension": stats.dimension,
                "index_fullness": stats.index_fullness,
                "namespaces": {}
            }
            
            # Thêm thông tin namespace
            if hasattr(stats, 'namespaces') and stats.namespaces:
                for ns_name, ns_stats in stats.namespaces.items():
                    result["namespaces"][ns_name] = {
                        "vector_count": ns_stats.vector_count
                    }
            
            self.logger.info(f"Thống kê index: {result['total_vectors']} vectors")
            return result
            
        except Exception as e:
            error_msg = f"Lỗi lấy thống kê index: {str(e)}"
            self.logger.error(error_msg)
            raise PineconeServiceError(error_msg, "STATS_ERROR")
    
    def _validate_legal_domain(self, domain: str) -> bool:
        """
        Validate legal domain
        
        Args:
            domain: Legal domain to validate
            
        Returns:
            bool: True nếu domain hợp lệ
        """
        return domain in self.SUPPORTED_LEGAL_DOMAINS
    
    def _build_citation(self, metadata: Dict[str, Any]) -> Optional[str]:
        """
        Tạo citation từ metadata
        Build citation from metadata
        
        Args:
            metadata: Document metadata
            
        Returns:
            Optional[str]: Citation string
        """
        try:
            parts = []
            
            # Tên tài liệu
            if metadata.get("title"):
                parts.append(metadata["title"])
            
            # Điều/Khoản
            if metadata.get("article_number"):
                parts.append(f"Điều {metadata['article_number']}")
            
            if metadata.get("clause"):
                parts.append(f"Khoản {metadata['clause']}")
            
            # Chương
            if metadata.get("chapter"):
                parts.append(f"Chương {metadata['chapter']}")
            
            # Cơ quan ban hành
            if metadata.get("issuing_authority"):
                parts.append(f"({metadata['issuing_authority']})")
            
            return ", ".join(parts) if parts else None
            
        except Exception as e:
            self.logger.warning(f"Lỗi tạo citation: {e}")
            return None
    
    def get_supported_domains(self) -> Dict[str, str]:
        """
        Lấy danh sách các domain pháp lý được hỗ trợ
        Get supported legal domains
        
        Returns:
            Dict[str, str]: Mapping domain code to Vietnamese name
        """
        return self.SUPPORTED_LEGAL_DOMAINS.copy()
    
    def health_check(self) -> Dict[str, Any]:
        """
        Kiểm tra sức khỏe của service
        Health check for the service
        
        Returns:
            Dict[str, Any]: Health status
        """
        try:
            status = {
                "service": "PineconeService",
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "index_name": self.index_name,
                "index_ready": False,
                "embeddings_ready": False
            }
            
            # Kiểm tra index
            if self.index:
                stats = self.get_index_stats()
                status["index_ready"] = True
                status["total_vectors"] = stats.get("total_vectors", 0)
            
            # Kiểm tra embeddings
            if self.embeddings:
                status["embeddings_ready"] = True
            
            return status
            
        except Exception as e:
            return {
                "service": "PineconeService",
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

class LegalDocumentProcessor:
    """
    Bộ xử lý tài liệu pháp lý để chuẩn bị cho lưu trữ vector
    Processor for preparing legal documents for vector storage
    """
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Khởi tạo document processor
        Initialize document processor
        
        Args:
            chunk_size: Kích thước chunk (ký tự)
            chunk_overlap: Độ chồng lấp giữa các chunk
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Khởi tạo text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
        )
    
    def process_legal_document(
        self, 
        content: str, 
        metadata: DocumentMetadata
    ) -> List[Dict[str, Any]]:
        """
        Xử lý tài liệu pháp lý thành các chunk với metadata
        Process legal document into chunks with metadata
        
        Args:
            content: Nội dung tài liệu
            metadata: Metadata của tài liệu
            
        Returns:
            List[Dict[str, Any]]: Danh sách chunks đã xử lý
        """
        try:
            if not content.strip():
                self.logger.warning("Nội dung tài liệu rỗng")
                return []
            
            self.logger.info(f"Xử lý tài liệu: {metadata.title}")
            
            # Trích xuất cấu trúc pháp luật
            legal_structure = self.extract_legal_structure(content)
            
            # Chia tài liệu thành chunks
            chunks = self.text_splitter.split_text(content)
            
            processed_chunks = []
            for i, chunk in enumerate(chunks):
                # Tạo ID unique cho chunk
                chunk_id = f"{metadata.document_id}_chunk_{i}"
                
                # Tạo metadata cho chunk
                chunk_metadata = asdict(metadata)
                chunk_metadata.update({
                    "chunk_id": chunk_id,
                    "chunk_index": i,
                    "total_chunks": len(chunks),
                    "content_length": len(chunk),
                    "chunk_type": self._identify_chunk_type(chunk)
                })
                
                # Thêm thông tin cấu trúc nếu có
                article_info = self._extract_article_from_chunk(chunk)
                if article_info:
                    chunk_metadata.update(article_info)
                
                processed_chunk = {
                    "id": chunk_id,
                    "content": chunk,
                    "metadata": chunk_metadata
                }
                
                processed_chunks.append(processed_chunk)
            
            self.logger.info(f"Đã xử lý thành {len(processed_chunks)} chunks")
            return processed_chunks
            
        except Exception as e:
            error_msg = f"Lỗi xử lý tài liệu: {str(e)}"
            self.logger.error(error_msg)
            raise PineconeServiceError(error_msg, "DOCUMENT_PROCESSING_ERROR")
    
    def extract_legal_structure(self, content: str) -> Dict[str, Any]:
        """
        Trích xuất cấu trúc tài liệu pháp lý Việt Nam
        Extract Vietnamese legal document structure
        
        Args:
            content: Nội dung tài liệu
            
        Returns:
            Dict[str, Any]: Thông tin cấu trúc
        """
        import re
        
        structure = {
            "chapters": [],
            "articles": [],
            "clauses": [],
            "points": []
        }
        
        try:
            # Tìm chương (Chương I, II, III...)
            chapter_pattern = r'CHƯƠNG\s+([IVXLCDM]+|[0-9]+)[\s\.:]*([^\n]+)?'
            chapters = re.findall(chapter_pattern, content, re.IGNORECASE)
            structure["chapters"] = [{"number": ch[0], "title": ch[1].strip()} for ch in chapters]
            
            # Tìm điều (Điều 1, 2, 3...)
            article_pattern = r'Điều\s+([0-9]+)[\s\.:]*([^\n]+)?'
            articles = re.findall(article_pattern, content, re.IGNORECASE)
            structure["articles"] = [{"number": art[0], "title": art[1].strip()} for art in articles]
            
            # Tìm khoản (1., 2., 3... hoặc a), b), c)...)
            clause_pattern = r'^([0-9]+)\.\s+([^\n]+)|^([a-z])\)\s+([^\n]+)'
            clauses = re.findall(clause_pattern, content, re.MULTILINE | re.IGNORECASE)
            for clause in clauses:
                if clause[0]:  # Khoản số
                    structure["clauses"].append({"number": clause[0], "content": clause[1]})
                elif clause[2]:  # Khoản chữ
                    structure["clauses"].append({"letter": clause[2], "content": clause[3]})
            
            self.logger.debug(f"Trích xuất cấu trúc: {len(structure['chapters'])} chương, "
                            f"{len(structure['articles'])} điều")
            
        except Exception as e:
            self.logger.warning(f"Lỗi trích xuất cấu trúc: {e}")
        
        return structure
    
    def _identify_chunk_type(self, chunk: str) -> str:
        """
        Xác định loại chunk (title, article, clause, content)
        Identify chunk type
        """
        import re
        
        chunk_upper = chunk.upper().strip()
        
        if re.match(r'CHƯƠNG\s+[IVXLCDM0-9]+', chunk_upper):
            return "chapter"
        elif re.match(r'ĐIỀU\s+[0-9]+', chunk_upper):
            return "article"
        elif re.match(r'^[0-9]+\.\s+', chunk.strip()):
            return "clause"
        elif re.match(r'^[a-z]\)\s+', chunk.strip(), re.IGNORECASE):
            return "point"
        else:
            return "content"
    
    def _extract_article_from_chunk(self, chunk: str) -> Optional[Dict[str, str]]:
        """
        Trích xuất thông tin điều từ chunk
        Extract article information from chunk
        """
        import re
        
        try:
            # Tìm số điều
            article_match = re.search(r'Điều\s+([0-9]+)', chunk, re.IGNORECASE)
            if article_match:
                return {"article_number": article_match.group(1)}
            
            # Tìm khoản
            clause_match = re.search(r'^([0-9]+)\.\s+', chunk.strip())
            if clause_match:
                return {"clause": clause_match.group(1)}
            
        except Exception as e:
            self.logger.debug(f"Lỗi trích xuất article info: {e}")
        
        return None

class VietnameseLegalMetadataBuilder:
    """
    Builder cho metadata tài liệu pháp lý Việt Nam
    Builder for Vietnamese legal document metadata
    """
    
    # Mapping các loại tài liệu pháp lý
    DOCUMENT_TYPES = {
        "hien_phap": "Hiến pháp",
        "luat": "Luật",
        "bo_luat": "Bộ luật", 
        "nghi_dinh": "Nghị định",
        "quyet_dinh": "Quyết định",
        "thong_tu": "Thông tư",
        "chi_thi": "Chỉ thị",
        "nghi_quyet": "Nghị quyết"
    }
    
    # Mapping cơ quan ban hành
    ISSUING_AUTHORITIES = {
        "quoc_hoi": "Quốc hội",
        "chu_tich_nuoc": "Chủ tịch nước",
        "chinh_phu": "Chính phủ",
        "thu_tuong": "Thủ tướng Chính phủ",
        "bo_tu_phap": "Bộ Tư pháp",
        "bo_cong_an": "Bộ Công an",
        "bo_tai_chinh": "Bộ Tài chính",
        "bo_lao_dong": "Bộ Lao động - Thương binh và Xã hội"
    }
    
    @staticmethod
    def build_metadata(
        document_type: str,
        title: str,
        legal_domain: str,
        issuing_authority: str = "",
        **kwargs
    ) -> DocumentMetadata:
        """
        Tạo metadata chuẩn cho tài liệu pháp lý Việt Nam
        Build standardized metadata for Vietnamese legal documents
        
        Args:
            document_type: Loại tài liệu (luat, bo_luat, nghi_dinh...)
            title: Tiêu đề tài liệu
            legal_domain: Domain pháp lý
            issuing_authority: Cơ quan ban hành
            **kwargs: Các thông tin bổ sung
            
        Returns:
            DocumentMetadata: Metadata đã được chuẩn hóa
        """
        try:
            # Chuẩn hóa document type
            standardized_doc_type = VietnameseLegalMetadataBuilder.DOCUMENT_TYPES.get(
                document_type.lower(), document_type
            )
            
            # Chuẩn hóa issuing authority
            standardized_authority = VietnameseLegalMetadataBuilder.ISSUING_AUTHORITIES.get(
                issuing_authority.lower(), issuing_authority
            )
            
            # Tạo document ID nếu chưa có
            document_id = kwargs.get("document_id") or str(uuid.uuid4())
            
            metadata = DocumentMetadata(
                document_id=document_id,
                title=title.strip(),
                legal_domain=legal_domain.lower(),
                document_type=standardized_doc_type,
                article_number=kwargs.get("article_number"),
                chapter=kwargs.get("chapter"),
                clause=kwargs.get("clause"),
                effective_date=kwargs.get("effective_date"),
                issuing_authority=standardized_authority,
                language="vietnamese",
                source_url=kwargs.get("source_url"),
                created_at=kwargs.get("created_at", datetime.now().isoformat())
            )
            
            return metadata
            
        except Exception as e:
            logging.error(f"Lỗi tạo metadata: {e}")
            raise PineconeServiceError(f"Lỗi tạo metadata: {str(e)}", "METADATA_BUILD_ERROR")
    
    @staticmethod
    def validate_legal_domain(domain: str) -> bool:
        """
        Kiểm tra domain pháp lý có hợp lệ không
        Validate if legal domain is supported
        
        Args:
            domain: Domain code cần kiểm tra
            
        Returns:
            bool: True nếu domain hợp lệ
        """
        return domain.lower() in PineconeService.SUPPORTED_LEGAL_DOMAINS
    
    @staticmethod
    def validate_document_type(doc_type: str) -> bool:
        """
        Kiểm tra loại tài liệu có hợp lệ không
        Validate document type
        
        Args:
            doc_type: Document type cần kiểm tra
            
        Returns:
            bool: True nếu document type hợp lệ
        """
        return doc_type.lower() in VietnameseLegalMetadataBuilder.DOCUMENT_TYPES
    
    @staticmethod
    def get_supported_document_types() -> Dict[str, str]:
        """
        Lấy danh sách các loại tài liệu được hỗ trợ
        Get supported document types
        
        Returns:
            Dict[str, str]: Mapping document type code to Vietnamese name
        """
        return VietnameseLegalMetadataBuilder.DOCUMENT_TYPES.copy()
    
    @staticmethod
    def get_supported_authorities() -> Dict[str, str]:
        """
        Lấy danh sách các cơ quan ban hành được hỗ trợ
        Get supported issuing authorities
        
        Returns:
            Dict[str, str]: Mapping authority code to Vietnamese name
        """
        return VietnameseLegalMetadataBuilder.ISSUING_AUTHORITIES.copy()
    
    @staticmethod
    def extract_metadata_from_title(title: str) -> Dict[str, Any]:
        """
        Trích xuất metadata từ tiêu đề tài liệu
        Extract metadata from document title
        
        Args:
            title: Tiêu đề tài liệu
            
        Returns:
            Dict[str, Any]: Metadata đã trích xuất
        """
        import re
        
        extracted = {}
        
        try:
            title_upper = title.upper()
            
            # Xác định loại tài liệu từ tiêu đề
            if "HIẾN PHÁP" in title_upper:
                extracted["document_type"] = "hien_phap"
                extracted["legal_domain"] = "hien_phap"
            elif "BỘ LUẬT DÂN SỰ" in title_upper:
                extracted["document_type"] = "bo_luat"
                extracted["legal_domain"] = "dan_su"
            elif "BỘ LUẬT HÌNH SỰ" in title_upper:
                extracted["document_type"] = "bo_luat"
                extracted["legal_domain"] = "hinh_su"
            elif "BỘ LUẬT LAO ĐỘNG" in title_upper:
                extracted["document_type"] = "bo_luat"
                extracted["legal_domain"] = "lao_dong"
            elif "LUẬT" in title_upper:
                extracted["document_type"] = "luat"
            elif "NGHỊ ĐỊNH" in title_upper:
                extracted["document_type"] = "nghi_dinh"
            elif "THÔNG TƯ" in title_upper:
                extracted["document_type"] = "thong_tu"
            
            # Trích xuất số hiệu
            number_pattern = r'(\d+/\d+/[A-Z-]+)'
            number_match = re.search(number_pattern, title)
            if number_match:
                extracted["document_number"] = number_match.group(1)
            
            # Trích xuất năm
            year_pattern = r'(\d{4})'
            year_matches = re.findall(year_pattern, title)
            if year_matches:
                extracted["year"] = year_matches[-1]  # Lấy năm cuối cùng
            
        except Exception as e:
            logging.warning(f"Lỗi trích xuất metadata từ title: {e}")
        
        return extracted


# Factory class để tạo PineconeService với cấu hình từ Settings
class PineconeServiceFactory:
    """
    Factory để tạo PineconeService instance
    Factory for creating PineconeService instances
    """
    
    @staticmethod
    def create_from_settings(settings: DemoSettings) -> PineconeService:
        """
        Tạo PineconeService từ DemoSettings object
        Create PineconeService from DemoSettings object
        
        Args:
            settings: DemoSettings object chứa cấu hình
            
        Returns:
            PineconeService: Instance đã được cấu hình
        """
        return PineconeService(
            api_key=settings.pinecone_api_key,
            environment=settings.pinecone_environment,
            index_name=settings.pinecone_index_name,
            dimension=settings.pinecone_dimension,
            openai_api_key=settings.openai_embedding_api_key
        )
    
    @staticmethod
    def create_from_env() -> PineconeService:
        """
        Tạo PineconeService từ environment variables
        Create PineconeService from environment variables
        
        Returns:
            PineconeService: Instance đã được cấu hình
        """
        settings = DemoSettings()
        return PineconeServiceFactory.create_from_settings(settings)
