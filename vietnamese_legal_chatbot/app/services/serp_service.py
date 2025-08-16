"""
SerpAPI Service for Vietnamese Legal Documents Search
Dịch vụ SerpAPI để tìm kiếm tài liệu pháp lý Việt Nam
"""

import logging
from typing import List, Dict, Optional, Any
from serpapi import GoogleSearch
import traceback

logger = logging.getLogger(__name__)

class SerpAPIService:
    """Service for searching Vietnamese legal documents using SerpAPI"""
    
    def __init__(self, api_key: str):
        """Initialize SerpAPI service"""
        self.api_key = api_key
        self.is_available = bool(api_key and api_key != "demo-serp-key")
        
        if self.is_available:
            logger.info("SerpAPI service initialized successfully")
        else:
            logger.warning("SerpAPI service not available - using mock data")
    
    def search_legal_documents(self, question: str, max_results: int = 5) -> List[Dict]:
        """
        Search for Vietnamese legal documents using SerpAPI
        
        Args:
            question: Legal question to search for
            max_results: Maximum number of results to return
            
        Returns:
            List of legal documents with metadata
        """
        if not self.is_available:
            logger.info("SerpAPI not available, returning empty results")
            return []
        
        try:
            legal_docs = []
            
            # Construct search queries for Vietnamese legal documents
            search_queries = [
                f'"{question}" thư viện pháp luật việt nam',
                f'"{question}" luật việt nam filetype:pdf',
                f'"{question}" bộ luật dân sự việt nam',
                f'"{question}" site:thuvienphapluat.vn',
                f'{question} pháp luật việt nam'
            ]
            
            logger.info(f"🔍 SerpAPI: Searching with {len(search_queries)} queries for: {question}")
            
            for i, query in enumerate(search_queries):
                try:
                    logger.info(f"🔍 SerpAPI Query {i+1}: {query}")
                    
                    search = GoogleSearch({
                        "q": query,
                        "location": "Vietnam",
                        "hl": "vi",
                        "gl": "vn",
                        "api_key": self.api_key,
                        "num": 3
                    })
                    
                    results = search.get_dict()
                    organic_results = results.get('organic_results', [])
                    logger.info(f"📊 SerpAPI Query {i+1} results: {len(organic_results)} items")
                    
                    if organic_results:
                        for result in organic_results[:2]:  # Limit to 2 per query
                            legal_doc = {
                                'id': f"serp_{result.get('position', 0)}_{len(legal_docs)}",
                                'title': result.get('title', 'Tài liệu pháp lý'),
                                'content': self._format_serp_content(result, question),
                                'law_type': 'tim_kiem',
                                'article': 'Kết quả tìm kiếm',
                                'authority': 'SerpAPI',
                                'source': result.get('link', ''),
                                'snippet': result.get('snippet', ''),
                                'url': result.get('link', ''),
                                'relevance_score': 0.8,  # Default relevance for SerpAPI results
                                'search_query': query
                            }
                            legal_docs.append(legal_doc)
                            
                            if len(legal_docs) >= max_results:
                                break
                                
                except Exception as search_error:
                    logger.error(f"⚠️ SerpAPI search error for query '{query}': {str(search_error)}")
                    continue
                    
                if len(legal_docs) >= max_results:
                    break
                    
            logger.info(f"✅ SerpAPI search completed: {len(legal_docs)} documents found")
            return legal_docs[:max_results]
            
        except Exception as e:
            logger.error(f"❌ SerpAPI service error: {str(e)}")
            logger.error(traceback.format_exc())
            return []
    
    def _format_serp_content(self, result: Dict, question: str) -> str:
        """Format SerpAPI result into legal document content"""
        return f"""🔍 **Kết quả tìm kiếm tự động**

**Nguồn:** {result.get('link', '')}

**Tiêu đề:** {result.get('title', '')}

**Mô tả:** {result.get('snippet', '')}

**Câu hỏi liên quan:** "{question}"

**⚠️ Lưu ý quan trọng:** 
- Đây là kết quả tìm kiếm tự động từ internet
- Vui lòng truy cập nguồn gốc để có thông tin chính xác và cập nhật
- Nên tham khảo thêm các tài liệu pháp lý chính thức
- Thông tin có thể cần được xác minh bởi chuyên gia pháp lý

**Truy cập nguồn:** {result.get('link', '')}"""

    def get_search_suggestions(self, question: str) -> List[str]:
        """Get search suggestions for legal queries"""
        base_terms = [
            "luật việt nam",
            "bộ luật dân sự",
            "bộ luật hình sự", 
            "bộ luật lao động",
            "thư viện pháp luật",
            "văn bản pháp luật",
            "nghị định",
            "thông tư"
        ]
        
        suggestions = []
        for term in base_terms:
            suggestions.append(f"{question} {term}")
            
        return suggestions[:5]

    def is_service_available(self) -> bool:
        """Check if SerpAPI service is available"""
        return self.is_available
