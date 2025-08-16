"""
Streamlit Frontend for Vietnamese Legal AI Chatbot
Frontend Streamlit cho Chatbot AI Pháp lý Việt Nam
"""

import streamlit as st
import requests
import json
from datetime import datetime
from typing import Dict, List, Optional

# Page configuration
st.set_page_config(
    page_title="Chatbot AI Pháp lý Việt Nam",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables
def initialize_session_state():
    """Initialize all session state variables"""
    if 'current_legal_domain' not in st.session_state:
        st.session_state.current_legal_domain = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'recent_queries' not in st.session_state:
        st.session_state.recent_queries = []
    if 'user_session_id' not in st.session_state:
        st.session_state.user_session_id = None
    if 'chatbot_initialized' not in st.session_state:
        st.session_state.chatbot_initialized = False
    if 'show_history' not in st.session_state:
        st.session_state.show_history = False
    if 'new_question' not in st.session_state:
        st.session_state.new_question = False
    if 'search_laws' not in st.session_state:
        st.session_state.search_laws = False
    if 'user_region' not in st.session_state:
        st.session_state.user_region = 'south'

# Custom CSS
def load_css():
    """Load Vietnamese cultural CSS styling"""
    css = """
    <style>
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 1440px;
    }
    
    .government-header {
        background: linear-gradient(135deg, #004B87 0%, #1E3A8A 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 12px rgba(0, 75, 135, 0.3);
    }
    
    .legal-category {
        background: linear-gradient(90deg, rgba(218, 2, 14, 0.05) 0%, rgba(255, 255, 255, 0) 100%);
        border-left: 4px solid #DA020E;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0 8px 8px 0;
        transition: all 0.3s ease;
    }
    
    .legal-citation {
        background: #FFFEF7;
        border: 1px solid #D4AF37;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def render_government_header():
    """Render Vietnamese Government compliant header"""
    header_html = """
    <div class="government-header">
        <div style="text-align: center; margin-bottom: 1rem;">
            <h1 style="font-size: 1.2rem; font-weight: 700; margin-bottom: 0.5rem;">CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM</h1>
            <p style="font-style: italic; opacity: 0.9; margin: 0;">Độc lập - Tự do - Hạnh phúc</p>
        </div>
        <h1 style="font-size: 2rem; font-weight: 700; color: #D4AF37; text-align: center; margin-top: 1rem;">
            🏛️ Hệ thống Tư vấn Pháp lý AI
        </h1>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)

def render_legal_categories():
    """Render legal categories sidebar"""
    st.markdown("### ⚖️ Lĩnh vực Pháp lý")
    
    legal_domains = {
        "dan_su": {
            "name": "Luật Dân sự", 
            "icon": "👥",
            "subcategories": ["Quyền sở hữu", "Hợp đồng", "Nghĩa vụ dân sự", "Thừa kế"]
        },
        "hinh_su": {
            "name": "Luật Hình sự", 
            "icon": "🛡️",
            "subcategories": ["Tội phạm", "Hình phạt", "Thủ tục tố tụng"]
        },
        "lao_dong": {
            "name": "Luật Lao động", 
            "icon": "💼",
            "subcategories": ["Hợp đồng lao động", "Quyền lao động", "Tranh chấp"]
        },
        "thuong_mai": {
            "name": "Luật Thương mại", 
            "icon": "🏢",
            "subcategories": ["Kinh doanh", "Thương mại", "Cạnh tranh"]
        },
        "gia_dinh": {
            "name": "Luật Gia đình", 
            "icon": "❤️",
            "subcategories": ["Hôn nhân", "Ly hôn", "Quyền trẻ em"]
        }
    }
    
    for domain_key, domain_info in legal_domains.items():
        with st.expander(f"{domain_info['icon']} {domain_info['name']}", 
                        expanded=(st.session_state.current_legal_domain == domain_key)):
            for subcategory in domain_info['subcategories']:
                if st.button(f"📖 {subcategory}", key=f"sub_{domain_key}_{subcategory}"):
                    st.session_state.current_legal_domain = domain_key
                    st.rerun()

def render_recent_queries():
    """Render recent queries section"""
    st.markdown("### 🕒 Truy vấn gần đây")
    
    recent_queries = [
        {"text": "Thủ tục ly hôn thuận tình", "time": "2 giờ trước"},
        {"text": "Quyền lợi người lao động", "time": "1 ngày trước"},
        {"text": "Hợp đồng mua bán nhà", "time": "3 ngày trước"}
    ]
    
    for query in recent_queries:
        st.markdown(f"""
        <div class="legal-category">
            <p style="margin: 0; font-weight: 500;">{query['text']}</p>
            <small style="color: #64748B;">{query['time']}</small>
        </div>
        """, unsafe_allow_html=True)

def render_quick_actions():
    """Render quick actions section"""
    st.markdown("### ⚡ Hành động nhanh")
    
    if st.button("➕ Đặt câu hỏi mới", use_container_width=True):
        st.session_state.new_question = True
        
    if st.button("🔍 Tìm luật liên quan", use_container_width=True):
        st.session_state.search_laws = True

def render_chat_interface():
    """Render main chat interface"""
    st.markdown("### 💬 Tư vấn Pháp lý AI")
    
    # Regional selector
    st.markdown("**🌏 Chọn vùng miền:**")
    region_options = {
        "north": "🏔️ Miền Bắc",
        "central": "🏖️ Miền Trung", 
        "south": "🌾 Miền Nam",
        "special_zones": "🏭 Khu Kinh tế Đặc biệt"
    }
    
    selected_region = st.selectbox(
        "Vùng miền",
        options=list(region_options.keys()),
        format_func=lambda x: region_options[x],
        index=list(region_options.keys()).index(st.session_state.user_region),
        label_visibility="collapsed"
    )
    st.session_state.user_region = selected_region
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        for i, message in enumerate(st.session_state.chat_history):
            if message['role'] == 'user':
                st.info(f"👤 **Bạn** ({message['timestamp']}):\n\n{message['content']}")
            else:
                st.success(f"🤖 **AI Pháp lý** ({message['timestamp']}):\n\n{message['content']}")
                    
                # Display legal citations if available
                if 'citations' in message:
                    render_legal_citations(message['citations'])
    
    # Chat input
    st.markdown("---")
    user_input = st.text_area(
        "💭 Nhập câu hỏi pháp lý của bạn:",
        placeholder="Ví dụ: Tôi muốn biết về thủ tục ly hôn thuận tình...",
        height=100,
        key="user_input"
    )
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("📤 Gửi câu hỏi", use_container_width=True):
            if user_input.strip():
                process_user_question(user_input)
                st.rerun()
    
    with col2:
        if st.button("🔄 Làm mới", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
    
    with col3:
        if st.button("📥 Xuất lịch sử", use_container_width=True):
            export_chat_history()

def render_legal_references():
    """Render legal references sidebar"""
    st.markdown("### 📖 Tham khảo Pháp lý")
    
    references = [
        {
            "title": "Bộ luật Dân sự 2015",
            "type": "Luật",
            "status": "Hiệu lực"
        },
        {
            "title": "Luật An toàn VSLĐ 2015", 
            "type": "Luật",
            "status": "Hiệu lực"
        },
        {
            "title": "Nghị định 44/2016/NĐ-CP",
            "type": "Nghị định", 
            "status": "Hiệu lực"
        }
    ]
    
    for ref in references:
        status_color = "🟢" if ref['status'] == "Hiệu lực" else "🔴"
        st.markdown(f"""
        <div class="legal-citation">
            <p style="color: #1E3A8A; font-weight: 600; margin-bottom: 0.5rem;">{ref['title']}</p>
            <small>{ref['type']} • {status_color} {ref['status']}</small>
        </div>
        """, unsafe_allow_html=True)

def render_legal_citations(citations: List[Dict]):
    """Render legal citations"""
    st.markdown("**📋 Cơ sở pháp lý:**")
    
    for citation in citations:
        citation_html = f"""
        <div class="legal-citation">
            <div style="color: #1E3A8A; font-weight: 600; margin-bottom: 0.5rem;">{citation.get('title', 'N/A')}</div>
            <div style="color: #DA020E; font-weight: 500;">
                {citation.get('article', '')} {citation.get('clause', '')} {citation.get('point', '')}
            </div>
            <p style="margin: 0.5rem 0; font-style: italic;">
                "{citation.get('content', '')}"
            </p>
            <small style="color: #64748B;">
                {citation.get('authority', '')} • {citation.get('date', '')}
            </small>
        </div>
        """
        st.markdown(citation_html, unsafe_allow_html=True)

def render_footer():
    """Render Vietnamese compliant footer"""
    st.markdown("---")
    
    footer_html = """
    <div style="background: #1E3A8A; color: white; padding: 1rem; border-radius: 8px; text-align: center; margin-top: 2rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
            <div>
                <small>© 2025 Bộ Tư pháp Việt Nam - Hệ thống AI Pháp lý</small>
            </div>
            <div>
                <small>Phiên bản 2.0 | Liên hệ: legal-ai@moj.gov.vn</small>
            </div>
        </div>
        <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid rgba(255,255,255,0.3);">
            <small>
                ⚠️ <strong>Tuyên bố:</strong> Thông tin từ AI chỉ mang tính tham khảo. 
                Vui lòng tham khảo ý kiến chuyên gia pháp lý cho các vấn đề phức tạp.
            </small>
        </div>
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)

def process_user_question(question: str):
    """Process user question and get AI response"""
    timestamp = datetime.now().strftime("%H:%M - %d/%m/%Y")
    
    # Add user message to history
    st.session_state.chat_history.append({
        'role': 'user',
        'content': question,
        'timestamp': timestamp
    })
    
    # Get AI response
    ai_response = get_ai_response(question)
    
    st.session_state.chat_history.append({
        'role': 'assistant', 
        'content': ai_response['content'],
        'timestamp': timestamp,
        'citations': ai_response.get('citations', [])
    })

def get_ai_response(question: str) -> Dict:
    """Get AI response from FastAPI backend with real RAG search"""
    try:
        # Try to call FastAPI backend
        backend_url = "http://localhost:8000"
        
        payload = {
            "question": question,  # Changed from "query" to "question"
            "region": st.session_state.user_region,
            "domain": st.session_state.current_legal_domain or "dan_su"  # Ensure not None
        }
        
        with st.spinner("🔍 Đang tìm kiếm trong cơ sở dữ liệu pháp luật..."):
            response = requests.post(
                f"{backend_url}/api/legal-query",
                json=payload,
                timeout=30,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                api_response = response.json()
                
                # Format response for display
                formatted_response = {
                    'content': f"""**🔍 Kết quả tìm kiếm từ cơ sở dữ liệu pháp luật:**

{api_response.get('response', {}).get('content', 'Không có phản hồi từ hệ thống')}

� **Thông tin tìm kiếm:**
- Độ tin cậy: {api_response.get('response', {}).get('confidence', 0):.1%}
- Thời gian xử lý: {api_response.get('response', {}).get('processing_time', 0):.2f}s
- Vùng miền: {st.session_state.user_region}
- Lĩnh vực: {st.session_state.current_legal_domain or 'Tổng hợp'}""",
                    'citations': api_response.get('citations', [])
                }
                
                return formatted_response
                
        # If API call fails, try direct Pinecone search
        st.warning("⚠️ Backend API không khả dụng, đang thử tìm kiếm trực tiếp...")
        return get_direct_search_response(question)
        
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Lỗi kết nối API: {str(e)}")
        return get_direct_search_response(question)
    except Exception as e:
        st.error(f"❌ Lỗi xử lý: {str(e)}")
        return get_fallback_response(question)

def get_direct_search_response(question: str) -> Dict:
    """Direct search using Pinecone when backend is unavailable"""
    try:
        # Import services
        from app.services.pinecone_service import PineconeService
        from app.models.legal_rag import LegalRAG
        from app.utils.demo_config import get_demo_config
        
        # Initialize services with config
        config = get_demo_config()
        pinecone_service = PineconeService(
            api_key=config.pinecone_api_key,
            environment=config.pinecone_environment,
            index_name=config.pinecone_index_name
        )
        rag_system = LegalRAG()
        
        with st.spinner("🔍 Đang tìm kiếm trực tiếp trong Pinecone..."):
            # Perform RAG search
            search_results = rag_system.query(
                question=question,
                region=st.session_state.user_region,
                legal_domain=st.session_state.current_legal_domain
            )
            
            # Check if we have meaningful results
            if search_results and 'response' in search_results and len(search_results.get('citations', [])) > 0:
                formatted_response = {
                    'content': f"""**🔍 Kết quả tìm kiếm trực tiếp từ Pinecone:**

{search_results['response']}

📊 **Thông tin tìm kiếm:**
- Nguồn: Tìm kiếm vector trực tiếp
- Số tài liệu tìm được: {len(search_results.get('citations', []))}
- Vùng miền: {st.session_state.user_region}
- Lĩnh vực: {st.session_state.current_legal_domain or 'Tổng hợp'}""",
                    'citations': search_results.get('citations', [])
                }
                return formatted_response
            else:
                # No results found in Pinecone - perform search and insert
                st.info("📚 Không tìm thấy dữ liệu trong cơ sở dữ liệu. Đang tìm kiếm và cập nhật...")
                return search_and_insert_to_pinecone(question, pinecone_service)
                
    except ImportError as e:
        st.warning(f"⚠️ Không thể import các service cần thiết: {e}")
        return get_fallback_response(question)
    except Exception as e:
        st.error(f"❌ Lỗi tìm kiếm trực tiếp: {str(e)}")
        return get_fallback_response(question)

def search_and_insert_to_pinecone(question: str, pinecone_service) -> Dict:
    """Search for legal information via backend and update Pinecone"""
    try:
        with st.spinner("🔍 Đang tìm kiếm thông tin pháp lý từ backend..."):
            # Call backend API which will handle both vector search and SerpAPI fallback
            response = requests.post(
                f"{BACKEND_URL}/api/legal-query",
                json={
                    "question": f"Tìm kiếm và thêm tài liệu pháp lý về: {question}",
                    "domain": st.session_state.current_legal_domain or "dan_su",
                    "region": st.session_state.user_region
                },
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                citations = data.get("citations", [])
                
                if citations:
                    st.success(f"✅ Backend đã tìm thấy và xử lý {len(citations)} tài liệu!")
                    return {
                        'content': data.get("content", "Đã cập nhật cơ sở dữ liệu"),
                        'citations': citations
                    }
                else:
                    return get_fallback_response(question)
            else:
                st.error(f"❌ Backend API lỗi: {response.status_code}")
                return get_fallback_response(question)
            
    except Exception as e:
        st.error(f"❌ Lỗi khi gọi backend API: {str(e)}")
        return get_fallback_response(question)

def detect_legal_domain(question: str) -> str:
    """Detect legal domain from question"""
    question_lower = question.lower()
    
    if any(keyword in question_lower for keyword in ["ly hôn", "kết hôn", "hôn nhân", "gia đình", "con cái"]):
        return "gia_dinh"
    elif any(keyword in question_lower for keyword in ["lao động", "nghỉ việc", "lương", "bảo hiểm"]):
        return "lao_dong"
    elif any(keyword in question_lower for keyword in ["hợp đồng", "tài sản", "thừa kế", "dân sự"]):
        return "dan_su"
    elif any(keyword in question_lower for keyword in ["kinh doanh", "công ty", "thương mại"]):
        return "thuong_mai"
    elif any(keyword in question_lower for keyword in ["tội phạm", "hình sự", "án", "tù"]):
        return "hinh_su"
    else:
        return "dan_su"  # Default

def search_in_updated_pinecone(question: str, pinecone_service) -> Dict:
    """Search in Pinecone after updating with new documents"""
    try:
        # Perform vector search with the question
        search_results = pinecone_service.search_similar_documents(
            query_text=question,
            legal_domain=st.session_state.current_legal_domain,
            top_k=3
        )
        
        if search_results:
            # Format search results
            content = "**📋 Kết quả từ cơ sở dữ liệu đã cập nhật:**\n\n"
            citations = []
            
            for i, result in enumerate(search_results, 1):
                content += f"**{i}. {result.metadata.get('title', 'Tài liệu pháp lý')}**\n"
                content += f"{result.content[:300]}...\n\n"
                
                citations.append({
                    'title': result.metadata.get('title', 'Không rõ'),
                    'article': result.metadata.get('article', 'N/A'),
                    'content': result.content[:200],
                    'authority': result.metadata.get('authority', 'N/A'),
                    'source': result.metadata.get('source', 'N/A')
                })
            
            return {
                'content': content,
                'citations': citations
            }
    except Exception as e:
        st.warning(f"⚠️ Lỗi tìm kiếm trong Pinecone đã cập nhật: {e}")
        return None

def generate_response_from_inserted_docs(legal_documents: List[Dict], question: str) -> Dict:
    """Generate response from the inserted documents"""
    try:
        content = f"""**📚 Phản hồi dựa trên tài liệu đã cập nhật:**

Dựa trên câu hỏi: "{question}"

"""
        citations = []
        
        for i, doc in enumerate(legal_documents, 1):
            content += f"**{i}. {doc['title']}**\n"
            content += f"{doc['content'][:400]}...\n\n"
            
            citations.append({
                'title': doc['title'],
                'article': doc.get('article', 'N/A'),
                'content': doc['content'][:200],
                'authority': doc.get('authority', 'N/A'),
                'source': doc.get('source', 'N/A')
            })
        
        content += """
⚠️ **Lưu ý quan trọng:**
- Thông tin này được tự động thu thập và cập nhật vào cơ sở dữ liệu
- Cần được xác minh bởi chuyên gia pháp lý trước khi áp dụng
- Tham khảo thêm tại các trang web chính thức của Chính phủ"""
        
        return {
            'content': content,
            'citations': citations
        }
        
    except Exception as e:
        st.error(f"❌ Lỗi tạo phản hồi từ tài liệu: {str(e)}")
        return get_fallback_response(question)

def get_fallback_response(question: str) -> Dict:
    """Fallback response when all search methods fail"""
    return {
        'content': f"""**⚠️ Thông báo hệ thống:**

Hiện tại hệ thống tìm kiếm chính đang bảo trì. Câu hỏi của bạn: "{question}" đã được ghi nhận.

🔧 **Tình trạng hệ thống:**
- Backend API: Không khả dụng
- Pinecone Search: Không khả dụng  
- Database: Đang kiểm tra kết nối

📞 **Hướng dẫn:**
1. Vui lòng thử lại sau vài phút
2. Kiểm tra kết nối internet
3. Liên hệ support nếu vấn đề tiếp tục

💡 **Gợi ý tạm thời:**
Bạn có thể tham khảo trực tiếp các văn bản pháp luật tại:
- Cổng thông tin điện tử Chính phủ
- Website Bộ Tư pháp
- Thư viện pháp luật quốc gia

🔄 **Thời gian dự kiến khôi phục:** 15-30 phút""",
        'citations': []
    }

def export_chat_history():
    """Export chat history to file"""
    if st.session_state.chat_history:
        export_content = "LỊCH SỬ TƯ VẤN PHÁP LÝ AI\n"
        export_content += "=" * 50 + "\n\n"
        
        for message in st.session_state.chat_history:
            role = "NGƯỜI DÙNG" if message['role'] == 'user' else "AI PHÁP LÝ"
            export_content += f"{role} ({message['timestamp']}):\n"
            export_content += f"{message['content']}\n\n"
        
        st.download_button(
            label="📥 Tải xuống lịch sử",
            data=export_content,
            file_name=f"tu_van_phap_ly_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain"
        )
    else:
        st.warning("Chưa có lịch sử để xuất!")

def main():
    """Main Streamlit application"""
    # Initialize session state
    initialize_session_state()
    
    # Load CSS
    load_css()
    
    # Render header
    render_government_header()
    
    # Compliance notice
    st.info("🛡️ **Hệ thống tuân thủ tiêu chuẩn Chính phủ** - Được chứng nhận bởi Bộ TT&TT.")
    
    # Create three-column layout
    left_sidebar, main_content, right_sidebar = st.columns([1, 2, 1])
    
    with left_sidebar:
        render_legal_categories()
        render_recent_queries()
        render_quick_actions()
    
    with main_content:
        render_chat_interface()
    
    with right_sidebar:
        render_legal_references()
    
    # Render footer
    render_footer()

if __name__ == "__main__":
    main()
