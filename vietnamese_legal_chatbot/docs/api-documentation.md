# 🔌 API Documentation - Vietnamese Legal AI Chatbot

## Overview

The Vietnamese Legal AI Chatbot provides a comprehensive REST API built with FastAPI for legal consultation services. This documentation covers all available endpoints, request/response formats, and integration examples.

## Base URL

```
Development: http://localhost:8000
Production: https://api.legal-ai.gov.vn
```

## Authentication

Currently, the API uses API key authentication for production environments:

```http
Authorization: Bearer <your-api-key>
Content-Type: application/json
```

## API Endpoints

### 1. Legal Query Endpoint

**Endpoint**: `POST /api/legal-query`

**Description**: Submit a legal question and receive AI-powered consultation with citations.

**Request Body**:
```json
{
  "query": "Thủ tục ly hôn thuận tình cần những gì?",
  "region": "south",
  "legal_domain": "gia_dinh",
  "user_context": {
    "age": 30,
    "gender": "female",
    "occupation": "teacher"
  }
}
```

**Response**:
```json
{
  "response": {
    "content": "Dựa trên câu hỏi của bạn về thủ tục ly hôn thuận tình...",
    "confidence": 0.95,
    "processing_time": 1.2
  },
  "citations": [
    {
      "title": "Luật Hôn nhân và Gia đình 2014",
      "article": "Điều 62",
      "clause": "Khoản 1",
      "content": "Việc ly hôn được thực hiện tại Tòa án...",
      "authority": "Quốc hội",
      "date": "23/06/2014",
      "relevance_score": 0.89
    }
  ],
  "related_topics": [
    "Thủ tục tại tòa án",
    "Phân chia tài sản",
    "Quyền nuôi con"
  ],
  "session_id": "session_123456789"
}
```

**Status Codes**:
- `200`: Success
- `400`: Bad Request (invalid query format)
- `422`: Validation Error
- `500`: Internal Server Error

### 2. Document Upload Endpoint

**Endpoint**: `POST /api/upload-document`

**Description**: Upload legal documents for processing and inclusion in the knowledge base.

**Request**: Multipart form data
```
file: <legal_document.pdf>
metadata: {
  "document_type": "law",
  "legal_domain": "dan_su",
  "authority": "Quốc hội",
  "date_issued": "2015-11-24",
  "description": "Bộ luật Dân sự 2015"
}
```

**Response**:
```json
{
  "document_id": "doc_123456789",
  "status": "processed",
  "message": "Document uploaded and processed successfully",
  "metadata": {
    "pages": 450,
    "chapters": 24,
    "articles": 689,
    "processing_time": 45.2
  },
  "embeddings_created": 1250
}
```

### 3. Legal Domains Endpoint

**Endpoint**: `GET /api/legal-domains`

**Description**: Retrieve list of supported Vietnamese legal domains.

**Response**:
```json
{
  "domains": [
    {
      "id": "dan_su",
      "name": "Luật Dân sự",
      "description": "Quyền sở hữu, hợp đồng, nghĩa vụ dân sự",
      "subcategories": [
        "Quyền sở hữu",
        "Hợp đồng",
        "Nghĩa vụ dân sự",
        "Thừa kế"
      ],
      "document_count": 1250
    },
    {
      "id": "hinh_su",
      "name": "Luật Hình sự",
      "description": "Tội phạm, hình phạt, thủ tục tố tụng",
      "subcategories": [
        "Tội phạm",
        "Hình phạt",
        "Thủ tục tố tụng"
      ],
      "document_count": 890
    }
  ]
}
```

### 4. Chat History Endpoint

**Endpoint**: `GET /api/chat-history/{session_id}`

**Description**: Retrieve chat history for a specific session.

**Parameters**:
- `session_id`: String - Unique session identifier
- `limit`: Integer (optional) - Number of messages to return (default: 50)
- `offset`: Integer (optional) - Pagination offset (default: 0)

**Response**:
```json
{
  "session_id": "session_123456789",
  "messages": [
    {
      "id": "msg_001",
      "timestamp": "2025-01-15T10:30:00Z",
      "role": "user",
      "content": "Thủ tục ly hôn thuận tình cần những gì?",
      "metadata": {
        "region": "south",
        "legal_domain": "gia_dinh"
      }
    },
    {
      "id": "msg_002",
      "timestamp": "2025-01-15T10:30:02Z",
      "role": "assistant",
      "content": "Dựa trên câu hỏi của bạn...",
      "metadata": {
        "confidence": 0.95,
        "processing_time": 1.2,
        "citations_count": 3
      }
    }
  ],
  "total_messages": 2,
  "session_created": "2025-01-15T10:29:55Z"
}
```

### 5. Health Check Endpoint

**Endpoint**: `GET /health`

**Description**: Check system health and service status.

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2025-01-15T10:30:00Z",
  "version": "2.0.0",
  "services": {
    "pinecone": {
      "status": "connected",
      "index_stats": {
        "total_vectors": 125000,
        "dimension": 1536
      }
    },
    "openai": {
      "status": "available",
      "model": "gpt-4"
    },
    "database": {
      "status": "connected",
      "response_time": "2ms"
    }
  },
  "performance": {
    "average_response_time": "1.5s",
    "requests_per_minute": 45,
    "error_rate": "0.1%"
  }
}
```

## Regional Support

The API supports Vietnamese regional variations:

| Region Code | Name | Description |
|-------------|------|-------------|
| `north` | Miền Bắc | Northern Vietnam legal preferences |
| `central` | Miền Trung | Central Vietnam legal preferences |
| `south` | Miền Nam | Southern Vietnam legal preferences |
| `special_zones` | Khu Đặc biệt | Special economic zones |

## Error Handling

### Standard Error Response

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid query format",
    "details": "Query must be at least 10 characters long",
    "timestamp": "2025-01-15T10:30:00Z",
    "request_id": "req_123456789"
  }
}
```

### Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `VALIDATION_ERROR` | 422 | Request validation failed |
| `RATE_LIMIT_EXCEEDED` | 429 | Too many requests |
| `UNAUTHORIZED` | 401 | Invalid or missing API key |
| `RESOURCE_NOT_FOUND` | 404 | Requested resource not found |
| `INTERNAL_ERROR` | 500 | Internal server error |
| `SERVICE_UNAVAILABLE` | 503 | External service unavailable |

## Rate Limiting

The API implements rate limiting to ensure fair usage:

- **Free Tier**: 100 requests per hour
- **Standard Tier**: 1000 requests per hour
- **Premium Tier**: 10000 requests per hour

Rate limit headers are included in responses:

```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1642262400
```

## SDK Examples

### Python SDK

```python
import requests

class VietnameseLegalAPI:
    def __init__(self, api_key, base_url="http://localhost:8000"):
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        })
    
    def legal_query(self, query, region="south", legal_domain=None):
        payload = {
            "query": query,
            "region": region,
            "legal_domain": legal_domain
        }
        response = self.session.post(
            f"{self.base_url}/api/legal-query",
            json=payload
        )
        return response.json()
    
    def get_legal_domains(self):
        response = self.session.get(f"{self.base_url}/api/legal-domains")
        return response.json()

# Usage example
api = VietnameseLegalAPI("your-api-key")
result = api.legal_query("Thủ tục ly hôn thuận tình cần những gì?")
print(result["response"]["content"])
```

### cURL Examples

```bash
# Legal Query
curl -X POST "http://localhost:8000/api/legal-query" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer your-api-key" \
     -d '{
       "query": "Thủ tục ly hôn thuận tình cần những gì?",
       "region": "south",
       "legal_domain": "gia_dinh"
     }'

# Get Legal Domains
curl -X GET "http://localhost:8000/api/legal-domains" \
     -H "Authorization: Bearer your-api-key"

# Health Check
curl -X GET "http://localhost:8000/health"
```

### JavaScript/Node.js

```javascript
const axios = require('axios');

class VietnameseLegalAPI {
    constructor(apiKey, baseURL = 'http://localhost:8000') {
        this.apiKey = apiKey;
        this.baseURL = baseURL;
        this.client = axios.create({
            baseURL: this.baseURL,
            headers: {
                'Authorization': `Bearer ${apiKey}`,
                'Content-Type': 'application/json'
            }
        });
    }
    
    async legalQuery(query, region = 'south', legalDomain = null) {
        try {
            const response = await this.client.post('/api/legal-query', {
                query,
                region,
                legal_domain: legalDomain
            });
            return response.data;
        } catch (error) {
            throw new Error(`API Error: ${error.response.data.error.message}`);
        }
    }
    
    async getLegalDomains() {
        const response = await this.client.get('/api/legal-domains');
        return response.data;
    }
}

// Usage
const api = new VietnameseLegalAPI('your-api-key');
api.legalQuery('Thủ tục ly hôn thuận tình cần những gì?')
   .then(result => console.log(result.response.content))
   .catch(error => console.error(error));
```

## Webhook Support

For real-time notifications and updates:

### Document Processing Webhook

```json
{
  "event": "document.processed",
  "timestamp": "2025-01-15T10:30:00Z",
  "data": {
    "document_id": "doc_123456789",
    "status": "completed",
    "embeddings_created": 1250,
    "processing_time": 45.2
  }
}
```

### Usage Analytics Webhook

```json
{
  "event": "usage.report",
  "timestamp": "2025-01-15T10:30:00Z",
  "data": {
    "period": "daily",
    "total_queries": 1250,
    "unique_users": 89,
    "top_domains": ["gia_dinh", "dan_su", "lao_dong"],
    "average_response_time": 1.5
  }
}
```

## Monitoring and Analytics

### API Metrics

The system provides comprehensive metrics:

- **Response Times**: P50, P95, P99 percentiles
- **Error Rates**: By endpoint and error type
- **Usage Patterns**: Peak hours, popular domains
- **Performance**: Throughput and latency

### Custom Dashboards

Integration with monitoring tools:
- Grafana dashboards
- Prometheus metrics
- Custom alerting rules
- Real-time monitoring

---

For additional support or questions, contact: **legal-ai@moj.gov.vn**
