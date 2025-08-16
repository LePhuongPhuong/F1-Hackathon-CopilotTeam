"""
Vietnamese Legal AI Chatbot
Chatbot AI Pháp lý Việt Nam

Complete chatbot implementation with Vietnamese text processing,
RAG system, and conversational memory.

Triển khai chatbot hoàn chỉnh với xử lý văn bản tiếng Việt,
hệ thống RAG và bộ nhớ hội thoại.
"""

import os
import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
import logging

from app.models.chat_model import OpenAIChatModel
from app.models.legal_rag import VietnameseLegalRAG
from app.utils.text_processing import (
    preprocess_vietnamese_query,
    get_legal_domain,
    extract_legal_citations,
    VietnameseTextProcessor
)
from app.utils.demo_config import demo_settings
from app.services.pinecone_service import PineconeService

# Configure logging
logger = logging.getLogger(__name__)

@dataclass
class ChatMessage:
    """Chat message data structure"""
    id: str
    role: str  # 'user' or 'assistant'
    content: str
    timestamp: datetime
    metadata: Dict[str, Any] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ChatMessage':
        """Create from dictionary"""
        data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        return cls(**data)

@dataclass
class ChatSession:
    """Chat session data structure"""
    session_id: str
    user_id: Optional[str]
    created_at: datetime
    last_activity: datetime
    messages: List[ChatMessage]
    context: Dict[str, Any] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            'session_id': self.session_id,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat(),
            'last_activity': self.last_activity.isoformat(),
            'messages': [msg.to_dict() for msg in self.messages],
            'context': self.context
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ChatSession':
        """Create from dictionary"""
        data['created_at'] = datetime.fromisoformat(data['created_at'])
        data['last_activity'] = datetime.fromisoformat(data['last_activity'])
        data['messages'] = [ChatMessage.from_dict(msg) for msg in data['messages']]
        return cls(**data)

class VietnameseLegalChatbot:
    """Main Vietnamese Legal Chatbot class"""
    
    def __init__(self, 
                 chat_model: Optional[OpenAIChatModel] = None,
                 rag_system: Optional[VietnameseLegalRAG] = None,
                 pinecone_service: Optional[PineconeService] = None):
        """Initialize Vietnamese Legal Chatbot"""
        
        # Initialize components with demo settings - order matters
        self.chat_model = chat_model or OpenAIChatModel(
            api_key=demo_settings.openai_chat_api_key,
            api_base=demo_settings.openai_chat_api_base,
            model=demo_settings.chat_model,
            temperature=demo_settings.temperature,
            max_tokens=demo_settings.max_tokens
        )
        
        self.pinecone_service = pinecone_service or PineconeService(
            api_key=demo_settings.pinecone_api_key,
            environment=demo_settings.pinecone_environment,
            index_name=demo_settings.pinecone_index_name
        )
        
        # Initialize RAG system with required dependencies
        self.rag_system = rag_system or VietnameseLegalRAG(
            pinecone_service=self.pinecone_service,
            chat_model=self.chat_model,
            embedding_api_key=demo_settings.openai_embedding_api_key,
            embedding_api_base=demo_settings.openai_embedding_api_base
        )
        
        self.text_processor = VietnameseTextProcessor()
        
        # Session management
        self.sessions: Dict[str, ChatSession] = {}
        self.session_timeout = timedelta(hours=2)  # 2 hours timeout
        
        # Legal conversation templates
        self.conversation_templates = self._load_conversation_templates()
        
        logger.info("Vietnamese Legal Chatbot initialized successfully")
    
    def _load_conversation_templates(self) -> Dict[str, str]:
        """Load conversation templates for different legal scenarios"""
        return {
            'greeting': """Xin chào! Tôi là trợ lý AI pháp lý của Việt Nam. 
Tôi có thể giúp bạn:
• Tư vấn về các vấn đề pháp lý
• Giải thích các điều luật và quy định
• Hướng dẫn thủ tục hành chính
• Phân tích các tình huống pháp lý

Bạn có câu hỏi gì về pháp luật Việt Nam không?""",
            
            'clarification': """Để tôi có thể tư vấn chính xác hơn, bạn có thể cung cấp thêm thông tin về:
• Tình huống cụ thể bạn đang gặp phải
• Lĩnh vực pháp lý liên quan (dân sự, hình sự, lao động, v.v.)
• Thời gian và địa điểm xảy ra sự việc""",
            
            'legal_disclaimer': """⚠️ **Lưu ý quan trọng**: 
Thông tin tôi cung cấp chỉ mang tính tham khảo, dựa trên pháp luật Việt Nam hiện hành. 
Để có tư vấn chính thức và xử lý vấn đề pháp lý cụ thể, bạn nên tham khảo ý kiến của luật sư có thẩm quyền.""",
            
            'escalation': """Tình huống này có vẻ phức tạp và cần được xem xét kỹ lưỡng. 
Tôi khuyên bạn nên:
• Liên hệ với luật sư chuyên ngành
• Tham khảo tại các trung tâm tư vấn pháp luật
• Liên hệ cơ quan nhà nước có thẩm quyền"""
        }
    
    def create_session(self, user_id: Optional[str] = None) -> str:
        """Create a new chat session"""
        session_id = str(uuid.uuid4())
        now = datetime.now()
        
        # Create greeting message
        greeting_msg = ChatMessage(
            id=str(uuid.uuid4()),
            role='assistant',
            content=self.conversation_templates['greeting'],
            timestamp=now,
            metadata={'type': 'greeting'}
        )
        
        session = ChatSession(
            session_id=session_id,
            user_id=user_id,
            created_at=now,
            last_activity=now,
            messages=[greeting_msg],
            context={'legal_domain': None, 'conversation_state': 'greeting'}
        )
        
        self.sessions[session_id] = session
        logger.info(f"Created new chat session: {session_id}")
        
        return session_id
    
    def get_session(self, session_id: str) -> Optional[ChatSession]:
        """Get chat session by ID"""
        session = self.sessions.get(session_id)
        
        if session:
            # Check if session is expired
            if datetime.now() - session.last_activity > self.session_timeout:
                del self.sessions[session_id]
                logger.info(f"Session {session_id} expired and removed")
                return None
        
        return session
    
    def process_message(self, session_id: str, user_message: str) -> Dict[str, Any]:
        """Process user message and generate response"""
        session = self.get_session(session_id)
        if not session:
            return {
                'error': 'Session not found or expired',
                'session_id': session_id
            }
        
        try:
            # Step 1: Vietnamese text processing
            query_analysis = preprocess_vietnamese_query(user_message)
            legal_domain = get_legal_domain(user_message)
            citations = extract_legal_citations(user_message)
            
            # Step 2: Update session context
            session.context['legal_domain'] = legal_domain
            session.context['last_intent'] = query_analysis['intent']
            session.context['legal_terms'] = query_analysis['legal_terms']
            
            # Step 3: Add user message to session
            user_msg = ChatMessage(
                id=str(uuid.uuid4()),
                role='user',
                content=user_message,
                timestamp=datetime.now(),
                metadata={
                    'intent': query_analysis['intent'],
                    'domain': legal_domain,
                    'legal_terms': query_analysis['legal_terms'],
                    'citations': citations
                }
            )
            session.messages.append(user_msg)
            
            # Step 4: Generate response using RAG
            response_data = self._generate_contextual_response(
                session, user_message, query_analysis
            )
            
            # Step 5: Add assistant message to session
            assistant_msg = ChatMessage(
                id=str(uuid.uuid4()),
                role='assistant',
                content=response_data['content'],
                timestamp=datetime.now(),
                metadata=response_data['metadata']
            )
            session.messages.append(assistant_msg)
            
            # Step 6: Update session activity
            session.last_activity = datetime.now()
            
            return {
                'session_id': session_id,
                'response': response_data['content'],
                'metadata': response_data['metadata'],
                'session_context': session.context
            }
            
        except Exception as e:
            logger.error(f"Error processing message in session {session_id}: {e}")
            return {
                'error': f'Error processing message: {str(e)}',
                'session_id': session_id
            }
    
    def _generate_contextual_response(self, session: ChatSession, 
                                    user_message: str, 
                                    query_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate contextual response using RAG and conversation history"""
        
        # Get conversation context
        conversation_history = self._get_conversation_context(session)
        
        # Use RAG system to get relevant documents
        try:
            rag_result = self.rag_system.query(user_message)
            
            # Build enhanced prompt with Vietnamese context
            enhanced_prompt = self._build_vietnamese_legal_prompt(
                user_message=user_message,
                query_analysis=query_analysis,
                rag_result=rag_result,
                conversation_history=conversation_history,
                session_context=session.context
            )
            
            # Generate response
            response_content = self.chat_model.generate_response(
                prompt=enhanced_prompt,
                context=None  # Context is already in the prompt
            )
            
            # Add legal disclaimer if needed
            if self._should_add_disclaimer(query_analysis):
                response_content += f"\n\n{self.conversation_templates['legal_disclaimer']}"
            
            return {
                'content': response_content,
                'metadata': {
                    'rag_sources': rag_result.sources if hasattr(rag_result, 'sources') else [],
                    'legal_domain': query_analysis.get('legal_domain', 'general'),
                    'intent': query_analysis['intent'],
                    'confidence': getattr(rag_result, 'confidence', 0.0),
                    'response_type': 'rag_enhanced'
                }
            }
            
        except Exception as e:
            logger.warning(f"RAG system failed, using fallback response: {e}")
            
            # Fallback: Use chat model without RAG
            fallback_prompt = self._build_fallback_prompt(user_message, query_analysis)
            response_content = self.chat_model.generate_response(fallback_prompt)
            
            return {
                'content': response_content,
                'metadata': {
                    'response_type': 'fallback',
                    'intent': query_analysis['intent'],
                    'legal_domain': get_legal_domain(user_message)
                }
            }
    
    def _get_conversation_context(self, session: ChatSession, max_messages: int = 6) -> str:
        """Get recent conversation context"""
        if len(session.messages) <= 1:  # Only greeting message
            return ""
        
        # Get last few messages (excluding current)
        recent_messages = session.messages[-max_messages:-1] if len(session.messages) > 1 else []
        
        context_parts = []
        for msg in recent_messages:
            role_label = "Người dùng" if msg.role == 'user' else "Trợ lý AI"
            context_parts.append(f"{role_label}: {msg.content}")
        
        return "\n".join(context_parts)
    
    def _build_vietnamese_legal_prompt(self, 
                                     user_message: str,
                                     query_analysis: Dict[str, Any],
                                     rag_result: Any,
                                     conversation_history: str,
                                     session_context: Dict[str, Any]) -> str:
        """Build enhanced prompt for Vietnamese legal consultation"""
        
        domain_context = {
            'dan_su': 'dân sự (hợp đồng, tài sản, quyền sở hữu)',
            'hinh_su': 'hình sự (tội phạm, hình phạt, điều tra)',
            'lao_dong': 'lao động (hợp đồng lao động, quyền người lao động)',
            'thuong_mai': 'thương mại (kinh doanh, doanh nghiệp)',
            'hanh_chinh': 'hành chính (thủ tục, giấy phép, cơ quan nhà nước)'
        }
        
        legal_domain = session_context.get('legal_domain', 'general')
        domain_expertise = domain_context.get(legal_domain, 'pháp luật Việt Nam')
        
        prompt_parts = [
            f"Bạn là chuyên gia tư vấn pháp lý Việt Nam với chuyên môn sâu về lĩnh vực {domain_expertise}.",
            f"Ý định người dùng: {query_analysis['intent']}",
        ]
        
        # Add conversation context if available
        if conversation_history:
            prompt_parts.append(f"Ngữ cảnh cuộc trò chuyện trước:\n{conversation_history}")
        
        # Add RAG context if available
        if hasattr(rag_result, 'answer') and rag_result.answer:
            prompt_parts.append(f"Thông tin pháp lý liên quan:\n{rag_result.answer}")
        
        # Add legal terms context
        if query_analysis.get('legal_terms'):
            terms_str = ', '.join(query_analysis['legal_terms'])
            prompt_parts.append(f"Thuật ngữ pháp lý được phát hiện: {terms_str}")
        
        # Add main query
        prompt_parts.extend([
            f"Câu hỏi của người dùng: {user_message}",
            "",
            "Hãy trả lời một cách:",
            "• Chính xác dựa trên pháp luật Việt Nam",
            "• Dễ hiểu cho người dân",
            "• Có trích dẫn điều luật cụ thể (nếu có)",
            "• Thực tế và hữu ích",
            "• Bằng tiếng Việt trang trọng nhưng thân thiện",
            "",
            "Trả lời:"
        ])
        
        return "\n".join(prompt_parts)
    
    def _build_fallback_prompt(self, user_message: str, query_analysis: Dict[str, Any]) -> str:
        """Build fallback prompt when RAG is not available"""
        return f"""Bạn là chuyên gia tư vấn pháp lý Việt Nam.

Câu hỏi: {user_message}
Ý định: {query_analysis['intent']}

Hãy trả lời dựa trên kiến thức về pháp luật Việt Nam, ngắn gọn và chính xác.
Nếu không chắc chắn, hãy khuyên người dùng tham khảo chuyên gia pháp lý.

Trả lời bằng tiếng Việt:"""
    
    def _should_add_disclaimer(self, query_analysis: Dict[str, Any]) -> bool:
        """Determine if legal disclaimer should be added"""
        sensitive_intents = ['violation_inquiry', 'procedure_inquiry', 'obligation_inquiry']
        return query_analysis['intent'] in sensitive_intents
    
    def get_session_history(self, session_id: str) -> Dict[str, Any]:
        """Get session conversation history"""
        session = self.get_session(session_id)
        if not session:
            return {'error': 'Session not found or expired'}
        
        return {
            'session_id': session_id,
            'created_at': session.created_at.isoformat(),
            'last_activity': session.last_activity.isoformat(),
            'message_count': len(session.messages),
            'messages': [msg.to_dict() for msg in session.messages],
            'context': session.context
        }
    
    def clear_session(self, session_id: str) -> bool:
        """Clear/delete a chat session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            logger.info(f"Cleared session: {session_id}")
            return True
        return False
    
    def cleanup_expired_sessions(self) -> int:
        """Clean up expired sessions"""
        now = datetime.now()
        expired_sessions = []
        
        for session_id, session in self.sessions.items():
            if now - session.last_activity > self.session_timeout:
                expired_sessions.append(session_id)
        
        for session_id in expired_sessions:
            del self.sessions[session_id]
        
        if expired_sessions:
            logger.info(f"Cleaned up {len(expired_sessions)} expired sessions")
        
        return len(expired_sessions)
    
    def get_chat_statistics(self) -> Dict[str, Any]:
        """Get chatbot usage statistics"""
        if not self.sessions:
            return {
                'active_sessions': 0,
                'total_messages': 0,
                'avg_messages_per_session': 0,
                'most_common_domain': None,
                'most_common_intent': None
            }
        
        total_messages = sum(len(session.messages) for session in self.sessions.values())
        avg_messages = total_messages / len(self.sessions) if self.sessions else 0
        
        # Analyze domains and intents
        domains = []
        intents = []
        
        for session in self.sessions.values():
            if session.context.get('legal_domain'):
                domains.append(session.context['legal_domain'])
            for msg in session.messages:
                if msg.metadata and msg.metadata.get('intent'):
                    intents.append(msg.metadata['intent'])
        
        most_common_domain = max(set(domains), key=domains.count) if domains else None
        most_common_intent = max(set(intents), key=intents.count) if intents else None
        
        return {
            'active_sessions': len(self.sessions),
            'total_messages': total_messages,
            'avg_messages_per_session': round(avg_messages, 2),
            'most_common_domain': most_common_domain,
            'most_common_intent': most_common_intent,
            'session_timeout_hours': self.session_timeout.total_seconds() / 3600
        }

# Utility functions for external use
def create_vietnamese_legal_chatbot() -> VietnameseLegalChatbot:
    """Create a Vietnamese Legal Chatbot instance"""
    return VietnameseLegalChatbot()

def quick_legal_query(question: str) -> str:
    """Quick one-off legal query without session management"""
    chatbot = create_vietnamese_legal_chatbot()
    session_id = chatbot.create_session()
    
    result = chatbot.process_message(session_id, question)
    chatbot.clear_session(session_id)
    
    if 'error' in result:
        return f"Error: {result['error']}"
    
    return result['response']
