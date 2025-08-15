# Copilot Instructions for Vietnamese Legal AI Chatbot

## Project Overview
This is a Vietnamese Legal AI Chatbot project using a Python-only tech stack with Pinecone as the vector database. The system provides legal advice based on Vietnamese legal documents through a Streamlit frontend and FastAPI backend.

## Architecture & Key Components

### Tech Stack (Python-Only Constraint)
- **Frontend**: Streamlit (Port 8501) - Vietnamese chat interface
- **Backend**: FastAPI (Port 8000) - REST API endpoints  
- **Vector DB**: Pinecone (Cloud) - Legal document embeddings
- **LLM**: LangChain/LangGraph + OpenAI - RAG implementation
- **Documents**: PyPDF2, python-docx - Vietnamese legal text processing

### Core Service Architecture
```
Streamlit ↔ FastAPI ↔ Pinecone
    ↓         ↓         ↓
Local Storage  LLM    Vector Store
```

### Directory Structure Pattern
```
vietnamese_legal_chatbot/
├── app/
│   ├── main.py                  # FastAPI entry point
│   ├── streamlit_app.py         # Streamlit frontend
│   ├── models/legal_rag.py      # RAG implementation
│   ├── services/pinecone_service.py  # Vector operations
│   └── utils/text_processing.py # Vietnamese text handling
├── scripts/                     # Setup & deployment
└── tests/                       # pytest test suites
```

## Development Patterns

### API Endpoints Structure
Follow this pattern for FastAPI routes in `app/main.py`:
```python
POST /api/legal-query      # Main chat endpoint
POST /api/upload-document  # Document processing
GET  /api/legal-domains    # Vietnamese legal categories
GET  /api/chat-history     # Session management
```

### Vietnamese Legal Domain Handling
When implementing legal logic, support these Vietnamese law categories:
- Hiến pháp (Constitution)
- Bộ luật Dân sự (Civil Code) 
- Bộ luật Hình sự (Criminal Code)
- Bộ luật Lao động (Labor Code)
- Luật Thương mại (Commercial Law)

### Pinecone Integration Pattern
Use metadata filtering for legal domains in `services/pinecone_service.py`:
```python
# Filter by legal domain
metadata_filter = {"legal_domain": "dan_su", "language": "vietnamese"}
```

### Vietnamese Text Processing
For `utils/text_processing.py`, handle Vietnamese legal terminology and document structure recognition (chapters, articles, clauses).

## Critical Workflows

### Development Setup
```bash
# Environment setup
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt

# Pinecone initialization  
python scripts/setup_pinecone.py

# Start services
docker-compose up -d
```

### Testing Strategy
Use pytest with this structure:
- `tests/test_pinecone_service.py` - Vector operations
- `tests/test_legal_rag.py` - RAG accuracy for Vietnamese
- `tests/test_document_processor.py` - PDF/Word parsing

### Performance Requirements
- Response time: < 2 seconds for legal queries
- Accuracy: > 85% for Vietnamese legal questions  
- Concurrent users: 100+ simultaneous
- Vietnamese text processing optimization

## Environment Configuration

### Required Environment Variables
```bash
OPENAI_API_KEY=your_openai_key
PINECONE_API_KEY=your_pinecone_key  
PINECONE_ENVIRONMENT=your_pinecone_env
PINECONE_INDEX_NAME=vietnamese-legal-docs
```

### Docker Services
The `docker-compose.yml` runs both Streamlit (8501) and FastAPI (8000) services simultaneously.

## Code Quality Standards

### Python Standards
- PEP 8 compliance mandatory
- Type hints throughout codebase
- Comprehensive docstrings
- Error handling with Vietnamese error messages

### Vietnamese Language Support
- UTF-8 encoding for all Vietnamese text
- Proper handling of Vietnamese diacritics
- Legal terminology recognition and processing
- Citation formatting for Vietnamese legal documents

## Integration Points

### Streamlit-FastAPI Communication
Streamlit frontend communicates with FastAPI backend via HTTP requests. Session state managed through Streamlit's session_state.

### Pinecone Vector Operations
All document embeddings stored in Pinecone with metadata for legal domain classification and Vietnamese language processing.

### LangChain RAG Pipeline
Context-aware Vietnamese legal document retrieval with citation extraction and multi-domain knowledge handling.

## Legal Compliance
- Vietnamese data protection law compliance
- Legal accuracy validation required
- Proper disclaimers for legal advice
- Audit trail for legal queries
