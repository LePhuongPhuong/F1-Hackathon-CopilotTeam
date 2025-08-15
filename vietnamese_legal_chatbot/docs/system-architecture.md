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
        C3[Document Service]
        C4[User Management]
    end
    
    subgraph "AI/ML Layer"
        D1[OpenAI GPT-4]
        D2[LangChain Framework]
        D3[Embedding Models]
        D4[Vietnamese NLP]
    end
    
    subgraph "Data Layer"
        E1[Pinecone Vector DB]
        E2[PostgreSQL]
        E3[Redis Cache]
        E4[File Storage]
    end
    
    A1 --> B1
    B1 --> C1
    C1 --> D1
    C1 --> E1
    C2 --> D4
    C3 --> E4
    C4 --> E2
    B2 --> E3
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
        U4[Content Managers]
    end
    
    subgraph "Vietnamese Legal AI Chatbot System"
        SYS[Vietnamese Legal AI Chatbot<br/>Core System]
    end
    
    subgraph "External Services"
        E1[OpenAI API<br/>GPT-4 & Embeddings]
        E2[Pinecone Cloud<br/>Vector Database]
        E3[Email Service<br/>SMTP Provider]
        E4[Monitoring Service<br/>Application Insights]
    end
    
    subgraph "External Data Sources"
        D1[Vietnamese Legal Documents<br/>Government Sources]
        D2[Legal Databases<br/>Third-party Sources]
        D3[Law Updates<br/>Official Publications]
    end
    
    U1 -->|Legal Questions<br/>Vietnamese Language| SYS
    U2 -->|Document Upload<br/>Legal Research| SYS
    U3 -->|System Management<br/>Monitoring| SYS
    U4 -->|Content Management<br/>Document Review| SYS
    
    SYS -->|AI Processing<br/>Text Generation| E1
    SYS -->|Vector Search<br/>Document Retrieval| E2
    SYS -->|Notifications<br/>User Communication| E3
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
    
    subgraph "Data Containers"
        POSTGRES[PostgreSQL<br/>User Data & History]
        REDIS[Redis<br/>Session & Cache]
        STORAGE[File Storage<br/>Document Repository]
    end
    
    subgraph "External Services"
        OPENAI[OpenAI API<br/>GPT-4 & Embeddings]
        PINECONE[Pinecone<br/>Vector Database]
    end
    
    WEB --> LB
    MOB --> LB
    LB --> ST
    ST -.->|API Calls| API
    API --> RAG
    API --> NLP
    API --> POSTGRES
    API --> REDIS
    API --> STORAGE
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
            DOC[Document Controller]
            USER[User Controller]
            ADMIN[Admin Controller]
        end
        
        subgraph "Service Layer"
            LEGAL[Legal Service]
            RAGSERVICE[RAG Service]
            DOCSERVICE[Document Service]
            USERSERVICE[User Service]
            ANALYTICS[Analytics Service]
        end
        
        subgraph "Core Components"
            RAG[Vietnamese Legal RAG]
            PROCESSOR[Document Processor]
            CLASSIFIER[Legal Domain Classifier]
            EXTRACTOR[Vietnamese Text Extractor]
        end
        
        subgraph "Data Access Layer"
            PINECONE_DAO[Pinecone DAO]
            POSTGRES_DAO[PostgreSQL DAO]
            REDIS_DAO[Redis DAO]
            FILE_DAO[File Storage DAO]
        end
    end
    
    subgraph "External Integrations"
        OPENAI_CLIENT[OpenAI Client]
        PINECONE_CLIENT[Pinecone Client]
        EMAIL_CLIENT[Email Client]
    end
    
    AUTH --> USERSERVICE
    CHAT --> LEGAL
    DOC --> DOCSERVICE
    USER --> USERSERVICE
    ADMIN --> ANALYTICS
    
    LEGAL --> RAG
    RAGSERVICE --> RAG
    DOCSERVICE --> PROCESSOR
    
    RAG --> CLASSIFIER
    RAG --> OPENAI_CLIENT
    PROCESSOR --> EXTRACTOR
    CLASSIFIER --> PINECONE_DAO
    
    PINECONE_DAO --> PINECONE_CLIENT
    POSTGRES_DAO -.-> POSTGRES_CLIENT
    REDIS_DAO -.-> REDIS_CLIENT
```

### Frontend Component Diagram | Sơ đồ Component Frontend

```mermaid
graph TB
    subgraph "Streamlit Application"
        subgraph "UI Components"
            CHAT_UI[Chat Interface<br/>Vietnamese Input/Output]
            DOC_UI[Document Upload UI<br/>Drag & Drop]
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
            FILE_UPLOAD[File Upload Handler<br/>Progress Tracking]
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
    
    DOC_UI --> FILE_UPLOAD
    DOC_UI --> API_CLIENT
    
    PROFILE_UI --> SESSION
    PROFILE_UI --> API_CLIENT
    
    ADMIN_UI --> WEBSOCKET
    ADMIN_UI --> API_CLIENT
    
    API_CLIENT --> ERROR
    FILE_UPLOAD --> LOADING
    
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
    participant PG as PostgreSQL
    participant RD as Redis
    
    U->>ST: Enter Vietnamese legal question
    ST->>API: POST /api/legal-query
    
    API->>RD: Check query cache
    alt Cache Hit
        RD-->>API: Return cached response
        API-->>ST: Return response
    else Cache Miss
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
        API->>RD: Cache response
        API->>PG: Log query & response
        API-->>ST: Return response
    end
    
    ST-->>U: Display Vietnamese legal advice
```

### Document Upload Processing Flow | Luồng Xử lý Tải lên Tài liệu

```mermaid
sequenceDiagram
    participant U as User
    participant ST as Streamlit Frontend
    participant API as FastAPI Backend
    participant DOC as Document Processor
    participant NLP as Vietnamese NLP
    participant PC as Pinecone
    participant FS as File Storage
    participant PG as PostgreSQL
    
    U->>ST: Select Vietnamese legal document
    ST->>API: POST /api/upload-document (multipart)
    
    API->>FS: Store temporary file
    FS-->>API: Return file path
    
    API->>DOC: Process document
    DOC->>DOC: Validate file format
    DOC->>DOC: Extract Vietnamese text
    DOC->>NLP: Analyze legal content
    
    NLP->>NLP: Identify legal entities
    NLP->>NLP: Classify legal domain
    NLP->>NLP: Extract key concepts
    NLP-->>DOC: Return analysis results
    
    DOC->>DOC: Chunk document text
    DOC->>PC: Generate embeddings
    PC-->>DOC: Return embedding vectors
    
    DOC->>PC: Store document chunks
    PC-->>DOC: Confirm storage
    
    DOC->>FS: Move to permanent storage
    FS-->>DOC: Confirm storage
    
    DOC->>PG: Save document metadata
    PG-->>DOC: Confirm save
    
    DOC-->>API: Return processing results
    API-->>ST: Return success response
    ST-->>U: Show upload confirmation
```

### User Authentication Flow | Luồng Xác thực Người dùng

```mermaid
sequenceDiagram
    participant U as User
    participant ST as Streamlit Frontend
    participant API as FastAPI Backend
    participant AUTH as Auth Service
    participant PG as PostgreSQL
    participant RD as Redis
    participant EMAIL as Email Service
    
    U->>ST: Enter login credentials
    ST->>API: POST /api/auth/login
    
    API->>AUTH: Validate credentials
    AUTH->>PG: Query user data
    PG-->>AUTH: Return user info
    
    AUTH->>AUTH: Verify password hash
    alt Valid Credentials
        AUTH->>RD: Generate session token
        RD-->>AUTH: Return token
        AUTH->>PG: Update last login
        AUTH-->>API: Return user data & token
        API-->>ST: Return success + token
        ST->>ST: Store session state
        ST-->>U: Redirect to dashboard
    else Invalid Credentials
        AUTH-->>API: Return authentication error
        API-->>ST: Return error response
        ST-->>U: Show error message
    end
    
    Note over U,EMAIL: New User Registration
    U->>ST: Register new account
    ST->>API: POST /api/auth/register
    API->>AUTH: Create user account
    AUTH->>PG: Save user data
    AUTH->>EMAIL: Send verification email
    EMAIL-->>U: Verification email
    U->>EMAIL: Click verification link
    EMAIL->>API: Verify email token
    API->>AUTH: Activate account
    AUTH-->>U: Account activated
```

---

## 🚀 Deployment Architecture | Kiến trúc Triển khai

### Container Deployment Diagram | Sơ đồ Triển khai Container

```mermaid
graph TB
    subgraph "Production Environment"
        subgraph "Load Balancer Tier"
            LB1[Nginx Load Balancer 1<br/>Primary]
            LB2[Nginx Load Balancer 2<br/>Backup]
        end
        
        subgraph "Application Tier"
            subgraph "Frontend Cluster"
                ST1[Streamlit Instance 1<br/>Port 8501]
                ST2[Streamlit Instance 2<br/>Port 8501]
                ST3[Streamlit Instance 3<br/>Port 8501]
            end
            
            subgraph "Backend Cluster"
                API1[FastAPI Instance 1<br/>Port 8000]
                API2[FastAPI Instance 2<br/>Port 8000]
                API3[FastAPI Instance 3<br/>Port 8000]
            end
        end
        
        subgraph "Data Tier"
            subgraph "Database Cluster"
                PG_MASTER[PostgreSQL Master<br/>Read/Write]
                PG_SLAVE1[PostgreSQL Slave 1<br/>Read Only]
                PG_SLAVE2[PostgreSQL Slave 2<br/>Read Only]
            end
            
            subgraph "Cache Cluster"
                RD_MASTER[Redis Master<br/>Primary Cache]
                RD_SLAVE1[Redis Slave 1<br/>Replica]
                RD_SLAVE2[Redis Slave 2<br/>Replica]
            end
        end
        
        subgraph "Storage Tier"
            FS1[File Storage 1<br/>Documents]
            FS2[File Storage 2<br/>Backup]
        end
    end
    
    subgraph "External Services"
        PINECONE[Pinecone Cloud<br/>Vector Database]
        OPENAI[OpenAI API<br/>GPT-4 Service]
        MONITOR[Monitoring Service<br/>Application Insights]
    end
    
    LB1 --> ST1
    LB1 --> ST2
    LB1 --> ST3
    LB2 --> ST1
    LB2 --> ST2
    LB2 --> ST3
    
    ST1 --> API1
    ST2 --> API2
    ST3 --> API3
    
    API1 --> PG_MASTER
    API2 --> PG_SLAVE1
    API3 --> PG_SLAVE2
    
    API1 --> RD_MASTER
    API2 --> RD_SLAVE1
    API3 --> RD_SLAVE2
    
    API1 --> FS1
    API2 --> FS1
    API3 --> FS1
    
    API1 --> PINECONE
    API2 --> PINECONE
    API3 --> PINECONE
    
    API1 --> OPENAI
    API2 --> OPENAI
    API3 --> OPENAI
    
    PG_MASTER -.-> PG_SLAVE1
    PG_MASTER -.-> PG_SLAVE2
    RD_MASTER -.-> RD_SLAVE1
    RD_MASTER -.-> RD_SLAVE2
    FS1 -.-> FS2
```

### Docker Compose Architecture | Kiến trúc Docker Compose

```mermaid
graph TB
    subgraph "Docker Compose Stack"
        subgraph "Frontend Services"
            FRONTEND[vietnamese-legal-frontend<br/>Streamlit Container<br/>Port: 8501]
        end
        
        subgraph "Backend Services"
            BACKEND[vietnamese-legal-backend<br/>FastAPI Container<br/>Port: 8000]
        end
        
        subgraph "Database Services"
            POSTGRES[vietnamese-legal-postgres<br/>PostgreSQL Container<br/>Port: 5432]
            REDIS[vietnamese-legal-redis<br/>Redis Container<br/>Port: 6379]
        end
        
        subgraph "Infrastructure Services"
            NGINX[vietnamese-legal-nginx<br/>Nginx Container<br/>Port: 80,443]
            PROMETHEUS[vietnamese-legal-prometheus<br/>Monitoring Container<br/>Port: 9090]
            GRAFANA[vietnamese-legal-grafana<br/>Dashboard Container<br/>Port: 3000]
        end
        
        subgraph "Data Volumes"
            VOL_PG[postgres_data<br/>Database Storage]
            VOL_RD[redis_data<br/>Cache Storage]
            VOL_FILES[file_storage<br/>Document Storage]
            VOL_LOGS[log_storage<br/>Application Logs]
        end
        
        subgraph "Networks"
            NET[vietnamese_legal_network<br/>Internal Communication]
        end
    end
    
    NGINX --> FRONTEND
    NGINX --> BACKEND
    FRONTEND --> BACKEND
    BACKEND --> POSTGRES
    BACKEND --> REDIS
    POSTGRES --> VOL_PG
    REDIS --> VOL_RD
    BACKEND --> VOL_FILES
    BACKEND --> VOL_LOGS
    
    PROMETHEUS --> BACKEND
    GRAFANA --> PROMETHEUS
    
    FRONTEND -.-> NET
    BACKEND -.-> NET
    POSTGRES -.-> NET
    REDIS -.-> NET
    NGINX -.-> NET
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
            BACKUP[Secure Backups<br/>Encrypted Storage]
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
    
    WAF --> SSL
    SSL --> AUTH
    AUTH --> AUTHZ
    AUTHZ --> VALID
    
    ENCRYPT --> BACKUP
    BACKUP --> AUDIT
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
            EMAIL_INT[Email Integration<br/>SMTP + Templates]
            MONITORING_INT[Monitoring Integration<br/>Metrics + Alerts]
        end
        
        subgraph "Adapter Pattern"
            AI_ADAPTER[AI Service Adapter<br/>Abstract Interface]
            VECTOR_ADAPTER[Vector DB Adapter<br/>Abstract Interface]
            NOTIFICATION_ADAPTER[Notification Adapter<br/>Abstract Interface]
        end
    end
    
    subgraph "External Services"
        OPENAI[OpenAI API<br/>GPT-4 + Embeddings]
        PINECONE[Pinecone Cloud<br/>Vector Database]
        SMTP[Email Service<br/>SendGrid/SMTP]
        APPINSIGHTS[Application Insights<br/>Azure Monitor]
    end
    
    subgraph "Fallback Services"
        OLLAMA[Ollama<br/>Local LLM Fallback]
        CHROMA[ChromaDB<br/>Local Vector DB]
        LOCAL_EMAIL[Local Email<br/>SMTP Server]
    end
    
    CORE --> AI_ADAPTER
    CORE --> VECTOR_ADAPTER
    CORE --> NOTIFICATION_ADAPTER
    
    AI_ADAPTER --> OPENAI_INT
    VECTOR_ADAPTER --> PINECONE_INT
    NOTIFICATION_ADAPTER --> EMAIL_INT
    
    OPENAI_INT --> OPENAI
    PINECONE_INT --> PINECONE
    EMAIL_INT --> SMTP
    MONITORING_INT --> APPINSIGHTS
    
    OPENAI_INT -.->|Fallback| OLLAMA
    PINECONE_INT -.->|Fallback| CHROMA
    EMAIL_INT -.->|Fallback| LOCAL_EMAIL
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
            CB_EMAIL[Email Circuit Breaker<br/>Fault Tolerance]
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
    REST_CLIENT --> CB_EMAIL
    
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
            W1[Document Processor 1]
            W2[Document Processor 2]
            WN[Document Processor N]
        end
    end
    
    subgraph "Database Scaling"
        PG_CLUSTER[PostgreSQL Cluster<br/>Read Replicas]
        RD_CLUSTER[Redis Cluster<br/>Sharded Cache]
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
    
    API1 --> PG_CLUSTER
    API2 --> PG_CLUSTER
    APIN --> PG_CLUSTER
    
    API1 --> RD_CLUSTER
    API2 --> RD_CLUSTER
    APIN --> RD_CLUSTER
    
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
            L2[L2 Cache<br/>Redis Cache<br/>1 hour TTL]
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
        subgraph "Read Optimization"
            READ_REPLICA[Read Replicas<br/>Load Distribution]
            QUERY_OPT[Query Optimization<br/>Index Strategy]
            CONN_POOL[Connection Pooling<br/>Resource Management]
        end
        
        subgraph "Write Optimization"
            BATCH_WRITE[Batch Writes<br/>Bulk Operations]
            ASYNC_WRITE[Async Writes<br/>Non-blocking]
            PARTITION[Table Partitioning<br/>Date-based]
        end
    end
    
    subgraph "Vietnamese Language Optimization"
        TEXT_CACHE[Vietnamese Text Cache<br/>Processed Results]
        EMBEDDING_PRECOMPUTE[Precomputed Embeddings<br/>Common Legal Terms]
        DOMAIN_INDEX[Legal Domain Index<br/>Fast Classification]
    end
    
    L1 --> L2
    L2 --> L3
    
    QUERY_CACHE --> L1
    EMBEDDING_CACHE --> L2
    SESSION_CACHE --> L2
    STATIC_CACHE --> L3
    
    READ_REPLICA --> QUERY_OPT
    QUERY_OPT --> CONN_POOL
    
    BATCH_WRITE --> ASYNC_WRITE
    ASYNC_WRITE --> PARTITION
    
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
        POSTGRES_EXPORTER[PostgreSQL Exporter<br/>Database Metrics]
        REDIS_EXPORTER[Redis Exporter<br/>Cache Metrics]
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
    POSTGRES_EXPORTER --> PROMETHEUS
    REDIS_EXPORTER --> PROMETHEUS
    
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

### ADR-002: Microservices with Containers

**Status:** Accepted  
**Date:** August 2025  

**Context:** Need to decide on deployment architecture

**Decision:** Use containerized microservices with Docker

**Rationale:**
- Scalability requirements
- Development team separation
- Technology isolation
- Cloud-native deployment
- Easy CI/CD integration

**Consequences:**
- ✅ Independent service scaling
- ✅ Technology flexibility
- ✅ Better fault isolation
- ❌ Increased complexity
- ❌ Network latency concerns

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
