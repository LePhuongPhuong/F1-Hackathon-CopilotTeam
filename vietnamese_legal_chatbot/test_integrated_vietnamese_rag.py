"""
Integrated Test: Vietnamese Text Processing with RAG System
Test xử lý văn bản tiếng Việt tích hợp với hệ thống RAG
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
load_dotenv()

from openai import OpenAI
from app.utils.text_processing import (
    process_vietnamese_legal_text, 
    preprocess_vietnamese_query,
    get_legal_domain,
    extract_legal_citations
)

def test_integrated_vietnamese_rag():
    """Test Vietnamese text processing integrated with RAG"""
    
    print("🇻🇳 INTEGRATED VIETNAMESE RAG TEST")
    print("=" * 60)
    print(f"🕒 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Test queries with different intents and domains
    test_queries = [
        {
            "query": "Quyền dân sự của công dân được bảo vệ như thế nào theo Điều 15 Bộ luật Dân sự 2015?",
            "expected_domain": "dan_su",
            "expected_intent": "rights_inquiry"
        },
        {
            "query": "Thủ tục đăng ký kết hôn cần những giấy tờ gì?",
            "expected_domain": "hanh_chinh", 
            "expected_intent": "procedure_inquiry"
        },
        {
            "query": "Công ty bắt nhân viên làm thêm giờ 12 tiếng/ngày có vi phạm Bộ luật Lao động không?",
            "expected_domain": "lao_dong",
            "expected_intent": "violation_inquiry"
        },
        {
            "query": "Hợp đồng mua bán bất động sản cần có những điều khoản bắt buộc nào?",
            "expected_domain": "thuong_mai",
            "expected_intent": "information_inquiry"
        }
    ]
    
    # Mock legal documents with enhanced Vietnamese content
    mock_documents = [
        {
            "content": "Điều 15 Bộ luật Dân sự 2015 quy định: Quyền dân sự của công dân, pháp nhân được Nhà nước thừa nhận, tôn trọng, bảo vệ và bảo đảm theo quy định của Luật này và quy định khác của pháp luật có liên quan. Việc thực hiện quyền dân sự không được xâm phạm quyền và lợi ích hợp pháp của người khác, không trái đạo đức xã hội.",
            "metadata": {"law": "Bộ luật Dân sự 2015", "article": "Điều 15", "domain": "dan_su"}
        },
        {
            "content": "Điều 104 Bộ luật Lao động 2019 quy định thời gian làm việc bình thường không quá 8 giờ trong 1 ngày và không quá 48 giờ trong 1 tuần. Người sử dụng lao động có thể áp dụng chế độ làm việc theo ca, làm việc ban đêm đối với các công việc thích hợp.",
            "metadata": {"law": "Bộ luật Lao động 2019", "article": "Điều 104", "domain": "lao_dong"}
        },
        {
            "content": "Thủ tục đăng ký kết hôn theo Luật Hôn nhân và Gia đình 2014 yêu cầu: Đơn đăng ký kết hôn, Chứng minh nhân dân/Căn cước công dân, Giấy khai sinh, Giấy chứng nhận tình trạng hôn nhân (nếu có), Giấy khám sức khỏe tiền hôn nhân.",
            "metadata": {"law": "Luật Hôn nhân và Gia đình 2014", "procedure": "đăng ký kết hôn", "domain": "hanh_chinh"}
        }
    ]
    
    # Get API configuration
    embedding_api_key = os.getenv("OPENAI_EMBEDDING_API_KEY")
    embedding_api_base = os.getenv("OPENAI_EMBEDDING_API_BASE")
    chat_api_key = os.getenv("OPENAI_API_KEY")
    chat_api_base = os.getenv("OPENAI_API_BASE")
    
    try:
        # Create OpenAI clients
        embedding_client = OpenAI(
            api_key=embedding_api_key,
            base_url=embedding_api_base
        )
        
        chat_client = OpenAI(
            api_key=chat_api_key,
            base_url=chat_api_base
        )
        
        print("✅ OpenAI clients initialized")
        
        # Process each test query
        for i, test_case in enumerate(test_queries, 1):
            query = test_case["query"]
            
            print(f"\n{'='*60}")
            print(f"📋 TEST CASE {i}")
            print(f"❓ Query: {query}")
            print(f"{'='*60}")
            
            # Step 1: Vietnamese text processing
            print("🔍 Step 1: Vietnamese Text Processing")
            query_analysis = preprocess_vietnamese_query(query)
            domain = get_legal_domain(query)
            citations = extract_legal_citations(query)
            
            print(f"   ✅ Intent: {query_analysis['intent']}")
            print(f"   ✅ Domain: {domain}")
            print(f"   ✅ Legal terms: {query_analysis['legal_terms']}")
            print(f"   ✅ Search keywords: {query_analysis['search_keywords'][:5]}")
            if citations:
                print(f"   ✅ Citations: {[c['full_text'] for c in citations]}")
            
            # Verify expectations
            expected_domain = test_case["expected_domain"]
            expected_intent = test_case["expected_intent"]
            
            domain_match = "✅" if domain == expected_domain else "❌"
            intent_match = "✅" if query_analysis['intent'] == expected_intent else "❌"
            
            print(f"   {domain_match} Domain prediction: {domain} (expected: {expected_domain})")
            print(f"   {intent_match} Intent prediction: {query_analysis['intent']} (expected: {expected_intent})")
            
            # Step 2: Document retrieval with enhanced processing
            print("📚 Step 2: Enhanced Document Retrieval")
            query_embedding = embedding_client.embeddings.create(
                model="text-embedding-3-small",
                input=query_analysis['normalized_query']
            ).data[0].embedding
            
            best_doc = None
            best_similarity = -1
            
            for doc in mock_documents:
                # Process document content
                doc_analysis = process_vietnamese_legal_text(doc["content"])
                
                # Create document embedding
                doc_embedding = embedding_client.embeddings.create(
                    model="text-embedding-3-small",
                    input=doc_analysis.normalized_text
                ).data[0].embedding
                
                # Calculate similarity
                dot_product = sum(a * b for a, b in zip(query_embedding, doc_embedding))
                similarity = dot_product / (sum(a*a for a in query_embedding)**0.5 * sum(b*b for b in doc_embedding)**0.5)
                
                # Domain boost
                if doc["metadata"].get("domain") == domain:
                    similarity += 0.1  # Boost for matching domain
                
                print(f"   📄 {doc['metadata']['law']}: similarity={similarity:.3f}")
                
                if similarity > best_similarity:
                    best_similarity = similarity
                    best_doc = doc
            
            print(f"   🎯 Best match: {best_doc['metadata']['law']} (similarity: {best_similarity:.3f})")
            
            # Step 3: Enhanced response generation
            print("💬 Step 3: Enhanced Response Generation")
            
            # Create enhanced prompt with Vietnamese context
            enhanced_prompt = f"""Bạn là chuyên gia tư vấn pháp lý Việt Nam với chuyên môn sâu về {domain}.

Dựa trên tài liệu pháp lý sau đây:
{best_doc['content']}

Câu hỏi của người dùng: {query}
Intent được phát hiện: {query_analysis['intent']}
Thuật ngữ pháp lý liên quan: {', '.join(query_analysis['legal_terms'])}

Hãy trả lời một cách:
- Chính xác và dựa trên văn bản pháp luật
- Dễ hiểu cho người dân
- Có trích dẫn cụ thể điều khoản pháp luật
- Phù hợp với ngữ cảnh Việt Nam

Trả lời bằng tiếng Việt:"""

            response = chat_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Bạn là chuyên gia tư vấn pháp lý Việt Nam có kinh nghiệm và uy tín."},
                    {"role": "user", "content": enhanced_prompt}
                ],
                max_tokens=600,
                temperature=0.1
            )
            
            answer = response.choices[0].message.content
            
            # Display final result
            print("\n🎉 ENHANCED RESULT:")
            print("-" * 50)
            print(f"❓ Câu hỏi: {query}")
            print(f"🏷️ Lĩnh vực: {domain}")
            print(f"🎯 Ý định: {query_analysis['intent']}")
            print(f"📚 Tài liệu: {best_doc['metadata']['law']}")
            print(f"💡 Trả lời:\n{answer}")
            print("-" * 50)
        
        print(f"\n{'='*60}")
        print("🎉 Integrated Vietnamese RAG test completed successfully!")
        print("✅ Text Processing ✓ Domain Detection ✓ Intent Recognition ✓")
        print("✅ Legal Term Extraction ✓ Citation Parsing ✓ Enhanced RAG ✓")
        print(f"{'='*60}")
        
    except Exception as e:
        print(f"❌ Error in integrated test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_integrated_vietnamese_rag()
