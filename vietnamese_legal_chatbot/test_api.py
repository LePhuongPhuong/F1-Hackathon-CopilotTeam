#!/usr/bin/env python3
"""
Test script for debugging API issues
"""

import requests
import json

def test_api():
    url = "http://localhost:8000/api/legal-query"
    payload = {
        "question": "Thủ tục ly hôn thuận tình",
        "domain": "dan_su", 
        "region": "south"
    }
    
    print(f"Testing API: {url}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 422:
            print("Validation Error Details:")
            error_data = response.json()
            print(json.dumps(error_data, indent=2))
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_api()
