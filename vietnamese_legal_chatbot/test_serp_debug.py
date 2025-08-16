"""
Test SerpAPI integration debug
"""

import requests
import json

def test_serp_api_integration():
    """Test SerpAPI integration with debug"""
    
    # Test query
    test_query = {
        "question": "Thủ tục ly hôn thuận tình",
        "domain": "dan_su", 
        "region": "south"
    }
    
    print("🧪 Testing SerpAPI integration...")
    print(f"Query: {test_query}")
    
    try:
        response = requests.post(
            "http://localhost:8000/api/legal-query",
            json=test_query,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"\n📊 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            print("\n📝 Response Content:")
            print(f"Content length: {len(data.get('content', ''))}")
            print(f"Number of citations: {len(data.get('citations', []))}")
            
            print(f"\n💬 Content preview:")
            content = data.get('content', '')
            print(content[:500] + "..." if len(content) > 500 else content)
            
            print(f"\n📚 Citations:")
            for i, citation in enumerate(data.get('citations', []), 1):
                print(f"  {i}. {citation.get('document_name', 'N/A')}")
                print(f"     Source: {citation.get('source', 'N/A')}")
                print(f"     Authority: {citation.get('authority', 'N/A')}")
                print()
                
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_serp_api_integration()
