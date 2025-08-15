"""
FastAPI Backend for Vietnamese Legal AI Chatbot
Backend FastAPI cho Chatbot AI Pháp lý Việt Nam

Main entry point for the REST API serving legal queries and document processing.
Điểm vào chính cho REST API phục vụ truy vấn pháp lý và xử lý tài liệu.
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime
import uvicorn
import json
import logging
from pathlib import Path

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

class DocumentUpload(BaseModel):
    """Model for document upload response"""
    filename: str
    size: int
    document_type: str
    analysis_status: str
    extracted_text_preview: str

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
            "upload_document": "/api/upload-document", 
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
        logger.info(f"Processing legal query: {query.question[:50]}...")
        
        # Validate domain
        if query.domain not in VIETNAMESE_LEGAL_DOMAINS:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid legal domain. Supported: {list(VIETNAMESE_LEGAL_DOMAINS.keys())}"
            )
        
        # Validate region
        if query.region not in VIETNAMESE_REGIONS:
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
        
        logger.info(f"Successfully processed query for domain: {query.domain}")
        return ai_response
        
    except Exception as e:
        logger.error(f"Error processing legal query: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/api/upload-document", response_model=DocumentUpload, tags=["Documents"])
async def upload_legal_document(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """
    Upload and process legal document
    Tải lên và xử lý tài liệu pháp lý
    """
    try:
        # Validate file type
        allowed_types = ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "text/plain"]
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file type. Allowed: PDF, DOCX, TXT"
            )
        
        # Validate file size (max 10MB)
        max_size = 10 * 1024 * 1024  # 10MB
        file_content = await file.read()
        if len(file_content) > max_size:
            raise HTTPException(
                status_code=400,
                detail="File size exceeds maximum limit of 10MB"
            )
        
        # Save file temporarily
        upload_dir = Path("data/uploads")
        upload_dir.mkdir(exist_ok=True)
        
        file_path = upload_dir / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
        with open(file_path, "wb") as f:
            f.write(file_content)
        
        # Extract preview text
        preview_text = extract_text_preview(file_content, file.content_type)
        
        # Schedule background processing
        background_tasks.add_task(process_document_background, str(file_path))
        
        response = DocumentUpload(
            filename=file.filename,
            size=len(file_content),
            document_type=file.content_type,
            analysis_status="processing",
            extracted_text_preview=preview_text
        )
        
        logger.info(f"Document uploaded successfully: {file.filename}")
        return response
        
    except Exception as e:
        logger.error(f"Error uploading document: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

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
    """Generate AI legal response (placeholder for actual RAG implementation)"""
    
    domain_info = VIETNAMESE_LEGAL_DOMAINS[query.domain]
    region_info = VIETNAMESE_REGIONS[query.region]
    
    # Mock response - replace with actual AI/RAG implementation
    mock_content = f"""
🔍 **Phân tích câu hỏi pháp lý**

Dựa trên câu hỏi: "{query.question}"

📋 **Lĩnh vực pháp lý:** {domain_info['name']}
🌏 **Vùng miền:** {region_info['name']}

⚖️ **Cơ sở pháp lý chính:**
- {domain_info['primary_law']}
- Các văn bản hướng dẫn liên quan

📖 **Hướng dẫn cụ thể:**
1. Tham khảo {domain_info['primary_law']}
2. Tuân thủ quy định của {region_info['name']}
3. Đặc thù về: {', '.join(region_info['specialties'])}

⚠️ **Lưu ý quan trọng:**
- Thông tin này chỉ mang tính chất tham khảo
- Khuyến nghị tham khảo ý kiến luật sư cho các vấn đề phức tạp
- Kiểm tra văn bản pháp luật mới nhất

🏛️ **Liên hệ hỗ trợ:**
- Tổng đài tư vấn pháp luật: 1900-96-96
- Website: https://moj.gov.vn
"""
    
    mock_citations = [
        {
            "title": domain_info['primary_law'],
            "article": "Điều 15",
            "clause": "Khoản 1", 
            "content": "Quy định về quyền và nghĩa vụ cơ bản...",
            "authority": "Quốc hội",
            "date": "2015-06-19",
            "url": "https://thuvienphapluat.vn"
        }
    ]
    
    return LegalResponse(
        content=mock_content,
        citations=mock_citations,
        confidence=0.85,
        domain=query.domain,
        warnings=[
            "Thông tin chỉ mang tính tham khảo",
            "Cần xác minh với văn bản pháp luật mới nhất"
        ]
    )

def extract_text_preview(file_content: bytes, content_type: str) -> str:
    """Extract preview text from uploaded document"""
    # TODO: Implement actual text extraction for PDF, DOCX
    preview = f"Preview of {content_type} document ({len(file_content)} bytes)"
    return preview[:200] + "..." if len(preview) > 200 else preview

async def process_document_background(file_path: str):
    """Background task to process uploaded document"""
    logger.info(f"Starting background processing for: {file_path}")
    # TODO: Implement document processing, text extraction, legal analysis
    logger.info(f"Completed background processing for: {file_path}")

# TODO: Implement endpoints
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "vietnamese-legal-chatbot"}

# TODO: Legal Query Endpoints
@app.post("/api/legal-query")
async def process_legal_query():
    """Process legal query and return AI response"""
    pass

@app.post("/api/upload-document")
async def upload_legal_document():
    """Upload and process legal document"""
    pass

@app.get("/api/legal-domains")
async def get_legal_domains():
    """Get list of supported Vietnamese legal domains"""
    pass

@app.get("/api/chat-history")
async def get_chat_history():
    """Get user chat history"""
    pass

@app.post("/api/export-chat")
async def export_chat_history():
    """Export chat history to CSV/JSON"""
    pass

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
