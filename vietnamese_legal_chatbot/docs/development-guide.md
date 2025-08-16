# 👨‍💻 Development Guide - Vietnamese Legal AI Chatbot

## Getting Started

This guide provides comprehensive instructions for developers working on the Vietnamese Legal AI Chatbot project.

## Development Environment Setup

### Prerequisites

- Python 3.8+ (3.11+ recommended)
- Git
- VS Code or PyCharm (recommended)
- Docker (optional but recommended)

### Quick Setup

```bash
# Clone repository
git clone https://github.com/LePhuongPhuong/F1-Hackathon-CopilotTeam.git
cd F1-Hackathon-CopilotTeam/vietnamese_legal_chatbot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies

# Setup environment
cp .env.template .env
# Edit .env with your API keys

# Run development server
python run_development.py
```

## Project Structure

```
vietnamese_legal_chatbot/
├── app/                          # Main application code
│   ├── __init__.py
│   ├── main.py                   # FastAPI application
│   ├── streamlit_app.py          # Streamlit frontend
│   ├── models/                   # Data models and AI logic
│   │   ├── __init__.py
│   │   ├── chat_model.py         # Chat data models
│   │   └── legal_rag.py          # RAG implementation
│   ├── services/                 # Business logic services
│   │   ├── __init__.py
│   │   ├── legal_analyzer.py     # Legal document analysis
│   │   └── pinecone_service.py   # Vector database operations
│   └── utils/                    # Utility functions
│       ├── __init__.py
│       ├── config.py             # Configuration management
│       └── text_processing.py    # Text processing utilities
├── docs/                         # Documentation
├── scripts/                      # Setup and utility scripts
├── tests/                        # Test suites
├── .env.template                 # Environment template
├── requirements.txt              # Production dependencies
├── requirements-dev.txt          # Development dependencies
└── pyproject.toml               # Project configuration
```

## Code Standards

### Python Style Guide

We follow PEP 8 with some modifications:

```python
# Good: Clear function names and docstrings
def process_vietnamese_legal_query(query: str, region: str) -> Dict[str, Any]:
    """
    Process a Vietnamese legal query and return structured response.
    
    Args:
        query: The legal question in Vietnamese
        region: Vietnamese region (north, central, south)
        
    Returns:
        Dictionary containing response and citations
        
    Raises:
        ValueError: If query is empty or invalid
        ServiceError: If external services are unavailable
    """
    if not query or not query.strip():
        raise ValueError("Query cannot be empty")
    
    # Implementation here
    pass

# Bad: No type hints or documentation
def process(q, r):
    if not q:
        raise ValueError("error")
    pass
```

### Type Annotations

Use type hints throughout the codebase:

```python
from typing import Dict, List, Optional, Union
from pydantic import BaseModel

# Data models
class LegalQuery(BaseModel):
    query: str
    region: str
    legal_domain: Optional[str] = None
    user_context: Optional[Dict[str, Any]] = None

# Function signatures
async def search_legal_documents(
    query: str, 
    filters: Optional[Dict[str, str]] = None,
    limit: int = 10
) -> List[Dict[str, Any]]:
    """Search legal documents with optional filtering."""
    pass
```

### Documentation Standards

#### Docstring Format

```python
def analyze_legal_document(document: str, domain: str) -> AnalysisResult:
    """
    Analyze a legal document and extract key information.
    
    This function processes Vietnamese legal documents to extract
    articles, clauses, and legal references using NLP techniques.
    
    Args:
        document: Raw text of the legal document
        domain: Legal domain (dan_su, hinh_su, lao_dong, etc.)
        
    Returns:
        AnalysisResult object containing:
            - extracted_articles: List of article references
            - legal_concepts: Identified legal concepts
            - confidence_score: Analysis confidence (0.0-1.0)
            
    Raises:
        DocumentParseError: If document format is invalid
        DomainError: If legal domain is not supported
        
    Example:
        >>> doc = "Điều 1. Phạm vi điều chỉnh..."
        >>> result = analyze_legal_document(doc, "dan_su")
        >>> print(result.confidence_score)
        0.95
        
    Note:
        This function requires Vietnamese language models to be loaded.
        Processing time may vary based on document length.
    """
    pass
```

#### Code Comments

```python
# Good: Explain complex business logic
def calculate_legal_penalty(violation_type: str, severity: int) -> float:
    """Calculate legal penalty based on Vietnamese law."""
    
    # Base penalty rates defined in Vietnamese legal framework
    base_rates = {
        "administrative": 0.1,  # 10% of minimum wage
        "civil": 0.05,          # 5% of damages
        "criminal": 1.0         # Multiple of minimum sentence
    }
    
    # Apply severity multiplier (Article 15, Penal Code)
    severity_multiplier = min(severity * 0.5, 3.0)  # Cap at 3x
    
    return base_rates.get(violation_type, 0.0) * severity_multiplier

# Bad: Obvious comments
def add_numbers(a: int, b: int) -> int:
    # Add a and b
    return a + b  # Return the sum
```

## Development Workflow

### Git Workflow

We use GitFlow with the following branches:

- `main`: Production-ready code
- `develop`: Integration branch
- `feature/*`: Feature development
- `hotfix/*`: Critical fixes
- `release/*`: Release preparation

#### Feature Development

```bash
# Start new feature
git checkout develop
git pull origin develop
git checkout -b feature/vietnamese-legal-domain-classifier

# Work on feature
git add .
git commit -m "feat: add Vietnamese legal domain classifier

- Implement domain classification for legal queries
- Add support for 5 main legal domains
- Include confidence scoring for classifications
- Add unit tests for classifier accuracy

Closes #123"

# Push and create PR
git push origin feature/vietnamese-legal-domain-classifier
# Create Pull Request on GitHub
```

#### Commit Message Format

```
<type>(<scope>): <description>

<body>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding or modifying tests
- `chore`: Maintenance tasks

Examples:
```bash
git commit -m "feat(rag): implement Vietnamese legal document retrieval

- Add similarity search with Vietnamese embeddings
- Support metadata filtering by legal domain
- Implement relevance scoring algorithm
- Add caching for frequent queries

Resolves #456"

git commit -m "fix(api): handle empty query validation

- Add proper validation for empty legal queries
- Return appropriate error messages in Vietnamese
- Update API documentation with error codes

Fixes #789"
```

### Testing

#### Unit Tests

```python
# tests/test_legal_analyzer.py
import pytest
from app.services.legal_analyzer import LegalAnalyzer

class TestLegalAnalyzer:
    @pytest.fixture
    def analyzer(self):
        return LegalAnalyzer()
    
    def test_analyze_civil_law_document(self, analyzer):
        """Test analysis of civil law document."""
        document = """
        Điều 1. Phạm vi điều chỉnh
        Bộ luật này quy định về quan hệ dân sự...
        """
        
        result = analyzer.analyze_document(document, "dan_su")
        
        assert result.domain == "dan_su"
        assert result.confidence_score > 0.8
        assert len(result.extracted_articles) > 0
        assert "Điều 1" in result.extracted_articles[0].reference
    
    def test_invalid_domain_raises_error(self, analyzer):
        """Test that invalid domain raises appropriate error."""
        with pytest.raises(ValueError, match="Unsupported legal domain"):
            analyzer.analyze_document("test", "invalid_domain")
    
    @pytest.mark.parametrize("domain,expected_keywords", [
        ("dan_su", ["quan hệ dân sự", "quyền sở hữu"]),
        ("hinh_su", ["tội phạm", "hình phạt"]),
        ("lao_dong", ["hợp đồng lao động", "người lao động"])
    ])
    def test_domain_keyword_extraction(self, analyzer, domain, expected_keywords):
        """Test keyword extraction by legal domain."""
        document = f"Văn bản về {' và '.join(expected_keywords)}"
        result = analyzer.analyze_document(document, domain)
        
        for keyword in expected_keywords:
            assert any(keyword in concept.text for concept in result.legal_concepts)
```

#### Integration Tests

```python
# tests/integration/test_api_endpoints.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestLegalQueryAPI:
    def test_legal_query_success(self):
        """Test successful legal query processing."""
        query_data = {
            "query": "Thủ tục ly hôn thuận tình cần những gì?",
            "region": "south",
            "legal_domain": "gia_dinh"
        }
        
        response = client.post("/api/legal-query", json=query_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert "citations" in data
        assert data["response"]["confidence"] > 0.0
    
    def test_legal_query_validation_error(self):
        """Test validation error for invalid query."""
        query_data = {
            "query": "",  # Empty query should fail
            "region": "south"
        }
        
        response = client.post("/api/legal-query", json=query_data)
        
        assert response.status_code == 422
        assert "error" in response.json()
```

#### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_legal_analyzer.py

# Run tests matching pattern
pytest -k "test_legal_query"

# Run tests with verbose output
pytest -v

# Run integration tests only
pytest tests/integration/
```

### Code Quality Tools

#### Linting and Formatting

```bash
# Install development tools
pip install black flake8 isort mypy

# Format code
black app/ tests/

# Sort imports
isort app/ tests/

# Lint code
flake8 app/ tests/

# Type checking
mypy app/
```

#### Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.1.0
    hooks:
      - id: black
        language_version: python3.11
        
  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
        
  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
        
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.0.1
    hooks:
      - id: mypy
        additional_dependencies: [types-requests]
```

Install pre-commit hooks:
```bash
pip install pre-commit
pre-commit install
```

## API Development

### FastAPI Best Practices

```python
# app/api/legal_queries.py
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional, List

router = APIRouter(prefix="/api", tags=["legal-queries"])

class LegalQueryRequest(BaseModel):
    query: str = Field(..., min_length=10, max_length=1000, 
                      description="Vietnamese legal question")
    region: str = Field(..., regex="^(north|central|south|special_zones)$")
    legal_domain: Optional[str] = Field(None, 
                                       regex="^(dan_su|hinh_su|lao_dong|thuong_mai|gia_dinh)$")

class LegalQueryResponse(BaseModel):
    response: dict
    citations: List[dict]
    session_id: str

@router.post("/legal-query", response_model=LegalQueryResponse)
async def process_legal_query(
    request: LegalQueryRequest,
    # Add dependencies for authentication, rate limiting, etc.
) -> LegalQueryResponse:
    """
    Process a Vietnamese legal query and return AI-generated response.
    
    This endpoint accepts Vietnamese legal questions and returns
    comprehensive answers with legal citations and references.
    """
    try:
        # Process the query
        result = await legal_service.process_query(
            query=request.query,
            region=request.region,
            domain=request.legal_domain
        )
        
        return LegalQueryResponse(**result)
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ServiceUnavailableError as e:
        raise HTTPException(status_code=503, detail="Service temporarily unavailable")
```

### Database Operations

```python
# app/services/pinecone_service.py
import asyncio
from typing import List, Dict, Optional
import pinecone
from app.utils.config import settings

class PineconeService:
    def __init__(self):
        pinecone.init(
            api_key=settings.PINECONE_API_KEY,
            environment=settings.PINECONE_ENVIRONMENT
        )
        self.index = pinecone.Index(settings.PINECONE_INDEX_NAME)
    
    async def similarity_search(
        self, 
        query_embedding: List[float],
        filters: Optional[Dict[str, str]] = None,
        top_k: int = 10
    ) -> List[Dict]:
        """
        Perform similarity search on legal document embeddings.
        
        Args:
            query_embedding: Vector representation of the query
            filters: Metadata filters (legal_domain, region, etc.)
            top_k: Number of results to return
            
        Returns:
            List of matching documents with similarity scores
        """
        try:
            # Build filter dict for Pinecone
            pinecone_filter = {}
            if filters:
                if "legal_domain" in filters:
                    pinecone_filter["legal_domain"] = {"$eq": filters["legal_domain"]}
                if "region" in filters:
                    pinecone_filter["region"] = {"$eq": filters["region"]}
            
            # Perform search
            results = self.index.query(
                vector=query_embedding,
                filter=pinecone_filter,
                top_k=top_k,
                include_metadata=True
            )
            
            return [
                {
                    "id": match["id"],
                    "score": match["score"],
                    "content": match["metadata"]["content"],
                    "title": match["metadata"]["title"],
                    "article": match["metadata"].get("article"),
                    "legal_domain": match["metadata"]["legal_domain"]
                }
                for match in results["matches"]
            ]
            
        except Exception as e:
            logger.error(f"Pinecone search error: {e}")
            raise ServiceError(f"Vector search failed: {e}")
```

## Frontend Development

### Streamlit Components

```python
# app/components/legal_chat.py
import streamlit as st
from typing import List, Dict
from app.models.chat_model import ChatMessage

class LegalChatComponent:
    def __init__(self):
        self.initialize_session_state()
    
    def initialize_session_state(self):
        """Initialize chat-related session state variables."""
        if "chat_messages" not in st.session_state:
            st.session_state.chat_messages = []
        if "current_session_id" not in st.session_state:
            st.session_state.current_session_id = None
    
    def render_chat_interface(self) -> None:
        """Render the main chat interface."""
        st.markdown("### 💬 Tư vấn Pháp lý AI")
        
        # Display chat history
        self._render_chat_history()
        
        # Input area
        self._render_chat_input()
    
    def _render_chat_history(self) -> None:
        """Render chat message history."""
        for message in st.session_state.chat_messages:
            if message.role == "user":
                with st.chat_message("user"):
                    st.markdown(message.content)
            else:
                with st.chat_message("assistant"):
                    st.markdown(message.content)
                    if message.citations:
                        self._render_citations(message.citations)
    
    def _render_citations(self, citations: List[Dict]) -> None:
        """Render legal citations."""
        with st.expander("📋 Cơ sở pháp lý"):
            for citation in citations:
                st.markdown(f"""
                **{citation['title']}**  
                {citation['article']} - {citation['clause']}  
                *"{citation['content']}"*
                """)
    
    def _render_chat_input(self) -> None:
        """Render chat input area."""
        if prompt := st.chat_input("Nhập câu hỏi pháp lý của bạn..."):
            # Add user message
            user_message = ChatMessage(
                role="user",
                content=prompt,
                timestamp=datetime.now()
            )
            st.session_state.chat_messages.append(user_message)
            
            # Process query and add response
            with st.spinner("Đang xử lý câu hỏi..."):
                response = self._process_legal_query(prompt)
                
                assistant_message = ChatMessage(
                    role="assistant",
                    content=response["content"],
                    citations=response.get("citations", []),
                    timestamp=datetime.now()
                )
                st.session_state.chat_messages.append(assistant_message)
            
            st.rerun()
    
    def _process_legal_query(self, query: str) -> Dict:
        """Process legal query through API."""
        # Implementation here
        pass
```

### Vietnamese UI Components

```python
# app/components/vietnamese_ui.py
import streamlit as st

def render_vietnamese_header():
    """Render Vietnamese government-compliant header."""
    st.markdown("""
    <div class="vietnamese-header">
        <h1>🏛️ CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM</h1>
        <p><em>Độc lập - Tự do - Hạnh phúc</em></p>
        <h2>BỘ TƯ PHÁP</h2>
        <h3>Hệ thống Tư vấn Pháp lý AI</h3>
    </div>
    """, unsafe_allow_html=True)

def create_legal_domain_selector():
    """Create Vietnamese legal domain selector."""
    domains = {
        "dan_su": "👥 Luật Dân sự",
        "hinh_su": "🛡️ Luật Hình sự", 
        "lao_dong": "💼 Luật Lao động",
        "thuong_mai": "🏢 Luật Thương mại",
        "gia_dinh": "❤️ Luật Gia đình"
    }
    
    return st.selectbox(
        "Chọn lĩnh vực pháp lý:",
        options=list(domains.keys()),
        format_func=lambda x: domains[x],
        help="Chọn lĩnh vực pháp lý phù hợp với câu hỏi của bạn"
    )

def create_region_selector():
    """Create Vietnamese region selector."""
    regions = {
        "north": "🏔️ Miền Bắc",
        "central": "🏖️ Miền Trung",
        "south": "🌾 Miền Nam",
        "special_zones": "🏭 Khu Đặc biệt"
    }
    
    return st.selectbox(
        "Chọn vùng miền:",
        options=list(regions.keys()),
        format_func=lambda x: regions[x],
        help="Một số quy định pháp lý có thể khác nhau theo vùng miền"
    )
```

## Debugging and Troubleshooting

### Logging Setup

```python
# app/utils/logging.py
import logging
import sys
from pathlib import Path

def setup_logging(level: str = "INFO") -> None:
    """Setup application logging configuration."""
    
    # Create logs directory
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler(log_dir / "app.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Configure specific loggers
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("pinecone").setLevel(logging.WARNING)
    logging.getLogger("openai").setLevel(logging.WARNING)

# Usage in main.py
from app.utils.logging import setup_logging

setup_logging(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    logger.info(
        f"{request.method} {request.url.path} - "
        f"Status: {response.status_code} - "
        f"Time: {process_time:.3f}s"
    )
    
    return response
```

### Debug Tools

```python
# app/utils/debug.py
import json
from typing import Any, Dict
import streamlit as st

def debug_session_state():
    """Display current Streamlit session state for debugging."""
    if st.checkbox("Show Debug Info"):
        st.write("### Session State")
        st.json(dict(st.session_state))

def debug_api_response(response: Dict[str, Any]):
    """Debug API response data."""
    if st.checkbox("Show API Response"):
        st.write("### API Response")
        st.json(response)

def log_query_processing(query: str, processing_steps: Dict):
    """Log detailed query processing steps."""
    logger = logging.getLogger(__name__)
    
    logger.debug(f"Processing query: {query}")
    for step, data in processing_steps.items():
        logger.debug(f"Step {step}: {json.dumps(data, ensure_ascii=False)}")
```

## Performance Optimization

### Caching Strategies

```python
# app/utils/cache.py
from functools import lru_cache
import hashlib
import json
from typing import Any, Dict, Optional

# In-memory caching for frequently accessed data
@lru_cache(maxsize=1000)
def get_legal_domain_metadata(domain: str) -> Dict[str, Any]:
    """Cache legal domain metadata."""
    # Implementation here
    pass

# Custom cache for expensive operations
class QueryCache:
    def __init__(self, max_size: int = 100):
        self.cache = {}
        self.max_size = max_size
    
    def _hash_query(self, query: str, filters: Dict) -> str:
        """Create hash key for query and filters."""
        data = {"query": query, "filters": filters}
        return hashlib.md5(
            json.dumps(data, sort_keys=True).encode()
        ).hexdigest()
    
    def get(self, query: str, filters: Dict) -> Optional[Dict]:
        """Get cached result for query."""
        key = self._hash_query(query, filters)
        return self.cache.get(key)
    
    def set(self, query: str, filters: Dict, result: Dict) -> None:
        """Cache query result."""
        if len(self.cache) >= self.max_size:
            # Remove oldest entry
            oldest_key = next(iter(self.cache))
            del self.cache[oldest_key]
        
        key = self._hash_query(query, filters)
        self.cache[key] = result

# Global cache instance
query_cache = QueryCache()
```

### Async Operations

```python
# app/services/async_legal_service.py
import asyncio
from typing import List, Dict
import aiohttp

class AsyncLegalService:
    def __init__(self):
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def process_multiple_queries(
        self, 
        queries: List[str]
    ) -> List[Dict]:
        """Process multiple legal queries concurrently."""
        tasks = [
            self.process_single_query(query) 
            for query in queries
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle exceptions
        processed_results = []
        for result in results:
            if isinstance(result, Exception):
                processed_results.append({"error": str(result)})
            else:
                processed_results.append(result)
        
        return processed_results
    
    async def process_single_query(self, query: str) -> Dict:
        """Process a single legal query."""
        # Implementation here
        pass
```

## Contributing Guidelines

### Pull Request Process

1. **Fork and Branch**: Create a feature branch from `develop`
2. **Implement**: Write code following our standards
3. **Test**: Add appropriate test coverage
4. **Document**: Update documentation if needed
5. **Review**: Submit PR with clear description

### Code Review Checklist

- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] Documentation is updated
- [ ] No hardcoded values or secrets
- [ ] Error handling is appropriate
- [ ] Performance impact is considered
- [ ] Vietnamese text is properly handled

### Release Process

1. **Feature Freeze**: Stop adding new features
2. **Testing**: Comprehensive testing phase
3. **Documentation**: Update all documentation
4. **Release Branch**: Create from `develop`
5. **Deploy**: Deploy to staging environment
6. **Validation**: User acceptance testing
7. **Merge**: Merge to `main` and tag release

---

For development questions, contact: **dev-team@legal-ai.gov.vn**
