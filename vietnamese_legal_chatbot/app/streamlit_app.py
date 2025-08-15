"""
Streamlit Frontend for Vietnamese Legal AI Chatbot
Frontend Streamlit cho Chatbot AI Pháp lý Việt Nam

Interactive web interface for Vietnamese legal consultation.
Giao diện web tương tác cho tư vấn pháp lý Việt Nam.
"""

import streamlit as st
import requests
import json
import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional
import base64
import io
from pathlib import Path

# Custom CSS for Vietnamese Cultural Design
def load_css():
    """Load Vietnamese cultural CSS styling"""
    css = """
    <style>
    /* Import Vietnamese-optimized fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Vietnamese Cultural Color Palette */
    :root {
        --vn-red-primary: #DA020E;
        --vn-yellow-gold: #FFDF00;
        --vn-blue-government: #004B87;
        --vn-green-nature: #228B22;
        --vn-lotus-pink: #FDB5C8;
        --vn-bamboo-green: #9CAF88;
        --vn-legal-navy: #1E3A8A;
        --vn-justice-gold: #D4AF37;
        --vn-peace-white: #FFFEF7;
    }
    
    /* Main App Styling */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 1440px;
    }
    
    /* Vietnamese Government Header */
    .government-header {
        background: linear-gradient(135deg, var(--vn-blue-government) 0%, var(--vn-legal-navy) 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 12px rgba(0, 75, 135, 0.3);
    }
    
    .national-identity {
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .country-name {
        font-size: 1.2rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        margin-bottom: 0.5rem;
    }
    
    .national-motto {
        font-size: 1rem;
        font-style: italic;
        opacity: 0.9;
    }
    
    .system-title {
        font-size: 2rem;
        font-weight: 700;
        color: var(--vn-justice-gold);
        text-align: center;
        margin-top: 1rem;
    }
    
    /* Legal Categories Styling */
    .legal-category {
        background: linear-gradient(90deg, rgba(218, 2, 14, 0.05) 0%, rgba(255, 255, 255, 0) 100%);
        border-left: 4px solid var(--vn-red-primary);
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0 8px 8px 0;
        transition: all 0.3s ease;
    }
    
    .legal-category:hover {
        background: linear-gradient(90deg, rgba(218, 2, 14, 0.1) 0%, rgba(255, 255, 255, 0) 100%);
        transform: translateX(5px);
    }
    
    /* Chat Message Styling */
    .chat-message {
        background: white;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 10px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .user-message {
        background: linear-gradient(135deg, #F0F9FF 0%, #E0F2FE 100%);
        border-left: 4px solid var(--vn-blue-government);
    }
    
    .ai-message {
        background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%);
        border-left: 4px solid var(--vn-green-nature);
    }
    
    /* Legal Citation Styling */
    .legal-citation {
        background: var(--vn-peace-white);
        border: 1px solid var(--vn-justice-gold);
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .document-title {
        color: var(--vn-legal-navy);
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }
    
    .article-reference {
        color: var(--vn-red-primary);
        font-weight: 500;
    }
    
    /* Vietnamese Typography */
    .vietnamese-text {
        font-family: 'Inter', 'Segoe UI', sans-serif;
        line-height: 1.7;
        letter-spacing: 0.01em;
        word-spacing: 0.02em;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def main():
    """Main Streamlit application with Vietnamese localization"""
    
    # Page configuration
    st.set_page_config(
        page_title="Chatbot AI Pháp lý Việt Nam",
        page_icon="⚖️",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://legal.gov.vn/help',
            'Report a bug': 'https://legal.gov.vn/report',
            'About': "Hệ thống Tư vấn Pháp lý AI - Phiên bản 2.0"
        }
    )
    
    # Load Vietnamese cultural CSS
    load_css()
    
    # Render Vietnamese Government Header
    render_government_header()
    
    # Create three-column layout (matching design mockups)
    left_sidebar, main_content, right_sidebar = st.columns([1, 2, 1])
    
    with left_sidebar:
        render_legal_categories()
        render_recent_queries()
        render_quick_actions()
    
    with main_content:
        render_chat_interface()
    
    with right_sidebar:
        render_document_library()
        render_legal_references()
    
    # Render footer
    render_footer()

def render_government_header():
    """Render Vietnamese Government compliant header"""
    header_html = """
    <div class="government-header">
        <div class="national-identity">
            <h1 class="country-name">CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM</h1>
            <p class="national-motto">Độc lập - Tự do - Hạnh phúc</p>
        </div>
        <div class="authority-section">
            <h2 style="text-align: center; margin: 0.5rem 0; font-size: 1.3rem;">BỘ TƯ PHÁP</h2>
            <p style="text-align: center; margin: 0; opacity: 0.9;">Cục Pháp chế</p>
        </div>
        <h1 class="system-title">🏛️ Hệ thống Tư vấn Pháp lý AI</h1>
        <p style="text-align: center; color: var(--vn-justice-gold); margin-top: 0.5rem;">
            Phiên bản 2.0 - Năm 2025
        </p>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)
    
    # Compliance notice
    st.info("🛡️ **Hệ thống tuân thủ tiêu chuẩn Chính phủ** - Được chứng nhận bởi Bộ TT&TT theo Thông tư 20/2018/TT-BTTTT về an toàn thông tin mạng quốc gia.")

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
            "subcategories": ["Hợp đồng lao động", "Quyền lao động", "Tranh chấp", "Bảo hiểm XH"]
        },
        "thuong_mai": {
            "name": "Luật Thương mại", 
            "icon": "🏢",
            "subcategories": ["Kinh doanh", "Thương mại", "Cạnh tranh"]
        },
        "gia_dinh": {
            "name": "Luật Gia đình", 
            "icon": "❤️",
            "subcategories": ["Hôn nhân", "Ly hôn", "Quyền trẻ em", "Nhận con nuôi"]
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
    
    if st.button("📜 Xem tất cả lịch sử"):
        st.session_state.show_history = True

def render_quick_actions():
    """Render quick actions section"""
    st.markdown("### ⚡ Hành động nhanh")
    
    if st.button("➕ Đặt câu hỏi mới", use_container_width=True):
        st.session_state.new_question = True
        
    if st.button("📤 Tải lên tài liệu", use_container_width=True):
        st.session_state.upload_document = True
        
    if st.button("🔍 Tìm luật liên quan", use_container_width=True):
        st.session_state.search_laws = True

def render_chat_interface():
    """Render main chat interface with Vietnamese styling"""
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
                st.markdown(f"""
                <div class="chat-message user-message vietnamese-text">
                    <strong>👤 Bạn:</strong><br>
                    {message['content']}
                    <br><small style="color: #64748B;">{message['timestamp']}</small>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message ai-message vietnamese-text">
                    <strong>🤖 AI Pháp lý:</strong><br>
                    {message['content']}
                    <br><small style="color: #64748B;">{message['timestamp']}</small>
                </div>
                """, unsafe_allow_html=True)
                
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

def render_document_library():
    """Render document library sidebar"""
    st.markdown("### 📚 Thư viện Tài liệu")
    
    # Document upload
    uploaded_file = st.file_uploader(
        "Tải lên tài liệu",
        type=['pdf', 'docx', 'txt'],
        help="Hỗ trợ PDF, DOCX, TXT"
    )
    
    if uploaded_file:
        st.success(f"✅ Đã tải lên: {uploaded_file.name}")
        if st.button("🔍 Phân tích tài liệu"):
            analyze_document(uploaded_file)
    
    # Recent documents
    st.markdown("**📋 Tài liệu gần đây:**")
    recent_docs = [
        "Luật Dân sự 2015.pdf",
        "Nghị định 44-2016.docx", 
        "Thông tư 15-2016.pdf"
    ]
    
    for doc in recent_docs:
        if st.button(f"📄 {doc}", key=f"doc_{doc}"):
            st.info(f"Đang mở {doc}...")

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
            "title": "Luật An toàn VSLD 2015", 
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
            <p class="document-title">{ref['title']}</p>
            <small>{ref['type']} • {status_color} {ref['status']}</small>
        </div>
        """, unsafe_allow_html=True)

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

def render_legal_citations(citations: List[Dict]):
    """Render legal citations with Vietnamese formatting"""
    st.markdown("**📋 Cơ sở pháp lý:**")
    
    for citation in citations:
        citation_html = f"""
        <div class="legal-citation">
            <div class="document-title">{citation.get('title', 'N/A')}</div>
            <div class="article-reference">
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

def process_user_question(question: str):
    """Process user question and get AI response"""
    timestamp = datetime.now().strftime("%H:%M - %d/%m/%Y")
    
    # Add user message to history
    st.session_state.chat_history.append({
        'role': 'user',
        'content': question,
        'timestamp': timestamp
    })
    
    # Simulate AI response (replace with actual API call)
    ai_response = get_ai_response(question)
    
    st.session_state.chat_history.append({
        'role': 'assistant', 
        'content': ai_response['content'],
        'timestamp': timestamp,
        'citations': ai_response.get('citations', [])
    })

def get_ai_response(question: str) -> Dict:
    """Get AI response from FastAPI backend"""
    # TODO: Replace with actual API call to FastAPI backend
    
    # Simulated response for demo
    demo_response = {
        'content': f"""
        Dựa trên câu hỏi của bạn: "{question}"
        
        🔍 **Phân tích pháp lý:**
        Theo quy định của pháp luật Việt Nam hiện hành, tôi xin cung cấp thông tin như sau:
        
        📋 **Cơ sở pháp lý chính:**
        - Bộ luật Dân sự 2015
        - Luật Hôn nhân và Gia đình 2014
        
        ⚖️ **Hướng dẫn cụ thể:**
        1. Cần tuân thủ các thủ tục theo quy định
        2. Chuẩn bị đầy đủ hồ sơ cần thiết
        3. Nộp hồ sơ tại cơ quan có thẩm quyền
        
        ⚠️ **Lưu ý quan trọng:**
        Đây là thông tin tham khảo. Khuyến nghị tham khảo luật sư cho tư vấn chuyên sâu.
        """,
        'citations': [
            {
                'title': 'Bộ luật Dân sự số 91/2015/QH13',
                'article': 'Điều 15',
                'clause': 'Khoản 1',
                'content': 'Mọi người đều có quyền bình đẳng trong việc hưởng quyền dân sự...',
                'authority': 'Quốc hội',
                'date': '24/11/2015'
            }
        ]
    }
    
    return demo_response

def analyze_document(uploaded_file):
    """Analyze uploaded document"""
    st.info("🔄 Đang phân tích tài liệu...")
    # TODO: Implement document analysis
    st.success("✅ Phân tích hoàn tất!")

def export_chat_history():
    """Export chat history to file"""
    if st.session_state.chat_history:
        # Create export content
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

def render_sidebar():
    """Render sidebar with legal domains and options"""
    # TODO: Implement sidebar
    pass

def render_document_upload():
    """Render document upload component"""
    # TODO: Implement document upload
    pass

def render_chat_history():
    """Render chat history panel"""
    # TODO: Implement chat history
    pass

def render_export_options():
    """Render export functionality"""
    # TODO: Implement export options
    pass

if __name__ == "__main__":
    main()
