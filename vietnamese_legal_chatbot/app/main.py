"""
FastAPI Backend for Vietnamese Legal AI Chatbot
Backend FastAPI cho Chatbot AI Pháp lý Việt Nam

Main entry point for the REST API serving legal queries.
Điểm vào chính cho REST API phục vụ truy vấn pháp lý.
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime
import uvicorn
import json
import logging
from pathlib import Path
import asyncio
import traceback

# Import RAG system and services
try:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    from models.legal_rag import VietnameseLegalRAG
    from services.pinecone_service import PineconeService
    from services.serp_service import SerpAPIService
    from utils.text_processing import VietnameseTextProcessor
    RAG_AVAILABLE = True
except ImportError as e:
    RAG_AVAILABLE = False
    logging.warning(f"RAG system not available: {e}")
    print(f"Warning: RAG system import failed: {e}")

# Pydantic Models for API
class LegalQuery(BaseModel):
    """Model for legal query requests"""
    question: str = Field(..., description="Legal question in Vietnamese")
    domain: str = Field(default="dan_su", description="Legal domain (dan_su, hinh_su, etc.)")
    region: str = Field(default="south", description="Vietnamese region (north, central, south, special_zones)")
    user_id: Optional[str] = Field(None, description="User identifier")
    session_id: Optional[str] = Field(None, description="Session identifier")

class LegalResponse(BaseModel):
    """Model for legal response"""
    content: str = Field(..., description="AI generated legal advice")
    citations: List[Dict[str, Any]] = Field(default=[], description="Legal citations")
    confidence: float = Field(..., description="Confidence score 0-1")
    domain: str = Field(..., description="Identified legal domain")
    timestamp: datetime = Field(default_factory=datetime.now)
    warnings: List[str] = Field(default=[], description="Legal warnings")

class ChatHistory(BaseModel):
    """Model for chat history"""
    session_id: str
    messages: List[Dict[str, Any]]
    created_at: datetime
    updated_at: datetime

# Initialize FastAPI app
app = FastAPI(
    title="Vietnamese Legal AI Chatbot API",
    description="API cho Chatbot AI Pháp lý Việt Nam - Hệ thống tư vấn pháp lý thông minh",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    contact={
        "name": "Bộ Tư pháp Việt Nam",
        "url": "https://moj.gov.vn",
        "email": "legal-ai@moj.gov.vn"
    },
    license_info={
        "name": "Government of Vietnam",
        "url": "https://chinhphu.vn"
    }
)

# CORS middleware for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501", 
        "http://127.0.0.1:8501",
        "http://0.0.0.0:8501",
        "https://legal-ai.gov.vn"  # Production domain
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer(auto_error=False)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Debug middleware to log requests
@app.middleware("http")
async def log_requests(request, call_next):
    if request.url.path == "/api/legal-query" and request.method == "POST":
        body = await request.body()
        logger.info(f"Raw request body: {body.decode('utf-8')}")
        
        # Recreate request with the body
        async def receive():
            return {"type": "http.request", "body": body}
        
        request._receive = receive
    
    response = await call_next(request)
    return response

# Initialize RAG system globally
rag_system = None
pinecone_service = None
serp_service = None

async def initialize_rag_system():
    """Initialize RAG system on startup"""
    global rag_system, pinecone_service, serp_service
    try:
        if RAG_AVAILABLE:
            logger.info("Initializing Vietnamese Legal RAG system...")
            
            # Get config - use demo config for development
            try:
                from utils.demo_config import get_demo_config
                config = get_demo_config()
                logger.info("Using demo config for development")
            except Exception as e:
                logger.warning(f"Demo config not available, using mock mode: {e}")
                config = None
                
            if config and hasattr(config, 'pinecone_api_key'):
                # Initialize Pinecone service
                pinecone_service = PineconeService(
                    api_key=config.pinecone_api_key,
                    environment=config.pinecone_environment,
                    index_name=config.pinecone_index_name,
                    openai_api_key=config.openai_embedding_api_key
                )
                
                # Initialize SerpAPI service
                serp_service = SerpAPIService(
                    api_key=config.serp_api_key
                )
                logger.info(f"SerpAPI service initialized: {serp_service.is_service_available()}")
                
                # Import and initialize chat model
                from models.chat_model import OpenAIChatModel
                chat_model = OpenAIChatModel(
                    api_key=config.openai_chat_api_key,
                    api_base=config.openai_chat_api_base,
                    model=config.chat_model
                )
                
                rag_system = VietnameseLegalRAG(
                    pinecone_service=pinecone_service,
                    chat_model=chat_model,
                    embedding_api_key=config.openai_embedding_api_key,
                    embedding_api_base=config.openai_embedding_api_base,
                    serp_service=serp_service
                )
                logger.info("RAG system initialized with real Pinecone connection")
            else:
                logger.warning("Pinecone config not available - using mock RAG system")
                rag_system = None
                pinecone_service = None
                serp_service = None
        else:
            logger.warning("RAG system not available - using mock responses")
    except Exception as e:
        logger.error(f"Failed to initialize RAG system: {e}")
        logger.error(traceback.format_exc())
        rag_system = None
        pinecone_service = None
        serp_service = None

@app.on_event("startup")
async def startup_event():
    """App startup event"""
    await initialize_rag_system()

# Vietnamese Legal Domains Configuration
VIETNAMESE_LEGAL_DOMAINS = {
    "dan_su": {
        "name": "Luật Dân sự",
        "description": "Quyền sở hữu, hợp đồng, nghĩa vụ dân sự, thừa kế",
        "keywords": ["hợp đồng", "sở hữu", "thừa kế", "dân sự", "tài sản"],
        "primary_law": "Bộ luật Dân sự 2015"
    },
    "hinh_su": {
        "name": "Luật Hình sự", 
        "description": "Tội phạm, hình phạt, thủ tục tố tụng hình sự",
        "keywords": ["tội phạm", "hình phạt", "tố tụng", "án", "tòa án"],
        "primary_law": "Bộ luật Hình sự 2015"
    },
    "lao_dong": {
        "name": "Luật Lao động",
        "description": "Hợp đồng lao động, quyền lao động, bảo hiểm xã hội",
        "keywords": ["lao động", "nghỉ việc", "lương", "bảo hiểm", "thôi việc"],
        "primary_law": "Bộ luật Lao động 2019"
    },
    "thuong_mai": {
        "name": "Luật Thương mại",
        "description": "Kinh doanh, thương mại, cạnh tranh",
        "keywords": ["kinh doanh", "thương mại", "công ty", "doanh nghiệp"],
        "primary_law": "Luật Thương mại 2005"
    },
    "gia_dinh": {
        "name": "Luật Gia đình",
        "description": "Hôn nhân, ly hôn, quyền trẻ em, nhận con nuôi",
        "keywords": ["kết hôn", "ly hôn", "trẻ em", "con nuôi", "gia đình"],
        "primary_law": "Luật Hôn nhân và Gia đình 2014"
    }
}

# Regional Legal Variations
VIETNAMESE_REGIONS = {
    "north": {
        "name": "Miền Bắc",
        "specialties": ["Đất nông nghiệp", "Di sản văn hóa", "Thương mại biên giới"],
        "legal_focus": ["Luật Đất đai", "Luật Di sản văn hóa"]
    },
    "central": {
        "name": "Miền Trung", 
        "specialties": ["Du lịch", "Thủy sản", "Thiên tai"],
        "legal_focus": ["Luật Du lịch", "Luật Thủy sản", "Luật Phòng chống thiên tai"]
    },
    "south": {
        "name": "Miền Nam",
        "specialties": ["Thương mại", "Xuất nhập khẩu", "Nông nghiệp"],
        "legal_focus": ["Luật Thương mại", "Luật Hải quan", "Luật Nông nghiệp"]
    },
    "special_zones": {
        "name": "Khu Kinh tế Đặc biệt",
        "specialties": ["Đầu tư FDI", "Thuế ưu đãi", "Hải quan"],
        "legal_focus": ["Luật Đầu tư", "Luật Thuế", "Luật Hải quan"]
    }
}

# API Endpoints

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with Vietnamese government information"""
    return {
        "service": "Vietnamese Legal AI Chatbot API",
        "version": "2.0.0",
        "status": "active",
        "government": "Cộng hòa Xã hội Chủ nghĩa Việt Nam",
        "ministry": "Bộ Tư pháp",
        "department": "Cục Pháp chế",
        "compliance": "Tuân thủ Thông tư 20/2018/TT-BTTTT",
        "endpoints": {
            "legal_query": "/api/legal-query",
            "legal_domains": "/api/legal-domains",
            "chat_history": "/api/chat-history"
        }
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "service": "vietnamese-legal-chatbot",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0"
    }

@app.post("/api/legal-query", response_model=LegalResponse, tags=["Legal"])
async def process_legal_query(query: LegalQuery):
    """
    Process legal query and return AI response
    Xử lý truy vấn pháp lý và trả về phản hồi AI
    """
    try:
        logger.info(f"Received query data: question='{query.question[:50]}...', domain='{query.domain}', region='{query.region}'")
        logger.info(f"Processing legal query: {query.question[:50]}...")
        
        # Validate domain
        if query.domain not in VIETNAMESE_LEGAL_DOMAINS:
            logger.error(f"Invalid domain '{query.domain}'. Supported: {list(VIETNAMESE_LEGAL_DOMAINS.keys())}")
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid legal domain. Supported: {list(VIETNAMESE_LEGAL_DOMAINS.keys())}"
            )
        
        # Validate region
        if query.region not in VIETNAMESE_REGIONS:
            logger.error(f"Invalid region '{query.region}'. Supported: {list(VIETNAMESE_REGIONS.keys())}")
            raise HTTPException(
                status_code=400,
                detail=f"Invalid region. Supported: {list(VIETNAMESE_REGIONS.keys())}"
            )
        
        # Auto-detect domain if not specified
        detected_domain = auto_detect_legal_domain(query.question)
        if detected_domain and query.domain == "dan_su":  # Default domain
            query.domain = detected_domain
        
        # Generate AI response (placeholder for actual RAG implementation)
        ai_response = await generate_legal_response(query)
        
        # Debug: Log response structure
        logger.info(f"Generated response structure: {type(ai_response)}")
        logger.info(f"Response content length: {len(ai_response.content) if hasattr(ai_response, 'content') else 'No content'}")
        logger.info(f"Response confidence: {ai_response.confidence if hasattr(ai_response, 'confidence') else 'No confidence'}")
        logger.info(f"Response citations count: {len(ai_response.citations) if hasattr(ai_response, 'citations') else 'No citations'}")
        
        logger.info(f"Successfully processed query for domain: {query.domain}")
        return ai_response
        
    except Exception as e:
        logger.error(f"Error processing legal query: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/api/legal-domains", tags=["Legal"])
async def get_legal_domains():
    """
    Get list of supported Vietnamese legal domains
    Lấy danh sách các lĩnh vực pháp lý Việt Nam được hỗ trợ
    """
    return {
        "domains": VIETNAMESE_LEGAL_DOMAINS,
        "total_domains": len(VIETNAMESE_LEGAL_DOMAINS),
        "description": "Vietnamese legal domains supported by the AI system"
    }

@app.get("/api/regions", tags=["Regional"])
async def get_vietnamese_regions():
    """
    Get Vietnamese regional legal variations
    Lấy thông tin biến thể pháp lý theo vùng miền Việt Nam
    """
    return {
        "regions": VIETNAMESE_REGIONS,
        "total_regions": len(VIETNAMESE_REGIONS),
        "description": "Vietnamese regional legal specializations"
    }

@app.get("/api/chat-history/{session_id}", response_model=ChatHistory, tags=["Chat"])
async def get_chat_history(session_id: str):
    """
    Get user chat history by session ID
    Lấy lịch sử chat của người dùng theo session ID
    """
    try:
        # TODO: Implement actual database lookup
        # For now, return mock data
        mock_history = ChatHistory(
            session_id=session_id,
            messages=[
                {
                    "role": "user",
                    "content": "Tôi muốn biết về thủ tục ly hôn",
                    "timestamp": "2025-08-15T10:30:00"
                },
                {
                    "role": "assistant", 
                    "content": "Theo Luật Hôn nhân và Gia đình 2014...",
                    "timestamp": "2025-08-15T10:30:30"
                }
            ],
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        return mock_history
        
    except Exception as e:
        logger.error(f"Error retrieving chat history: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve chat history")

@app.post("/api/export-chat", tags=["Export"])
async def export_chat_history(session_id: str, format: str = "json"):
    """
    Export chat history to file
    Xuất lịch sử chat ra file
    """
    try:
        if format not in ["json", "txt", "csv"]:
            raise HTTPException(status_code=400, detail="Unsupported format. Use: json, txt, csv")
        
        # TODO: Implement actual export functionality
        export_data = {
            "session_id": session_id,
            "exported_at": datetime.now().isoformat(),
            "format": format,
            "status": "success"
        }
        
        return JSONResponse(content=export_data)
        
    except Exception as e:
        logger.error(f"Error exporting chat history: {str(e)}")
        raise HTTPException(status_code=500, detail="Export failed")

# Helper Functions

def auto_detect_legal_domain(question: str) -> Optional[str]:
    """Auto-detect legal domain from question content"""
    question_lower = question.lower()
    
    for domain_key, domain_info in VIETNAMESE_LEGAL_DOMAINS.items():
        for keyword in domain_info["keywords"]:
            if keyword in question_lower:
                return domain_key
    
    return None

async def generate_legal_response(query: LegalQuery) -> LegalResponse:
    """Generate AI legal response using RAG system"""
    global rag_system, pinecone_service
    
    try:
        # Try using RAG system first
        if rag_system is not None and RAG_AVAILABLE:
            logger.info("Using RAG system for legal query processing")
            
            # Process query through RAG
            rag_result = rag_system.query(
                question=query.question,
                legal_domain=query.domain,
                max_results=5,
                confidence_threshold=0.7
            )
            
            return LegalResponse(
                content=rag_result.answer,
                citations=[{
                    "title": str(citation),
                    "article": citation.article or "N/A",
                    "content": citation.document_name,
                    "authority": "RAG System",
                    "source": citation.document_type
                } for citation in rag_result.citations],
                confidence=rag_result.confidence_score,
                domain=rag_result.legal_domain,
                warnings=rag_result.warnings or []
            )
            
        # Fallback to Pinecone direct search
        elif pinecone_service is not None:
            logger.info("Using direct Pinecone search for legal query")
            
            # Search for relevant documents
            search_results = await pinecone_service.search_similar_documents(
                query_text=query.question,
                legal_domain=query.domain,
                top_k=3
            )
            
            if search_results:
                # Combine search results into response
                combined_content = "🔍 **Kết quả tìm kiếm từ cơ sở dữ liệu pháp lý:**\n\n"
                citations = []
                
                for i, result in enumerate(search_results, 1):
                    combined_content += f"**{i}. {result.metadata.get('title', 'Tài liệu pháp lý')}**\n"
                    combined_content += f"{result.content[:500]}...\n\n"
                    
                    citations.append({
                        "title": result.metadata.get('title', 'Không rõ'),
                        "article": result.metadata.get('article_number', 'N/A'),
                        "content": result.content[:200],
                        "score": result.score,
                        "legal_domain": result.metadata.get('legal_domain', query.domain)
                    })
                
                combined_content += "\n⚠️ **Lưu ý:** Thông tin trên được truy xuất từ cơ sở dữ liệu pháp lý. Vui lòng tham khảo ý kiến chuyên gia pháp lý."
                
                return LegalResponse(
                    content=combined_content,
                    citations=citations,
                    confidence=max(r.score for r in search_results),
                    domain=query.domain,
                    warnings=["Kết quả từ tìm kiếm trực tiếp - chưa qua xử lý AI đầy đủ"]
                )
        
        # Final fallback - enhanced mock response
        logger.warning("Using enhanced mock response - no RAG/Pinecone available")
        
    except Exception as e:
        logger.error(f"Error in RAG processing: {e}")
        logger.error(traceback.format_exc())
    
    # Enhanced fallback response
    domain_info = VIETNAMESE_LEGAL_DOMAINS[query.domain]
    region_info = VIETNAMESE_REGIONS[query.region]
    
    mock_content = f"""
🔍 **Phân tích câu hỏi pháp lý** (Chế độ demo - cần kết nối cơ sở dữ liệu)

**Câu hỏi:** "{query.question}"

📋 **Lĩnh vực pháp lý:** {domain_info['name']}
🌏 **Vùng miền áp dụng:** {region_info['name']}

⚖️ **Cơ sở pháp lý chính:**
- {domain_info['primary_law']}
- Các văn bản hướng dẫn thi hành

📖 **Hướng dẫn cụ thể:**
1. Tham khảo {domain_info['primary_law']}
2. Xem xét đặc thù của {region_info['name']}: {', '.join(region_info['specialties'])}
3. Tuân thủ các quy định về: {', '.join(domain_info['keywords'])}

⚠️ **Lưu ý quan trọng:**
- ⚠️ **HỆ THỐNG ĐANG TRONG CHẾ ĐỘ DEMO**
- Cần kết nối với cơ sở dữ liệu Pinecone để có kết quả chính xác
- Thông tin này chỉ mang tính chất tham khảo
- Khuyến nghị tham khảo ý kiến luật sư chuyên nghiệp

🏛️ **Liên hệ hỗ trợ chính thức:**
- Tổng đài tư vấn pháp luật: 1900-96-96
- Cổng thông tin điện tử Bộ Tư pháp: https://moj.gov.vn
- Hệ thống tra cứu văn bản: https://thuvienphapluat.vn
"""
    
    mock_citations = [
        {
            "title": domain_info['primary_law'],
            "article": "Cần tra cứu cụ thể",
            "clause": "Theo nội dung câu hỏi", 
            "content": "Nội dung chi tiết cần truy xuất từ cơ sở dữ liệu...",
            "authority": "Quốc hội/Chính phủ",
            "status": "Demo - cần kết nối DB",
            "url": "https://thuvienphapluat.vn"
        }
    ]
    
    return LegalResponse(
        content=mock_content,
        citations=mock_citations,
        confidence=0.3,  # Low confidence for demo
        domain=query.domain,
        warnings=[
            "HỆ THỐNG DEMO - Cần kết nối cơ sở dữ liệu Pinecone",
            "Thông tin chỉ mang tính tham khảo",
            "Cần xác minh với văn bản pháp luật chính thức"
        ]
    )

# Development server runner
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
