"""
Enhanced Vietnamese Legal RAG System Demo
With improved error handling and demo configuration
"""

import sys
import os
from datetime import datetime
from typing import Dict, List, Any

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.demo_config import get_demo_config, validate_api_keys
from app.utils.api_key_manager import get_api_key_manager, setup_demo_keys
from app.models.legal_rag import (
    VietnameseLegalRAG,
    VietnameseLegalPromptTemplates,
    LegalCitationExtractor,
    VietnameseLegalValidator,
    LegalQueryResult,
    DocumentChunk
)


class MockPineconeService:
    """Mock Pinecone service for demo without real API calls"""
    
    def __init__(self):
        self.documents = []
        self.search_results = []
    
    def add_documents(self, documents: List[DocumentChunk]) -> bool:
        """Add documents to mock storage"""
        self.documents.extend(documents)
        print(f"📚 Added {len(documents)} documents to mock Pinecone")
        return True
    
    def search_similar(self, query: str, top_k: int = 5) -> List[DocumentChunk]:
        """Mock similarity search"""
        print(f"🔍 Mock search for: {query[:50]}...")
        
        # Return mock relevant documents based on keywords
        mock_docs = []
        
        if "dân sự" in query.lower() or "civil" in query.lower():
            mock_docs.append(DocumentChunk(
                content="Luật Dân sự 2015 quy định về quyền và nghĩa vụ của công dân. Điều 15 quy định về quyền dân sự được bảo vệ bởi pháp luật.",
                metadata={
                    "law_type": "Luật",
                    "law_name": "Luật Dân sự",
                    "year": "2015",
                    "article": "15",
                    "domain": "dan_su"
                },
                chunk_id="civil_law_001"
            ))
        
        if "lao động" in query.lower() or "làm việc" in query.lower():
            mock_docs.append(DocumentChunk(
                content="Bộ luật Lao động 2019 quy định thời gian làm việc bình thường không quá 8 giờ một ngày và không quá 48 giờ một tuần. Điều 20 quy định cụ thể về thời gian làm việc.",
                metadata={
                    "law_type": "Bộ luật",
                    "law_name": "Bộ luật Lao động",
                    "year": "2019",
                    "article": "20",
                    "domain": "lao_dong"
                },
                chunk_id="labor_law_001"
            ))
        
        return mock_docs[:top_k]


class MockChatModel:
    """Mock chat model for demo without real API calls"""
    
    def __init__(self, config, api_key: str = None):
        self.config = config
        self.api_key = api_key or config.openai_chat_api_key
    
    def generate_response(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate mock response based on the prompt"""
        user_message = messages[-1].get("content", "")
        
        # Extract query from the prompt
        if "Query:" in user_message:
            query_part = user_message.split("Query:")[1].split("\n")[0].strip()
        else:
            query_part = user_message[:100]
        
        # Generate contextual response based on keywords
        if "quyền dân sự" in query_part.lower():
            return """Theo quy định tại Luật Dân sự số 91/2015/QH13, quyền dân sự của công dân được bảo vệ toàn diện. Cụ thể:

1. **Nguyên tắc bảo vệ**: Mọi quyền lợi hợp pháp của công dân đều được pháp luật bảo vệ
2. **Phạm vi quyền dân sự**: Bao gồm quyền về nhân thân, quyền tài sản, quyền sở hữu trí tuệ
3. **Cơ chế thực hiện**: Thông qua hệ thống tòa án và các cơ quan có thẩm quyền

**Tham chiếu pháp lý**: Điều 15 Luật Dân sự 2015."""
        
        elif "điều 15" in query_part.lower():
            return """Điều 15 Luật Dân sự 2015 quy định về nguyên tắc bảo vệ quyền dân sự:

"Quyền dân sự của công dân, pháp nhân được Nhà nước thừa nhận, tôn trọng, bảo vệ và bảo đảm theo quy định của Luật này và quy định khác của pháp luật có liên quan."

**Điểm chính**:
- Nhà nước có trách nhiệm bảo vệ quyền dân sự
- Quyền dân sự được thừa nhận và tôn trọng
- Có cơ chế bảo đảm thực hiện

**Căn cứ pháp luật**: Luật Dân sự số 91/2015/QH13, có hiệu lực từ 01/01/2017."""
        
        elif "thời gian làm việc" in query_part.lower():
            return """Theo Bộ luật Lao động 2019, thời gian làm việc được quy định như sau:

**Thời gian làm việc bình thường**:
- Không quá 8 giờ trong 1 ngày làm việc
- Không quá 48 giờ trong 1 tuần làm việc

**Quy định đặc biệt**:
- Có thể làm thêm giờ theo quy định
- Một số ngành nghề có quy định riêng
- Phải đảm bảo thời gian nghỉ ngơi

**Căn cứ pháp luật**: Điều 20 Bộ luật Lao động số 45/2019/QH14."""
        
        elif "10 giờ" in query_part.lower() and "vi phạm" in query_part.lower():
            return """**PHÂN TÍCH TUÂN THỦ PHÁP LUẬT**

Yêu cầu làm việc 10 giờ/ngày có thể vi phạm pháp luật lao động:

**Vi phạm**: 
- Vượt quá giới hạn 8 giờ/ngày theo Điều 20 Bộ luật Lao động 2019
- Có thể được chấp nhận nếu là làm thêm giờ hợp pháp

**Điều kiện làm thêm giờ hợp pháp**:
- Có thỏa thuận với người lao động
- Không quá 50% thời gian làm việc bình thường trong ngày
- Đảm bảo trả lương làm thêm giờ theo quy định

**Khuyến nghị**: Cần kiểm tra hợp đồng lao động và thỏa thuận về làm thêm giờ."""
        
        else:
            return """Dựa trên tài liệu pháp lý được cung cấp, đây là thông tin tổng hợp về vấn đề pháp lý bạn quan tâm.

Để có được tư vấn chính xác và phù hợp với tình huống cụ thể, khuyến nghị bạn tham khảo ý kiến của luật sư hoặc chuyên gia pháp lý có thẩm quyền.

**Lưu ý**: Đây là thông tin tham khảo, không thay thế cho tư vấn pháp lý chuyên nghiệp."""


def run_enhanced_demo():
    """Run enhanced demo with better error handling"""
    
    print("🇻🇳 VIETNAMESE LEGAL AI CHATBOT SYSTEM")
    print("🏛️ Hệ thống Tư vấn Pháp lý AI cho Việt Nam")
    print("=" * 60)
    print(f"🕒 Enhanced Demo started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Load configuration and API key manager
    config = get_demo_config()
    api_manager = setup_demo_keys()
    
    print(f"📋 Configuration loaded: {config.chat_model}")
    print(f"🔑 API Key Manager initialized in demo mode")
    
    # Get separate API configs
    chat_config = api_manager.get_chat_config()
    embedding_config = api_manager.get_embedding_config()
    
    # Check API configuration
    issues = validate_api_keys()
    if issues:
        print("\n⚠️ API Configuration Issues (using mock services):")
        for issue in issues:
            print(f"   • {issue}")
        print("   📝 Demo will run with mock services for demonstration")
        print(f"   🔑 Chat Model: {chat_config['model']} with key {chat_config['api_key'][:10]}...")
        print(f"   🔑 Embedding Model: {embedding_config['model']} with key {embedding_config['api_key'][:10]}...")
    
    print("\n🔥 === VIETNAMESE LEGAL RAG SYSTEM ENHANCED DEMO ===")
    print("🏛️  Hệ thống Tư vấn Pháp lý AI cho Việt Nam")
    
    # Initialize with mock services
    try:
        print("\n🚀 Initializing Vietnamese Legal RAG System...")
        
        # Create mock services
        mock_pinecone = MockPineconeService()
        mock_chat = MockChatModel(config, chat_config['api_key'])
        
        # Initialize RAG system with separated API keys
        rag_system = VietnameseLegalRAG(
            pinecone_service=mock_pinecone,
            chat_model=mock_chat,
            embedding_api_key=embedding_config['api_key'],
            embedding_api_base=embedding_config['api_base']
        )
        
        print("✅ RAG System initialized successfully with mock services!")
        
        # Demo queries with enhanced responses
        demo_queries = [
            {
                "question": "Quyền dân sự của công dân được bảo vệ như thế nào?",
                "category": "🔍 General Legal Query",
                "description": "Civil Rights Protection"
            },
            {
                "question": "Điều 15 Luật Dân sự quy định gì về quyền dân sự?",
                "category": "📋 Specific Law Query", 
                "description": "Article 15 Civil Code"
            },
            {
                "question": "Thời gian làm việc theo quy định pháp luật là bao lâu?",
                "category": "⏰ Procedure Query",
                "description": "Working Hours Regulation"
            },
            {
                "question": "Công ty tôi yêu cầu làm việc 10 giờ/ngày có vi phạm không?",
                "category": "⚖️ Compliance Query",
                "description": "Working Hours Violation Check"
            }
        ]
        
        for i, query_info in enumerate(demo_queries, 1):
            print(f"\n{'=' * 60}")
            print(f"📋 QUERY {i}: {query_info['category']} - {query_info['description']}")
            print(f"❓ Question: {query_info['question']}")
            
            try:
                # Process query
                result = rag_system.query(query_info["question"])
                
                print(f"🏷️  Domain: {result.domain} | Type: {result.query_type}")
                print("-" * 60)
                
                # Display answer
                confidence_level = "HIGH" if result.confidence > 0.8 else "MEDIUM" if result.confidence > 0.5 else "LOW"
                print(f"📝 **ANSWER** (Confidence: {result.confidence:.2f} - {confidence_level}):\n")
                print(result.answer)
                
                # Show warnings if any
                if result.warnings:
                    print(f"\n⚠️ **WARNINGS**:")
                    for warning in result.warnings:
                        print(f"   • {warning}")
                
                # Show reasoning
                if result.reasoning:
                    reasoning_preview = result.reasoning[:100] + "..." if len(result.reasoning) > 100 else result.reasoning
                    print(f"\n🧠 **REASONING**: {reasoning_preview}")
                
            except Exception as e:
                print(f"❌ Error processing query: {str(e)}")
        
        # Advanced features demo
        print(f"\n{'=' * 60}")
        print("🔬 === ADVANCED FEATURES DEMO ===")
        
        # 1. Citation extraction
        print("\n🔗 1. Citation Extraction Demo:")
        citation_extractor = LegalCitationExtractor()
        sample_text = """
        Theo Luật Dân sự số 91/2015/QH13, Nghị định số 01/2021/NĐ-CP và Điều 15 Khoản 1,
        quyền dân sự được bảo vệ toàn diện.
        """
        citations = citation_extractor.extract_citations_from_text(sample_text)
        print(f"📋 Extracted {len(citations)} citations from sample text:")
        for i, citation in enumerate(citations, 1):
            print(f"   {i}. {citation.full_reference}")
        
        # 2. Response validation
        print("\n✅ 2. Response Validation Demo:")
        validator = VietnameseLegalValidator()
        sample_response = "Quyền dân sự được bảo vệ theo pháp luật Việt Nam."
        validation_result = validator.validate_response(sample_response, "dan_su")
        
        print(f"🎯 Validation Result: {'Valid' if validation_result.is_valid else 'Invalid'}")
        print(f"📊 Confidence Adjustment: {validation_result.confidence_adjustment:+.2f}")
        if validation_result.warnings:
            print("⚠️ Warnings:")
            for warning in validation_result.warnings:
                print(f"   • {warning}")
        if validation_result.suggestions:
            print("💡 Suggestions:")
            for suggestion in validation_result.suggestions:
                print(f"   • {suggestion}")
        
        # 3. Prompt templates demo
        print("\n📝 3. Prompt Templates Demo:")
        templates = VietnameseLegalPromptTemplates()
        sample_query = "Quyền sở hữu nhà đất như thế nào?"
        prompt = templates.get_general_prompt(sample_query, [], "dan_su")
        prompt_preview = prompt[:200] + "..." if len(prompt) > 200 else prompt
        print(f"🎯 Generated prompt preview: {prompt_preview}")
        
        # Demo summary
        print(f"\n{'=' * 60}")
        print("🎉 === ENHANCED DEMO SUMMARY ===")
        print("✅ Vietnamese Legal RAG System successfully demonstrated!")
        print("🚀 Features showcased:")
        print("   • Enhanced error handling and mock services")
        print("   • Vietnamese legal citation extraction")
        print("   • Response validation and quality assurance")
        print("   • Multiple legal domains support")
        print("   • Prompt template system")
        print("   • Configuration management")
        print("   • Robust fallback mechanisms")
        
        print(f"\n📊 Total Demo Queries: {len(demo_queries)}")
        print("🏆 System ready for integration with real services!")
        
    except Exception as e:
        print(f"❌ Demo initialization failed: {str(e)}")
        print("💡 Please check configuration and dependencies")


if __name__ == "__main__":
    run_enhanced_demo()
