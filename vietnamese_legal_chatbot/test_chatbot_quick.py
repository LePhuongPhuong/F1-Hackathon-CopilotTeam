"""
Quick test cho Vietnamese Legal Chatbot
Test nhanh chatbot với demo config
"""

import sys
import os

# Add project paths
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app'))

print("=== Testing Vietnamese Legal Chatbot ===")

try:
    print("1. Testing demo config import...")
    from app.utils.demo_config import demo_settings
    print(f"   ✅ Demo config loaded: {demo_settings.chat_model}")
    
    print("\n2. Testing text processor import...")
    from app.utils.text_processing import VietnameseTextProcessor
    processor = VietnameseTextProcessor()
    print(f"   ✅ Text processor created")
    
    print("\n3. Testing quick text processing...")
    test_query = "Tôi muốn hỏi về luật lao động"
    processed = processor.normalize_vietnamese_text(test_query)
    print(f"   ✅ Normalized: '{test_query}' -> '{processed}'")
    
    # Test legal text analysis
    analysis = processor.process_legal_text(test_query)
    print(f"   ✅ Legal analysis completed:")
    print(f"      - Legal terms: {len(analysis.legal_terms)}")
    print(f"      - Entities: {len(analysis.entities)}")
    print(f"      - Language confidence: {analysis.language_confidence}")
    
    print("\n4. Testing chatbot import...")
    from app.models.vietnamese_legal_chatbot import VietnameseLegalChatbot
    print(f"   ✅ Chatbot class imported")
    
    print("\n5. Testing chatbot initialization...")
    chatbot = VietnameseLegalChatbot()
    print(f"   ✅ Chatbot initialized")
    
    print("\n6. Testing session creation...")
    session_id = chatbot.create_session()
    print(f"   ✅ Session created: {session_id}")
    
    print("\n7. Testing simple chat...")
    response = chatbot.chat(session_id, "Xin chào!")
    print(f"   ✅ Chat response:")
    print(f"      Query: 'Xin chào!'")
    print(f"      Response: {response[:100]}...")
    
    print("\n8. Testing legal query...")
    legal_response = chatbot.chat(session_id, "Tôi muốn hỏi về luật lao động")
    print(f"   ✅ Legal chat response:")
    print(f"      Query: 'Tôi muốn hỏi về luật lao động'")
    print(f"      Response: {legal_response[:100]}...")
    
    print("\n9. Testing session info...")
    session_info = chatbot.get_session_info(session_id)
    print(f"   ✅ Session info: {len(session_info.get('messages', []))} messages")
    
    print("\n🎉 ALL TESTS PASSED! Vietnamese Legal Chatbot is working!")
    
except Exception as e:
    print(f"\n❌ ERROR during testing: {e}")
    import traceback
    traceback.print_exc()
    
    print("\n🔍 Debugging info:")
    print(f"   - Python path: {sys.path[:3]}")
    print(f"   - Current directory: {os.getcwd()}")
    print(f"   - Script location: {__file__}")
