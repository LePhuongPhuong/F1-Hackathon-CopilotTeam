# 🏗️ System Architecture Diagrams - Vietnamese Legal AI Chatbot
# Sơ đồ Kiến trúc Hệ thống - Chatbot AI Pháp lý Việt Nam

> **Comprehensive system architecture documentation with detailed diagrams for the Vietnamese Legal AI Chatbot**  
> *Tài liệu kiến trúc hệ thống toàn diện với các sơ đồ chi tiết cho Chatbot AI Pháp lý Việt Nam*

## 📋 Table of Contents | Mục lục

1. [Architecture Overview](#-architecture-overview--tổng-quan-kiến-trúc)
2. [High-Level Architecture](#-high-level-architecture--kiến-trúc-tổng-thể)
3. [Component Architecture](#-component-architecture--kiến-trúc-component)
4. [Data Flow Diagrams](#-data-flow-diagrams--sơ-đồ-luồng-dữ-liệu)
5. [Deployment Architecture](#-deployment-architecture--kiến-trúc-triển-khai)
6. [Security Architecture](#-security-architecture--kiến-trúc-bảo-mật)
7. [Integration Architecture](#-integration-architecture--kiến-trúc-tích-hợp)
8. [Scalability Architecture](#-scalability-architecture--kiến-trúc-mở-rộng)

---

## 🎯 Architecture Overview | Tổng quan Kiến trúc

### Architecture Principles | Nguyên tắc Kiến trúc

1. **Microservices Architecture** - Kiến trúc microservices
2. **Cloud-Native Design** - Thiết kế cloud-native
3. **API-First Approach** - Tiếp cận API-first
4. **Scalable & Resilient** - Có khả năng mở rộng và phục hồi
5. **Vietnamese Language Optimized** - Tối ưu hóa cho tiếng Việt
6. **Security by Design** - Bảo mật theo thiết kế

### Technology Stack | Ngăn xếp Công nghệ

```mermaid
graph TB
    subgraph "Frontend Layer"
        A1[Streamlit 1.28+]
        A2[Vietnamese UI Components]
        A3[Clean Design]
    end
    
    subgraph "API Gateway Layer"
        B1[FastAPI 0.104+]
        B2[Authentication Middleware]
        B3[Rate Limiting]
    end
    
    subgraph "Application Layer"
        C1[Legal RAG Engine]
        C2[Vietnamese Text Processor]
    end
    
    subgraph "AI/ML Layer"
        D1[OpenAI GPT-4]
        D2[LangChain Framework]
        D3[Embedding Models]
        D4[Vietnamese NLP]
    end
    
    subgraph "Data Layer"
        E1[Pinecone Vector DB]
    end
    
    A1 --> B1
    B1 --> C1
    C1 --> D1
    C1 --> E1
    C2 --> D4
```

---

## 🏛️ High-Level Architecture | Kiến trúc Tổng thể

### System Context Diagram | Sơ đồ Ngữ cảnh Hệ thống

```mermaid
graph TB
    subgraph "External Users"
        U1[Vietnamese Citizens]
        U2[Legal Professionals]
        U3[System Administrators]
    end
    
    subgraph "Vietnamese Legal AI Chatbot System"
        SYS[Vietnamese Legal AI Chatbot<br/>Core System]
    end
    
    subgraph "External Services"
        E1[OpenAI API<br/>GPT-4 & Embeddings]
        E2[Pinecone Cloud<br/>Vector Database]
        E4[Monitoring Service<br/>Application Insights]
    end
    
    subgraph "External Data Sources"
        D1[Vietnamese Legal Documents<br/>Government Sources]
        D2[Legal Databases<br/>Third-party Sources]
        D3[Law Updates<br/>Official Publications]
    end
    
    U1 -->|Legal Questions<br/>Vietnamese Language| SYS
    U2 -->|Legal Research| SYS
    U3 -->|System Management<br/>Monitoring| SYS

    SYS -->|AI Processing<br/>Text Generation| E1
    SYS -->|Vector Search<br/>Document Retrieval| E2
    SYS -->|Performance Metrics<br/>Error Logs| E4
    
    D1 -->|Legal Content<br/>Document Ingestion| SYS
    D2 -->|Legal References<br/>Citation Data| SYS
    D3 -->|Law Changes<br/>Update Notifications| SYS
```

### Container Diagram | Sơ đồ Container

```mermaid
graph TB
    subgraph "User Devices"
        WEB[Web Browser<br/>Desktop Interface]
    end
    
    subgraph "Load Balancer & CDN"
        LB[Nginx Load Balancer<br/>SSL Termination]
        CDN[CloudFlare CDN<br/>Static Assets]
    end
    
    subgraph "Frontend Container"
        ST[Streamlit App<br/>Port 8501<br/>Vietnamese UI]
    end
    
    subgraph "Backend Container"
        API[FastAPI Backend<br/>Port 8000<br/>REST API]
    end
    
    subgraph "AI Processing Container"
        RAG[Legal RAG Engine<br/>Vietnamese Processing]
        NLP[Vietnamese NLP Service<br/>Text Analysis]
    end
    
    subgraph "External Services"
        OPENAI[OpenAI API<br/>GPT-4 & Embeddings]
        PINECONE[Pinecone<br/>Vector Database]
    end
    
    WEB --> LB
    LB --> ST
    ST -.->|API Calls| API
    API --> RAG
    API --> NLP
    RAG --> OPENAI
    RAG --> PINECONE
    NLP --> OPENAI
```

---

## 🔧 Component Architecture | Kiến trúc Component

### Backend Component Diagram | Sơ đồ Component Backend

```mermaid
graph TB
    subgraph "FastAPI Application"
        subgraph "API Layer"
            AUTH[Authentication Service]
            RATE[Rate Limiting Service]
            VALID[Input Validation]
            CORS[CORS Handler]
        end
        
        subgraph "Business Logic Layer"
            CHAT[Chat Controller]
            USER[User Controller]
            ADMIN[Admin Controller]
        end
        
        subgraph "Service Layer"
            LEGAL[Legal Service]
            RAGSERVICE[RAG Service]
            USERSERVICE[User Service]
            ANALYTICS[Analytics Service]
        end
        
        subgraph "Core Components"
            RAG[Vietnamese Legal RAG]
            CLASSIFIER[Legal Domain Classifier]
            EXTRACTOR[Vietnamese Text Extractor]
        end
        
        subgraph "Data Access Layer"
            PINECONE_DAO[Pinecone DAO]
        end
    end
    
    subgraph "External Integrations"
        OPENAI_CLIENT[OpenAI Client]
        PINECONE_CLIENT[Pinecone Client]
    end
    
    AUTH --> USERSERVICE
    CHAT --> LEGAL
    USER --> USERSERVICE
    ADMIN --> ANALYTICS
    
    LEGAL --> RAG
    RAGSERVICE --> RAG
    
    RAG --> CLASSIFIER
    RAG --> OPENAI_CLIENT
    CLASSIFIER --> PINECONE_DAO
    
    PINECONE_DAO --> PINECONE_CLIENT
```

### Frontend Component Diagram | Sơ đồ Component Frontend

```mermaid
graph TB
    subgraph "Streamlit Application"
        subgraph "UI Components"
            CHAT_UI[Chat Interface<br/>Vietnamese Input/Output]
            PROFILE_UI[User Profile UI<br/>Settings & Preferences]
            ADMIN_UI[Admin Dashboard UI<br/>Analytics & Management]
        end
        
        subgraph "State Management"
            SESSION[Session State<br/>User Context]
            CACHE[Frontend Cache<br/>Recent Queries]
            HISTORY[Chat History<br/>Conversation Memory]
        end
        
        subgraph "API Integration"
            API_CLIENT[FastAPI Client<br/>HTTP Requests]
            WEBSOCKET[WebSocket Client<br/>Real-time Updates]
        end
        
        subgraph "Vietnamese Language Support"
            FONT[Vietnamese Fonts<br/>Display Support]
            INPUT[Vietnamese Input<br/>Keyboard Support]
            VALIDATION[Vietnamese Validation<br/>Text Checking]
        end
        
        subgraph "Utility Components"
            ERROR[Error Handler<br/>User-friendly Messages]
            LOADING[Loading Indicators<br/>Progress Feedback]
            THEME[Theme Manager<br/>Vietnamese Styling]
        end
    end
    
    CHAT_UI --> SESSION
    CHAT_UI --> API_CLIENT
    CHAT_UI --> INPUT
    
    PROFILE_UI --> SESSION
    PROFILE_UI --> API_CLIENT
    
    ADMIN_UI --> WEBSOCKET
    ADMIN_UI --> API_CLIENT
    
    API_CLIENT --> ERROR
    
    SESSION --> CACHE
    SESSION --> HISTORY
```

---

## 🌊 Data Flow Diagrams | Sơ đồ Luồng Dữ liệu

### Legal Query Processing Flow | Luồng Xử lý Câu hỏi Pháp lý

```mermaid
sequenceDiagram
    participant U as User
    participant ST as Streamlit Frontend
    participant API as FastAPI Backend
    participant RAG as Legal RAG Engine
    participant NLP as Vietnamese NLP
    participant PC as Pinecone
    participant OAI as OpenAI API
    
    U->>ST: Enter Vietnamese legal question
    ST->>API: POST /api/legal-query
    
    API->>NLP: Analyze Vietnamese text
    NLP->>NLP: Tokenize & normalize text
    NLP->>NLP: Extract legal entities
    NLP-->>API: Return analysis results
    
    API->>RAG: Process legal query
    RAG->>NLP: Classify legal domain
    NLP-->>RAG: Return domain classification
    
    RAG->>OAI: Generate query embedding
    OAI-->>RAG: Return embedding vector
    
    RAG->>PC: Search similar documents
    PC-->>RAG: Return relevant documents
    
    RAG->>OAI: Generate response with context
    OAI-->>RAG: Return AI response
    
    RAG-->>API: Return structured response
    API-->>ST: Return response
    
    ST-->>U: Display Vietnamese legal advice
```

### User Authentication Flow | Luồng Xác thực Người dùng

```mermaid
sequenceDiagram
    participant U as User
    participant ST as Streamlit Frontend
    participant API as FastAPI Backend
    participant AUTH as Auth Service
    
    U->>ST: Enter login credentials
    ST->>API: POST /api/auth/login
    
    API->>AUTH: Validate credentials
    AUTH->>AUTH: Verify password hash
    alt Valid Credentials
        AUTH->>AUTH: Generate session token
        AUTH-->>API: Return user data & token
        API-->>ST: Return success + token
        ST->>ST: Store session state
        ST-->>U: Redirect to dashboard
    else Invalid Credentials
        AUTH-->>API: Return authentication error
        API-->>ST: Return error response
        ST-->>U: Show error message
    end
    
    Note over U,AUTH: New User Registration
    U->>ST: Register new account
    ST->>API: POST /api/auth/register
    API->>AUTH: Create user account
    AUTH-->>U: Account created
```

---

## 🚀 Deployment Architecture | Kiến trúc Triển khai

### Simple Deployment Diagram | Sơ đồ Triển khai Đơn giản

```mermaid
graph TB
    subgraph "Production Environment"
        subgraph "Application Tier"
            subgraph "Frontend"
                ST[Streamlit Application<br/>Port 8501]
            end
            
            subgraph "Backend"
                API[FastAPI Application<br/>Port 8000]
            end
        end
    end
    
    subgraph "External Services"
        PINECONE[Pinecone Cloud<br/>Vector Database]
        OPENAI[OpenAI API<br/>GPT-4 Service]
        MONITOR[Monitoring Service<br/>Application Insights]
    end
    
    ST --> API
    API --> PINECONE
    API --> OPENAI
    API --> MONITOR
```

---

## 🔐 Security Architecture | Kiến trúc Bảo mật

### Security Layers Diagram | Sơ đồ Lớp Bảo mật

```mermaid
graph TB
    subgraph "Security Layers"
        subgraph "Network Security"
            WAF[Web Application Firewall<br/>DDoS Protection]
            SSL[SSL/TLS Encryption<br/>Certificate Management]
            VPN[VPN Access<br/>Admin Access Only]
        end
        
        subgraph "Application Security"
            AUTH[JWT Authentication<br/>Token-based Security]
            AUTHZ[Role-based Authorization<br/>Permission Management]
            VALID[Input Validation<br/>XSS/Injection Prevention]
            RATE[Rate Limiting<br/>API Protection]
        end
        
        subgraph "Data Security"
            ENCRYPT[Data Encryption<br/>AES-256 at Rest]
            AUDIT[Audit Logging<br/>Security Events]
            GDPR[GDPR Compliance<br/>Vietnamese Data Laws]
        end
        
        subgraph "Infrastructure Security"
            SECRETS[Secret Management<br/>Environment Variables]
            MONITOR[Security Monitoring<br/>Intrusion Detection]
            UPDATE[Security Updates<br/>Vulnerability Management]
            ACCESS[Access Control<br/>Principle of Least Privilege]
        end
    end
    
    subgraph "External Security"
        MFA[Multi-Factor Authentication<br/>Enhanced User Security]
        PENTEST[Penetration Testing<br/>Regular Security Audits]
        COMPLIANCE[Compliance Monitoring<br/>Legal Requirements]
    end
    
    SSL --> AUTH
    AUTH --> AUTHZ
    AUTHZ --> VALID
    
    ENCRYPT --> AUDIT
    AUDIT --> GDPR
    
    SECRETS --> MONITOR
    MONITOR --> UPDATE
    UPDATE --> ACCESS
    
    MFA --> AUTH
    PENTEST --> MONITOR
    COMPLIANCE --> GDPR
```

### Authentication & Authorization Flow | Luồng Xác thực & Phân quyền

```mermaid
sequenceDiagram
    participant U as User
    participant FE as Frontend
    participant GW as API Gateway
    participant AUTH as Auth Service
    participant AUTHZ as Authorization Service
    participant API as Backend API
    participant DB as Database
    
    U->>FE: Login Request
    FE->>GW: POST /auth/login
    GW->>AUTH: Validate Credentials
    AUTH->>DB: Query User Data
    DB-->>AUTH: User Info + Roles
    AUTH->>AUTH: Generate JWT Token
    AUTH-->>GW: Return JWT + User Info
    GW-->>FE: Authentication Success
    FE->>FE: Store JWT in Session
    
    Note over U,DB: Protected API Call
    U->>FE: Access Protected Resource
    FE->>GW: API Call with JWT
    GW->>GW: Validate JWT Token
    GW->>AUTHZ: Check User Permissions
    AUTHZ->>DB: Query User Roles
    DB-->>AUTHZ: Role Information
    AUTHZ-->>GW: Authorization Result
    
    alt Authorized
        GW->>API: Forward Request
        API-->>GW: Response Data
        GW-->>FE: Return Data
        FE-->>U: Display Result
    else Unauthorized
        GW-->>FE: 403 Forbidden
        FE-->>U: Access Denied Message
    end
```

---

## 🔗 Integration Architecture | Kiến trúc Tích hợp

### External Service Integration | Tích hợp Dịch vụ Bên ngoài

```mermaid
graph TB
    subgraph "Vietnamese Legal AI Chatbot"
        CORE[Core Application]
        
        subgraph "Integration Layer"
            OPENAI_INT[OpenAI Integration<br/>API Client + Retry Logic]
            PINECONE_INT[Pinecone Integration<br/>Vector Operations]
            MONITORING_INT[Monitoring Integration<br/>Metrics + Alerts]
        end
        
        subgraph "Adapter Pattern"
            AI_ADAPTER[AI Service Adapter<br/>Abstract Interface]
            VECTOR_ADAPTER[Vector DB Adapter<br/>Abstract Interface]
        end
    end
    
    subgraph "External Services"
        OPENAI[OpenAI API<br/>GPT-4 + Embeddings]
        PINECONE[Pinecone Cloud<br/>Vector Database]
        APPINSIGHTS[Application Insights<br/>Azure Monitor]
    end
    
    subgraph "Fallback Services"
        OLLAMA[Ollama<br/>Local LLM Fallback]
        CHROMA[ChromaDB<br/>Local Vector DB]
    end
    
    CORE --> AI_ADAPTER
    CORE --> VECTOR_ADAPTER
    
    AI_ADAPTER --> OPENAI_INT
    VECTOR_ADAPTER --> PINECONE_INT
    
    OPENAI_INT --> OPENAI
    PINECONE_INT --> PINECONE
    MONITORING_INT --> APPINSIGHTS
    
    OPENAI_INT -.->|Fallback| OLLAMA
    PINECONE_INT -.->|Fallback| CHROMA
```

### API Integration Patterns | Mẫu Tích hợp API

```mermaid
graph TB
    subgraph "API Gateway Layer"
        GATEWAY[API Gateway<br/>FastAPI Router]
        
        subgraph "Middleware Stack"
            CORS_MW[CORS Middleware]
            AUTH_MW[Authentication Middleware]
            RATE_MW[Rate Limiting Middleware]
            LOG_MW[Logging Middleware]
            ERROR_MW[Error Handling Middleware]
        end
    end
    
    subgraph "Service Integration"
        subgraph "Synchronous APIs"
            REST_CLIENT[REST API Client<br/>HTTP/HTTPS]
            GRAPHQL_CLIENT[GraphQL Client<br/>Future Integration]
        end
        
        subgraph "Asynchronous Processing"
            QUEUE[Message Queue<br/>Redis Queue]
            WORKER[Background Workers<br/>Celery/AsyncIO]
            WEBHOOK[Webhook Handler<br/>Event Processing]
        end
        
        subgraph "Circuit Breaker Pattern"
            CB_OPENAI[OpenAI Circuit Breaker<br/>Fault Tolerance]
            CB_PINECONE[Pinecone Circuit Breaker<br/>Fault Tolerance]
        end
    end
    
    GATEWAY --> CORS_MW
    CORS_MW --> AUTH_MW
    AUTH_MW --> RATE_MW
    RATE_MW --> LOG_MW
    LOG_MW --> ERROR_MW
    
    ERROR_MW --> REST_CLIENT
    ERROR_MW --> QUEUE
    
    REST_CLIENT --> CB_OPENAI
    REST_CLIENT --> CB_PINECONE
    
    QUEUE --> WORKER
    WORKER --> WEBHOOK
```

---

## 📈 Scalability Architecture | Kiến trúc Mở rộng

### Horizontal Scaling Strategy | Chiến lược Mở rộng Ngang

```mermaid
graph TB
    subgraph "Auto-Scaling Groups"
        subgraph "Frontend Scaling"
            ST_LB[Streamlit Load Balancer]
            ST_ASG[Streamlit Auto Scaling Group<br/>Min: 2, Max: 10]
            ST1[Streamlit Instance 1]
            ST2[Streamlit Instance 2]
            STN[Streamlit Instance N]
        end
        
        subgraph "Backend Scaling"
            API_LB[API Load Balancer]
            API_ASG[FastAPI Auto Scaling Group<br/>Min: 3, Max: 20]
            API1[FastAPI Instance 1]
            API2[FastAPI Instance 2]
            APIN[FastAPI Instance N]
        end
        
        subgraph "Worker Scaling"
            WORKER_ASG[Worker Auto Scaling Group<br/>Min: 2, Max: 15]
            W1[Text Processor 1]
            W2[Text Processor 2]
            WN[Text Processor N]
        end
    end
    
    subgraph "External Scaling"
        PC_SHARDS[Pinecone Shards<br/>Multi-Region]
    end
    
    subgraph "Scaling Triggers"
        CPU_METRIC[CPU Usage > 70%]
        MEM_METRIC[Memory Usage > 80%]
        REQ_METRIC[Request Rate > 1000/min]
        QUEUE_METRIC[Queue Length > 100]
    end
    
    ST_LB --> ST_ASG
    ST_ASG --> ST1
    ST_ASG --> ST2
    ST_ASG --> STN
    
    API_LB --> API_ASG
    API_ASG --> API1
    API_ASG --> API2
    API_ASG --> APIN
    
    WORKER_ASG --> W1
    WORKER_ASG --> W2
    WORKER_ASG --> WN
    
    CPU_METRIC --> ST_ASG
    MEM_METRIC --> API_ASG
    REQ_METRIC --> API_ASG
    QUEUE_METRIC --> WORKER_ASG
    
    API1 --> PC_SHARDS
    API2 --> PC_SHARDS
    APIN --> PC_SHARDS
```

### Performance Optimization Architecture | Kiến trúc Tối ưu Hiệu suất

```mermaid
graph TB
    subgraph "Caching Strategy"
        subgraph "Multi-Level Cache"
            L1[L1 Cache<br/>Application Memory<br/>5 minutes TTL]
            L3[L3 Cache<br/>CDN Cache<br/>24 hours TTL]
        end
        
        subgraph "Cache Types"
            QUERY_CACHE[Query Result Cache<br/>Legal Responses]
            EMBEDDING_CACHE[Embedding Cache<br/>Vector Computations]
            SESSION_CACHE[Session Cache<br/>User State]
            STATIC_CACHE[Static Content Cache<br/>UI Assets]
        end
    end
    
    subgraph "Database Optimization"
        subgraph "Performance Optimization"
            QUERY_OPT[Query Optimization<br/>Index Strategy]
            CONN_POOL[Connection Pooling<br/>Resource Management]
        end
        
        subgraph "Processing Optimization"
            ASYNC_PROC[Async Processing<br/>Non-blocking]
            BATCH_PROC[Batch Processing<br/>Bulk Operations]
        end
    end
    
    subgraph "Vietnamese Language Optimization"
        TEXT_CACHE[Vietnamese Text Cache<br/>Processed Results]
        EMBEDDING_PRECOMPUTE[Precomputed Embeddings<br/>Common Legal Terms]
        DOMAIN_INDEX[Legal Domain Index<br/>Fast Classification]
    end
    
    L1 --> L3
    
    QUERY_CACHE --> L1
    EMBEDDING_CACHE --> L1
    SESSION_CACHE --> L1
    STATIC_CACHE --> L3
    
    QUERY_OPT --> CONN_POOL
    
    ASYNC_PROC --> BATCH_PROC
    
    TEXT_CACHE --> EMBEDDING_CACHE
    EMBEDDING_PRECOMPUTE --> DOMAIN_INDEX
```

---

## 📊 Monitoring & Observability Architecture | Kiến trúc Giám sát & Quan sát

### Observability Stack | Ngăn xếp Quan sát

```mermaid
graph TB
    subgraph "Application Monitoring"
        subgraph "Metrics Collection"
            PROMETHEUS[Prometheus<br/>Metrics Server]
            GRAFANA[Grafana<br/>Visualization Dashboard]
            ALERT_MGR[AlertManager<br/>Alert Routing]
        end
        
        subgraph "Logging Stack"
            FLUENTD[Fluentd<br/>Log Collector]
            ELASTICSEARCH[Elasticsearch<br/>Log Storage]
            KIBANA[Kibana<br/>Log Analysis]
        end
        
        subgraph "Tracing System"
            JAEGER[Jaeger<br/>Distributed Tracing]
            OPENTEL[OpenTelemetry<br/>Instrumentation]
        end
    end
    
    subgraph "Application Components"
        STREAMLIT[Streamlit App<br/>Frontend Metrics]
        FASTAPI[FastAPI Backend<br/>API Metrics]
        WORKERS[Background Workers<br/>Processing Metrics]
    end
    
    subgraph "Infrastructure Monitoring"
        NODE_EXPORTER[Node Exporter<br/>System Metrics]
        DOCKER_METRICS[Docker Metrics<br/>Container Stats]
    end
    
    subgraph "External Service Monitoring"
        OPENAI_MONITOR[OpenAI API Monitor<br/>Response Times & Errors]
        PINECONE_MONITOR[Pinecone Monitor<br/>Vector DB Performance]
        UPTIME_MONITOR[Uptime Monitor<br/>Service Availability]
    end
    
    STREAMLIT --> PROMETHEUS
    FASTAPI --> PROMETHEUS
    WORKERS --> PROMETHEUS
    
    STREAMLIT --> FLUENTD
    FASTAPI --> FLUENTD
    WORKERS --> FLUENTD
    
    FASTAPI --> OPENTEL
    OPENTEL --> JAEGER
    
    NODE_EXPORTER --> PROMETHEUS
    DOCKER_METRICS --> PROMETHEUS
    
    PROMETHEUS --> GRAFANA
    PROMETHEUS --> ALERT_MGR
    
    FLUENTD --> ELASTICSEARCH
    ELASTICSEARCH --> KIBANA
    
    OPENAI_MONITOR --> PROMETHEUS
    PINECONE_MONITOR --> PROMETHEUS
    UPTIME_MONITOR --> PROMETHEUS
```

---

## 📝 Architecture Decision Records | Bản ghi Quyết định Kiến trúc

### ADR-001: Python-Only Technology Stack

**Status:** Accepted  
**Date:** August 2025  

**Context:** Need to choose technology stack for Vietnamese Legal AI Chatbot

**Decision:** Use Python-only technology stack with FastAPI and Streamlit

**Rationale:**
- Unified development experience
- Rich AI/ML ecosystem in Python
- Vietnamese NLP library availability
- Team expertise alignment
- Simplified deployment and maintenance

**Consequences:**
- ✅ Faster development cycle
- ✅ Better Vietnamese language support
- ✅ Unified skill requirements
- ❌ Potential performance limitations
- ❌ Limited frontend flexibility

### ADR-002: Simplified Architecture

**Status:** Accepted  
**Date:** August 2025  

**Context:** Need to simplify architecture for faster development

**Decision:** Use simplified architecture without containers, databases, and complex infrastructure

**Rationale:**
- Faster development cycle
- Reduced complexity
- Focus on core AI functionality
- Minimal infrastructure overhead
- External services for data storage

**Consequences:**
- ✅ Simplified deployment
- ✅ Faster development
- ✅ Reduced maintenance overhead
- ❌ Limited scalability options
- ❌ Dependency on external services

### ADR-003: External AI Services

**Status:** Accepted  
**Date:** August 2025  

**Context:** Choice between self-hosted vs external AI services

**Decision:** Use OpenAI API with local fallback options

**Rationale:**
- Faster time to market
- State-of-the-art model quality
- Vietnamese language support
- Reduced infrastructure complexity
- Cost-effective for initial scale

**Consequences:**
- ✅ High-quality AI responses
- ✅ Reduced development time
- ✅ Automatic model updates
- ✅ Simplified data management
- ❌ External service dependency
- ❌ Data privacy considerations
- ❌ Variable API costs

---

*📅 Document Version: 1.0 | Created: August 2025 | Next Review: September 2025*

---

**Related Documents:**
- [User Stories](user-stories.md)
- [Use Cases](use-cases.md)
- [System Requirements](requirements.md)
- [Technical Specifications](technical-specs.md)
- [Deployment Guide](deployment.md)
