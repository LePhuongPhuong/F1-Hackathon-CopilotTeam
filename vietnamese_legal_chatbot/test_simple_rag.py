"""
Simple Vietnamese Legal RAG Demo
With working text-embedding-3-small configuration
"""

import os
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

def test_simple_rag():
    """Test simple RAG functionality with actual API"""
    
    print("🇻🇳 VIETNAMESE LEGAL AI - SIMPLE RAG TEST")
    print("=" * 60)
    print(f"🕒 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Load settings
    embedding_model = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    chat_model = os.getenv("CHAT_MODEL", "gpt-4o-mini")
    
    print(f"� Using embedding model: {embedding_model}")
    print(f"🤖 Using chat model: {chat_model}")
    
    # Get API keys
    chat_api_key = os.getenv("OPENAI_API_KEY")
    embedding_api_key = os.getenv("OPENAI_EMBEDDING_API_KEY")
    chat_api_base = os.getenv("OPENAI_API_BASE")
    embedding_api_base = os.getenv("OPENAI_EMBEDDING_API_BASE")
    
    print(f"🔑 Chat API Key: {chat_api_key[:8]}..." if chat_api_key else "❌ No chat API key")
    print(f"🔑 Embedding API Key: {embedding_api_key[:8]}..." if embedding_api_key else "❌ No embedding API key")
    
    # Test queries
    test_queries = [
        "Quyền dân sự của công dân được bảo vệ như thế nào?",
        "Thời gian làm việc theo quy định pháp luật là bao lâu?"
    ]
    
    # Mock legal documents (Vietnamese legal content)
    mock_docs = [
        {
            "content": "Luật Dân sự 2015 quy định về quyền và nghĩa vụ của công dân. Điều 15 quy định quyền dân sự được bảo vệ bởi pháp luật. Nhà nước có trách nhiệm thừa nhận, tôn trọng và bảo vệ quyền dân sự của công dân.",
            "metadata": {"law": "Luật Dân sự 2015", "article": "Điều 15"}
        },
        {
            "content": "Bộ luật Lao động 2019 quy định thời gian làm việc không quá 8 giờ trong 1 ngày và không quá 48 giờ trong 1 tuần. Người lao động có quyền nghỉ ngơi và được trả lương khi làm thêm giờ.",
            "metadata": {"law": "Bộ luật Lao động 2019", "article": "Điều 20"}
        }
    ]
    
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
        
        print("✅ OpenAI clients created successfully")
        
        # Process each query
        for i, query in enumerate(test_queries, 1):
            print(f"\n{'='*60}")
            print(f"📋 QUERY {i}: {query}")
            print(f"{'='*60}")
            
            # Step 1: Create query embedding
            print("🔍 Step 1: Creating query embedding...")
            query_response = embedding_client.embeddings.create(
                model=embedding_model,
                input=query
            )
            query_embedding = query_response.data[0].embedding
            print(f"✅ Query embedding created (dimension: {len(query_embedding)})")
            
            # Step 2: Create document embeddings and find similarity
            print("📚 Step 2: Processing documents...")
            best_doc = None
            best_similarity = -1
            
            for doc in mock_docs:
                doc_response = embedding_client.embeddings.create(
                    model=embedding_model,
                    input=doc["content"]
                )
                doc_embedding = doc_response.data[0].embedding
                
                # Simple cosine similarity
                dot_product = sum(a * b for a, b in zip(query_embedding, doc_embedding))
                similarity = dot_product / (sum(a*a for a in query_embedding)**0.5 * sum(b*b for b in doc_embedding)**0.5)
                
                print(f"📄 Document similarity: {similarity:.3f} - {doc['metadata']['law']}")
                
                if similarity > best_similarity:
                    best_similarity = similarity
                    best_doc = doc
            
            print(f"🎯 Best match: {best_doc['metadata']['law']} (similarity: {best_similarity:.3f})")
            
            # Step 3: Generate response
            print("💬 Step 3: Generating response...")
            prompt = f"""Bạn là chuyên gia tư vấn pháp lý Việt Nam. Dựa trên tài liệu pháp lý sau đây, hãy trả lời câu hỏi một cách chính xác và hữu ích.

Tài liệu tham khảo:
{best_doc['content']}

Câu hỏi: {query}

Trả lời bằng tiếng Việt, ngắn gọn và chính xác:"""

            chat_response = chat_client.chat.completions.create(
                model=chat_model,
                messages=[
                    {"role": "system", "content": "Bạn là chuyên gia tư vấn pháp lý Việt Nam."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.1
            )
            
            answer = chat_response.choices[0].message.content
            
            # Display results
            print("\n🎉 RESULT:")
            print("-" * 50)
            print(f"❓ Câu hỏi: {query}")
            print(f"📚 Tài liệu: {best_doc['metadata']['law']} - {best_doc['metadata']['article']}")
            print(f"💡 Trả lời:\n{answer}")
            print("-" * 50)
        
        print(f"\n{'='*60}")
        print("🎉 Simple RAG test completed successfully!")
        print("✅ All components working: Embedding ✓ Chat ✓ RAG Pipeline ✓")
        print(f"🔍 Embedding Model: {embedding_model}")
        print(f"💬 Chat Model: {chat_model}")
        print(f"{'='*60}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in RAG test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_simple_rag()
