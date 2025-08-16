"""
Vietnamese Legal Chatbot Demo
Demo Chatbot AI Pháp lý Việt Nam

Interactive demo showing chatbot capabilities with session management,
Vietnamese text processing, and conversational context.
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
load_dotenv()

from app.models.vietnamese_legal_chatbot import (
    VietnameseLegalChatbot, 
    create_vietnamese_legal_chatbot,
    quick_legal_query
)

def run_interactive_chatbot_demo():
    """Run interactive chatbot demo"""
    
    print("🇻🇳 VIETNAMESE LEGAL AI CHATBOT DEMO")
    print("=" * 60)
    print("🤖 Demo Chatbot AI Pháp lý Việt Nam")
    print("=" * 60)
    print(f"🕒 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    try:
        # Initialize chatbot
        print("🔧 Initializing Vietnamese Legal Chatbot...")
        chatbot = create_vietnamese_legal_chatbot()
        print("✅ Chatbot initialized successfully!")
        
        # Create session
        print("🆕 Creating new chat session...")
        session_id = chatbot.create_session(user_id="demo_user")
        print(f"✅ Session created: {session_id[:8]}...")
        
        # Get initial greeting
        session = chatbot.get_session(session_id)
        if session and session.messages:
            print(f"\n🤖 Chatbot: {session.messages[0].content}")
        
        # Interactive conversation loop
        print(f"\n{'='*60}")
        print("💬 INTERACTIVE CONVERSATION")
        print("Type 'exit' to quit, 'stats' for statistics, 'history' for chat history")
        print("=" * 60)
        
        while True:
            try:
                # Get user input
                user_input = input("\n👤 You: ").strip()
                
                if user_input.lower() == 'exit':
                    print("👋 Goodbye! Tạm biệt!")
                    break
                
                elif user_input.lower() == 'stats':
                    stats = chatbot.get_chat_statistics()
                    print(f"\n📊 CHATBOT STATISTICS:")
                    for key, value in stats.items():
                        print(f"   • {key}: {value}")
                    continue
                
                elif user_input.lower() == 'history':
                    history = chatbot.get_session_history(session_id)
                    print(f"\n📜 CHAT HISTORY:")
                    print(f"   • Messages: {history['message_count']}")
                    print(f"   • Domain: {history['context'].get('legal_domain', 'Not detected')}")
                    print(f"   • Last Intent: {history['context'].get('last_intent', 'None')}")
                    continue
                
                elif not user_input:
                    print("❓ Please enter a legal question or 'exit' to quit.")
                    continue
                
                # Process message
                print("🔄 Processing your question...")
                result = chatbot.process_message(session_id, user_input)
                
                if 'error' in result:
                    print(f"❌ Error: {result['error']}")
                    continue
                
                # Display response
                print(f"\n🤖 Chatbot: {result['response']}")
                
                # Display metadata
                metadata = result.get('metadata', {})
                if metadata:
                    print(f"\n📋 Analysis:")
                    print(f"   • Domain: {metadata.get('legal_domain', 'Unknown')}")
                    print(f"   • Intent: {metadata.get('intent', 'Unknown')}")
                    print(f"   • Response Type: {metadata.get('response_type', 'Unknown')}")
                    if metadata.get('rag_sources'):
                        print(f"   • Sources: {len(metadata['rag_sources'])} legal documents")
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye! Tạm biệt!")
                break
            except Exception as e:
                print(f"❌ Error in conversation: {e}")
                continue
        
        # Cleanup
        chatbot.clear_session(session_id)
        print("🧹 Session cleaned up")
        
    except Exception as e:
        print(f"❌ Failed to initialize chatbot: {e}")
        import traceback
        traceback.print_exc()

def run_predefined_conversation_demo():
    """Run demo with predefined conversation scenarios"""
    
    print("\n🎭 PREDEFINED CONVERSATION SCENARIOS")
    print("=" * 60)
    
    # Test scenarios
    test_scenarios = [
        {
            "name": "Dân sự - Quyền sở hữu",
            "messages": [
                "Quyền sở hữu tài sản được quy định như thế nào?",
                "Tôi có thể bán nhà đất mà không cần sự đồng ý của vợ không?",
                "Nếu có tranh chấp về quyền sở hữu thì phải làm gì?"
            ]
        },
        {
            "name": "Lao động - Thời gian làm việc", 
            "messages": [
                "Thời gian làm việc theo luật lao động là bao lâu?",
                "Công ty bắt tôi làm thêm giờ mà không trả lương có được không?",
                "Tôi có quyền từ chối làm thêm giờ không?"
            ]
        },
        {
            "name": "Hành chính - Thủ tục đăng ký",
            "messages": [
                "Thủ tục đăng ký kết hôn cần những giấy tờ gì?",
                "Mất bao lâu để hoàn thành thủ tục?",
                "Phí đăng ký kết hôn là bao nhiều?"
            ]
        }
    ]
    
    try:
        chatbot = create_vietnamese_legal_chatbot()
        
        for i, scenario in enumerate(test_scenarios, 1):
            print(f"\n📋 SCENARIO {i}: {scenario['name']}")
            print("-" * 50)
            
            # Create session for this scenario
            session_id = chatbot.create_session(user_id=f"scenario_{i}")
            
            # Skip initial greeting and start conversation
            for j, message in enumerate(scenario['messages'], 1):
                print(f"\n👤 User Message {j}: {message}")
                
                result = chatbot.process_message(session_id, message)
                
                if 'error' in result:
                    print(f"❌ Error: {result['error']}")
                    continue
                
                # Show response (truncated for demo)
                response = result['response']
                if len(response) > 200:
                    response = response[:200] + "..."
                
                print(f"🤖 Response: {response}")
                
                # Show analysis
                metadata = result.get('metadata', {})
                print(f"📊 Analysis: Domain={metadata.get('legal_domain')} | Intent={metadata.get('intent')}")
            
            # Clean up scenario session
            chatbot.clear_session(session_id)
            print(f"✅ Scenario {i} completed")
        
        # Show final statistics
        final_stats = chatbot.get_chat_statistics()
        print(f"\n📈 DEMO STATISTICS:")
        for key, value in final_stats.items():
            print(f"   • {key}: {value}")
            
    except Exception as e:
        print(f"❌ Error in predefined demo: {e}")
        import traceback
        traceback.print_exc()

def test_quick_query():
    """Test quick query function"""
    print("\n⚡ QUICK QUERY TEST")
    print("=" * 40)
    
    test_questions = [
        "Quyền dân sự là gì?",
        "Thời gian làm việc tối đa là bao lâu?",
        "Thủ tục ly hôn như thế nào?"
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n❓ Question {i}: {question}")
        print("🔄 Processing...")
        
        try:
            answer = quick_legal_query(question)
            # Truncate for demo display
            if len(answer) > 300:
                answer = answer[:300] + "..."
            print(f"💡 Answer: {answer}")
        except Exception as e:
            print(f"❌ Error: {e}")

def main():
    """Main demo function"""
    print("🚀 STARTING VIETNAMESE LEGAL CHATBOT DEMOS")
    print("=" * 60)
    
    # Test 1: Quick queries
    test_quick_query()
    
    # Test 2: Predefined scenarios  
    run_predefined_conversation_demo()
    
    # Test 3: Interactive mode (optional)
    print(f"\n{'='*60}")
    choice = input("Do you want to try interactive mode? (y/n): ").lower()
    if choice == 'y':
        run_interactive_chatbot_demo()
    
    print(f"\n{'='*60}")
    print("🎉 All demos completed successfully!")
    print("✅ Vietnamese Legal Chatbot is ready for production!")

if __name__ == "__main__":
    main()
