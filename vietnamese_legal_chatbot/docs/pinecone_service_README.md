# PineconeService Documentation

## Tổng quan (Overview)

`PineconeService` là một service class OOP hoàn chỉnh được thiết kế để quản lý cơ sở dữ liệu vector Pinecone cho hệ thống Vietnamese Legal AI Chatbot. Service này tuân thủ các nguyên tắc OOP và cung cấp các tính năng chuyên biệt cho việc xử lý tài liệu pháp lý Việt Nam.

## Tính năng chính (Key Features)

### 🔧 Core Functionality
- **Vector Database Operations**: Upsert, search, delete documents trong Pinecone
- **Vietnamese Legal Domain Support**: Hỗ trợ 8 domain pháp lý chính của Việt Nam
- **Automatic Text Processing**: Tự động chia nhỏ và xử lý tài liệu pháp lý
- **Metadata Management**: Quản lý metadata chuẩn hóa cho tài liệu pháp lý
- **Error Handling**: Xử lý lỗi với thông báo tiếng Việt

### 📚 Legal Domains Supported
- `hien_phap`: Hiến pháp
- `dan_su`: Bộ luật Dân sự
- `hinh_su`: Bộ luật Hình sự  
- `lao_dong`: Bộ luật Lao động
- `thuong_mai`: Luật Thương mại
- `hanh_chinh`: Luật Hành chính
- `thue`: Luật Thuế
- `bat_dong_san`: Luật Bất động sản

## Cấu trúc Classes (Class Structure)

### 1. PineconeService
Class chính để thao tác với Pinecone vector database.

```python
from app.services.pinecone_service import PineconeService

service = PineconeService(
    api_key="your-pinecone-api-key",
    environment="us-west1-gcp", 
    index_name="vietnamese-legal-docs",
    dimension=1536,
    openai_api_key="your-openai-api-key"
)
```

#### Key Methods:
- `upsert_documents()`: Upload tài liệu vào vector database
- `search_similar_documents()`: Tìm kiếm tài liệu tương tự
- `search_by_metadata()`: Tìm kiếm theo metadata filter
- `delete_documents()`: Xóa tài liệu theo ID
- `get_index_stats()`: Lấy thống kê index
- `health_check()`: Kiểm tra trạng thái service

### 2. LegalDocumentProcessor  
Class xử lý tài liệu pháp lý thành chunks phù hợp cho vector storage.

```python
from app.services.pinecone_service import LegalDocumentProcessor

processor = LegalDocumentProcessor(chunk_size=1000, chunk_overlap=200)
chunks = processor.process_legal_document(content, metadata)
```

#### Key Methods:
- `process_legal_document()`: Chia tài liệu thành chunks với metadata
- `extract_legal_structure()`: Trích xuất cấu trúc pháp lý (Chương, Điều, Khoản)
- `_identify_chunk_type()`: Xác định loại chunk (article, clause, content...)

### 3. VietnameseLegalMetadataBuilder
Builder pattern để tạo metadata chuẩn hóa cho tài liệu pháp lý Việt Nam.

```python
from app.services.pinecone_service import VietnameseLegalMetadataBuilder

metadata = VietnameseLegalMetadataBuilder.build_metadata(
    document_type="bo_luat",
    title="Bộ luật Dân sự 2015", 
    legal_domain="dan_su",
    issuing_authority="quoc_hoi"
)
```

#### Key Methods:
- `build_metadata()`: Tạo metadata chuẩn hóa
- `validate_legal_domain()`: Validate domain pháp lý
- `extract_metadata_from_title()`: Trích xuất metadata từ tiêu đề

### 4. Data Classes

#### DocumentMetadata
```python
@dataclass
class DocumentMetadata:
    document_id: str
    title: str
    legal_domain: str
    document_type: str
    article_number: Optional[str] = None
    chapter: Optional[str] = None
    clause: Optional[str] = None
    effective_date: Optional[str] = None
    issuing_authority: str = ""
    language: str = "vietnamese"
    source_url: Optional[str] = None
    created_at: str = ""
```

#### VectorSearchResult
```python
@dataclass
class VectorSearchResult:
    id: str
    score: float
    metadata: Dict[str, Any]
    content: str
    legal_domain: Optional[str] = None
    article_number: Optional[str] = None
    citation: Optional[str] = None
```

## Cách sử dụng (Usage Examples)

### 1. Khởi tạo Service

```python
# Method 1: Từ environment variables
from app.services.pinecone_service import PineconeServiceFactory
service = PineconeServiceFactory.create_from_env()

# Method 2: Trực tiếp với parameters
from app.services.pinecone_service import PineconeService
service = PineconeService(
    api_key="your-api-key",
    environment="us-west1-gcp",
    index_name="vietnamese-legal-docs"
)
```

### 2. Upload Tài liệu

```python
# Chuẩn bị dữ liệu
documents = [
    {
        "id": "doc_1_chunk_0",
        "content": "Điều 1. Phạm vi điều chỉnh của Bộ luật...",
        "metadata": {
            "title": "Bộ luật Dân sự 2015",
            "legal_domain": "dan_su",
            "article_number": "1",
            "document_type": "Bộ luật"
        }
    }
]

# Upload
success = service.upsert_documents(documents, batch_size=100)
```

### 3. Tìm kiếm Tương tự

```python
# Tìm kiếm cơ bản
results = service.search_similar_documents(
    query="quan hệ dân sự là gì?",
    legal_domain="dan_su",
    top_k=5,
    score_threshold=0.7
)

# Hiển thị kết quả
for result in results:
    print(f"Score: {result.score}")
    print(f"Citation: {result.citation}")
    print(f"Content: {result.content[:100]}...")
```

### 4. Tìm kiếm theo Metadata

```python
# Tìm tất cả Điều 1 trong Bộ luật Dân sự
results = service.search_by_metadata({
    "legal_domain": "dan_su",
    "article_number": "1",
    "document_type": "Bộ luật"
})
```

### 5. Xử lý Tài liệu Pháp lý

```python
# Tạo processor
processor = LegalDocumentProcessor(chunk_size=1000, chunk_overlap=200)

# Tạo metadata
metadata = VietnameseLegalMetadataBuilder.build_metadata(
    document_type="bo_luat",
    title="Bộ luật Dân sự 2015",
    legal_domain="dan_su",
    issuing_authority="quoc_hoi"
)

# Xử lý tài liệu
legal_content = """
CHƯƠNG I - QUY ĐỊNH CHUNG
Điều 1. Phạm vi điều chỉnh
1. Bộ luật này quy định về quan hệ dân sự...
"""

chunks = processor.process_legal_document(legal_content, metadata)
```

### 6. Health Check

```python
# Kiểm tra trạng thái service
health = service.health_check()
print(f"Status: {health['status']}")
print(f"Index ready: {health['index_ready']}")
print(f"Total vectors: {health.get('total_vectors', 0)}")
```

## Error Handling

Service sử dụng custom exception `PineconeServiceError` với thông báo tiếng Việt:

```python
from app.services.pinecone_service import PineconeServiceError

try:
    service.upsert_documents(documents)
except PineconeServiceError as e:
    print(f"Lỗi: {e.message}")
    print(f"Mã lỗi: {e.error_code}")
```

### Các loại lỗi thường gặp:
- `DEPENDENCY_ERROR`: Thiếu dependencies
- `INITIALIZATION_ERROR`: Lỗi khởi tạo
- `INDEX_CREATION_ERROR`: Lỗi tạo index
- `UPSERT_ERROR`: Lỗi upload document
- `SEARCH_ERROR`: Lỗi tìm kiếm
- `DELETE_ERROR`: Lỗi xóa document

## Environment Variables

Các biến môi trường cần thiết:

```bash
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENVIRONMENT=us-west1-gcp  
PINECONE_INDEX_NAME=vietnamese-legal-docs
PINECONE_DIMENSION=1536
OPENAI_API_KEY=your_openai_api_key
```

## Dependencies

```bash
pip install pinecone-client openai langchain python-dotenv pydantic
```

## Testing

Chạy tests:

```bash
# Chạy test cơ bản
python tests/test_pinecone_service.py

# Chạy với pytest
pytest tests/test_pinecone_service.py -v

# Chạy demo
python examples/pinecone_service_demo.py
```

## Cấu trúc Vietnamese Legal Document

Service hỗ trợ nhận diện và xử lý cấu trúc tài liệu pháp lý Việt Nam:

### Hierarchy Structure:
1. **Chương** (Chapter): CHƯƠNG I, II, III...
2. **Mục** (Section): Mục 1, 2, 3...  
3. **Điều** (Article): Điều 1, 2, 3...
4. **Khoản** (Clause): 1., 2., 3...
5. **Điểm** (Point): a), b), c)...

### Document Types:
- **Hiến pháp**: Constitution
- **Luật**: Law
- **Bộ luật**: Code
- **Nghị định**: Decree
- **Quyết định**: Decision
- **Thông tư**: Circular
- **Chỉ thị**: Directive

## Best Practices

### 1. OOP Principles
- **Single Responsibility**: Mỗi class có một trách nhiệm cụ thể
- **Dependency Injection**: Service nhận dependencies qua constructor
- **Error Handling**: Sử dụng custom exceptions với thông báo rõ ràng
- **Type Hints**: Đầy đủ type hints cho tất cả methods

### 2. Performance
- **Batch Processing**: Upload documents theo batch để tối ưu hiệu suất
- **Chunking Strategy**: Chia tài liệu hợp lý để cân bằng context và search quality
- **Metadata Filtering**: Sử dụng metadata filter để tối ưu search

### 3. Vietnamese Language
- **UTF-8 Encoding**: Đảm bảo encoding đúng cho tiếng Việt
- **Diacritics Handling**: Xử lý đúng dấu tiếng Việt
- **Legal Terms**: Nhận diện thuật ngữ pháp lý chuyên môn

### 4. Scalability
- **Namespace Support**: Sử dụng namespace để tổ chức dữ liệu
- **Async Ready**: Thiết kế sẵn sàng cho async operations
- **Connection Pooling**: Tối ưu kết nối với Pinecone

## Roadmap

### Planned Features:
- [ ] Async support cho tất cả operations
- [ ] Advanced search với semantic ranking
- [ ] Document versioning và change tracking
- [ ] Integration với popular Vietnamese NLP libraries
- [ ] Advanced citation extraction và linking
- [ ] Multi-language support (English legal documents)
- [ ] Real-time document updates
- [ ] Advanced analytics và reporting

## Contributing

Khi contribute code, đảm bảo:

1. **Code Quality**: PEP 8, type hints, docstring đầy đủ
2. **Testing**: Unit tests cho tất cả methods mới
3. **Documentation**: Cập nhật documentation cho features mới
4. **Vietnamese Support**: Đảm bảo hỗ trợ tiếng Việt đầy đủ
5. **OOP Design**: Tuân thủ nguyên tắc OOP và design patterns

## Support

Để được hỗ trợ:
1. Kiểm tra documentation này trước
2. Chạy health_check() để kiểm tra service status
3. Xem logs để debug issues
4. Tạo issue với thông tin chi tiết về lỗi

---

*Vietnamese Legal AI Chatbot - PineconeService v1.0*
