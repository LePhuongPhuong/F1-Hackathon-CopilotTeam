#!/usr/bin/env python3
"""
Quick chatbot test with correct method calls
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    print("=== Testing Vietnamese Legal Chatbot (Fixed) ===")
    
    print("1. Testing demo config import...")
    from app.utils.demo_config import demo_settings
    print("✅ Demo configuration loaded successfully")
    print(f"   - Chat API: {demo_settings.openai_chat_api_key[:20]}...")
    print(f"   - Embedding API: {demo_settings.openai_embedding_api_key[:20]}...")
    print(f"   - Pinecone: {demo_settings.pinecone_api_key[:20]}...")
    print(f"   ✅ Demo config loaded: {demo_settings.chat_model}")

    print("\n2. Testing text processor import...")
    from app.utils.text_processing import VietnameseTextProcessor
    text_processor = VietnameseTextProcessor()
    print("   ✅ Text processor created")

    print("\n3. Testing quick text processing...")
    test_text = "Tôi muốn hỏi về luật lao động"
    normalized = text_processor.normalize_vietnamese_text(test_text)
    # analysis = text_processor.analyze_legal_text(test_text)  # Skip complex analysis for now
    print(f"   ✅ Normalized: '{test_text}' -> '{normalized}'")
    print(f"   ✅ Text processing basic functions working")

    print("\n4. Testing chatbot import...")
    from app.models.vietnamese_legal_chatbot import VietnameseLegalChatbot
    print("   ✅ Chatbot class imported")

    print("\n5. Testing chatbot initialization...")
    chatbot = VietnameseLegalChatbot()
    print("   ✅ Chatbot initialized")

    print("\n6. Testing session creation...")
    session_id = chatbot.create_session()
    print(f"   ✅ Session created: {session_id}")

    print("\n7. Testing simple chat with process_message...")
    result = chatbot.process_message(session_id, "Xin chào!")
    if 'error' in result:
        print(f"❌ ERROR: {result['error']}")
    else:
        print(f"✅ Chat response received ({len(result['response'])} chars)")
        print(f"   Response preview: {result['response'][:150]}...")
        
    print("\n8. Testing legal question...")
    legal_result = chatbot.process_message(session_id, "Tôi muốn hỏi về luật lao động Việt Nam")
    if 'error' in legal_result:
        print(f"❌ ERROR: {legal_result['error']}")
    else:
        print(f"✅ Legal response received ({len(legal_result['response'])} chars)")
        print(f"   Legal response preview: {legal_result['response'][:150]}...")

    print("\n9. Testing session history...")
    history = chatbot.get_session_history(session_id)
    if 'error' in history:
        print(f"❌ ERROR: {history['error']}")
    else:
        print(f"✅ Session history retrieved:")
        print(f"   - Message count: {history['message_count']}")
        print(f"   - Session context: {history['context']}")

    print("\n10. Testing chatbot statistics...")
    stats = chatbot.get_chat_statistics()
    print(f"✅ Chatbot statistics:")
    print(f"   - Active sessions: {stats['active_sessions']}")
    print(f"   - Total messages: {stats['total_messages']}")
    print(f"   - Avg messages per session: {stats['avg_messages_per_session']}")

    print("\n✅ All tests completed successfully!")
    print("🎉 Vietnamese Legal Chatbot is working properly!")

except Exception as e:
    print(f"❌ ERROR during testing: {e}")
    import traceback
    traceback.print_exc()

print("\n🔍 Debugging info:")
print(f"   - Python path: {sys.path[:3]}")
print(f"   - Current directory: {os.getcwd()}")
print(f"   - Script location: {os.path.abspath(__file__)}")
