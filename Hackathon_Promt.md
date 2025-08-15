## Prompt Chính cho Dự án Chatbot AI Pháp lý Việt Nam Chỉ sử dụng Python

**Prompt Tiếng Việt:**

```
Bạn là một kiến trúc sư hệ thống AI chuyên gia chuyên về các ứng dụng AI pháp lý. Tạo một dự án Chatbot Pháp lý Việt Nam toàn diện chỉ sử dụng PYTHON và PINECONE làm cơ sở dữ liệu vector. Tạo ra tài liệu, kiến trúc, triển khai và tài liệu kiểm thử hoàn chỉnh theo tiêu chuẩn doanh nghiệp với ngăn xếp công nghệ đơn giản này.

## TỔNG QUAN DỰ ÁN
Tạo một chatbot pháp lý được hỗ trợ bởi AI cho luật pháp Việt Nam có thể:
- Trả lời các câu hỏi pháp lý sử dụng tài liệu pháp lý Việt Nam
- Cung cấp tư vấn pháp lý dựa trên pháp luật Việt Nam hiện hành
- Xử lý các truy vấn pháp lý phức tạp với trích dẫn phù hợp
- Hỗ trợ nhiều lĩnh vực pháp lý (dân sự, hình sự, thương mại, lao động, v.v.)
- Đảm bảo tính chính xác và tuân thủ pháp luật

## RÀNG BUỘC CÔNG NGHỆ
**NGĂN XẾP CÔNG NGHỆ BẮT BUỘC:**
- Ngôn ngữ lập trình: CHỈ Python (không có JavaScript/TypeScript)
- Cơ sở dữ liệu Vector: CHỈ Pinecone (không có PostgreSQL, Redis, hoặc cơ sở dữ liệu khác)
- Frontend: Framework web dựa trên Python (Streamlit)
- Backend: FastAPI với Python
- Tích hợp LLM: LangChain/LangGraph với OpenAI hoặc mô hình cục bộ
- Xử lý Tài liệu: Chỉ thư viện Python
- Triển khai: Container hóa dựa trên Python

## CÁC SẢN PHẨM YÊU CẦU

### 1. YÊU CẦU KINH DOANH & TÀI LIỆU

Tạo tài liệu chi tiết cho:

**Câu chuyện Người dùng & Trường hợp Sử dụng:**
- Nhân vật chính: Công dân cá nhân, chủ doanh nghiệp nhỏ, chuyên gia pháp lý, sinh viên luật
- Lập bản đồ hành trình người dùng từ truy vấn ban đầu đến tư vấn pháp lý
- Các tình huống trường hợp sử dụng chi tiết với tiêu chí chấp nhận
- Các trường hợp biên và tình huống xử lý lỗi

**Danh sách Tính năng MVP (Triển khai Chỉ Python):**
- Giao diện chat dựa trên Streamlit
- Truy xuất tài liệu pháp lý Việt Nam sử dụng Pinecone
- Trích dẫn và tham chiếu nguồn
- Hỗ trợ kiến thức pháp lý đa lĩnh vực
- Quản lý phiên đơn giản (dựa trên file hoặc trong bộ nhớ)
- Tải lên và phân tích tài liệu pháp lý qua trình tải file Streamlit
- Xuất lịch sử hội thoại ra CSV/JSON
- Giao diện web responsive sử dụng các thành phần Streamlit

**Yêu cầu Kinh doanh:**
- Yêu cầu chức năng với mức độ ưu tiên
- Yêu cầu phi chức năng (hiệu suất, bảo mật, khả năng mở rộng)
- Yêu cầu tuân thủ pháp luật (luật bảo vệ dữ liệu Việt Nam)
- Yêu cầu tích hợp với cơ sở dữ liệu vector Pinecone

### 2. THIẾT KẾ HỆ THỐNG & KIẾN TRÚC

Tạo tài liệu kỹ thuật toàn diện:

**Kiến trúc Hệ thống Đơn giản:**
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Streamlit     │    │   FastAPI        │    │   Pinecone      │
│   Frontend      │◄──►│   Backend        │◄──►│   Vector DB     │
│   (Python)      │    │   (Python)       │    │   (Cloud)       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │
         ▼                       ▼
┌─────────────────┐    ┌──────────────────┐
│ Lưu trữ File    │    │ OpenAI/Local     │
│ Cục bộ          │    │ LLM Service      │
│ (Tài liệu)      │    │ (API/Local)      │
└─────────────────┘    └──────────────────┘
```

**Ngăn xếp Công nghệ Python:**
- **Frontend**: Streamlit (framework web Python thuần túy)
- **Backend**: FastAPI với Python
- **Cơ sở dữ liệu Vector**: Pinecone (dịch vụ cloud được quản lý)
- **Xử lý Tài liệu**: PyPDF2, python-docx, langchain
- **Framework LLM**: LangChain/LangGraph
- **Lưu trữ Dữ liệu**: Hệ thống file cục bộ + Pinecone
- **Quản lý Phiên**: Trạng thái phiên Streamlit
- **Triển khai**: Docker với image cơ sở Python

### 3. TRIỂN KHAI PYTHON HOÀN CHỈNH

Cung cấp cấu trúc mã nguồn hoàn chỉnh:

**Cấu trúc Dự án:**
```
vietnamese_legal_chatbot/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Backend FastAPI
│   ├── streamlit_app.py        # Frontend Streamlit
│   ├── models/
│   │   ├── __init__.py
│   │   ├── chat_model.py       # Tích hợp LLM
│   │   └── legal_rag.py        # Triển khai RAG
│   ├── services/
│   │   ├── __init__.py
│   │   ├── pinecone_service.py # Các thao tác Pinecone
│   │   ├── document_processor.py # Xử lý tài liệu
│   │   └── legal_analyzer.py   # Logic phân tích pháp lý
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── text_processing.py  # Xử lý văn bản tiếng Việt
│   │   └── config.py          # Quản lý cấu hình
│   └── data/
│       ├── legal_documents/    # Lưu trữ tài liệu cục bộ
│       └── processed/         # Cache tài liệu đã xử lý
├── tests/
│   ├── __init__.py
│   ├── test_models/
│   ├── test_services/
│   └── test_utils/
├── scripts/
│   ├── setup_pinecone.py      # Thiết lập chỉ mục Pinecone
│   ├── process_documents.py   # Tiền xử lý tài liệu
│   └── deploy.py              # Script triển khai
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

**Các File Triển khai Cốt lõi:**

**1. Backend FastAPI (main.py):**
```python
# Tạo backend FastAPI hoàn chỉnh với:
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.vectorstores import Pinecone
import os
from typing import List, Dict, Optional
from pydantic import BaseModel

app = FastAPI(title="API Chatbot Pháp lý Việt Nam")

# Tạo triển khai hoàn chỉnh bao gồm:
# - Endpoints xử lý truy vấn pháp lý
# - Tải lên và xử lý tài liệu
# - Tích hợp tìm kiếm vector Pinecone
# - Pipeline RAG LangChain
# - Xử lý văn bản tiếng Việt
# - Xử lý lỗi và ghi log
# - Trích xuất trích dẫn pháp lý
# - Định dạng phản hồi
```

**2. Frontend Streamlit (streamlit_app.py):**
```python
# Tạo giao diện Streamlit hoàn chỉnh với:
import streamlit as st
import requests
import json
from typing import Dict, List
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Chatbot AI Pháp lý Việt Nam",
    page_icon="⚖️",
    layout="wide"
)

# Tạo triển khai hoàn chỉnh bao gồm:
# - Giao diện chat tiếng Việt
# - Chức năng tải lên tài liệu
# - Trình xem tài liệu pháp lý
# - Hiển thị lịch sử hội thoại
# - Chức năng xuất
# - Hiển thị trích dẫn pháp lý
# - Thu thập phản hồi người dùng
# - Quản lý trạng thái phiên
# - Hỗ trợ đa ngôn ngữ (Việt/Anh)
```

**3. Dịch vụ Pinecone (pinecone_service.py):**
```python
# Tạo tích hợp Pinecone hoàn chỉnh:
import pinecone
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from typing import List, Dict, Tuple
import numpy as np

class PineconeService:
    def __init__(self, api_key: str, environment: str, index_name: str):
        # Tạo triển khai hoàn chỉnh bao gồm:
        # - Khởi tạo client Pinecone
        # - Tạo và quản lý chỉ mục
        # - Embedding và lưu trữ tài liệu
        # - Triển khai tìm kiếm semantic
        # - Lọc metadata cho các lĩnh vực pháp lý
        # - Xử lý hàng loạt cho tài liệu lớn
        # - Xử lý lỗi và logic thử lại
        # - Tối ưu hóa hiệu suất
```

**4. Hệ thống RAG Pháp lý (legal_rag.py):**
```python
# Tạo triển khai RAG hoàn chỉnh:
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
import re
from typing import Dict, List, Optional

class VietnameseLegalRAG:
    def __init__(self, pinecone_service, llm_model):
        # Tạo triển khai hoàn chỉnh bao gồm:
        # - Truy xuất tài liệu pháp lý Việt Nam
        # - Tạo câu trả lời nhận thức ngữ cảnh
        # - Trích xuất và định dạng trích dẫn pháp lý
        # - Xử lý kiến thức pháp lý đa lĩnh vực
        # - Tiền xử lý truy vấn cho thuật ngữ pháp lý Việt Nam
        # - Xác thực phản hồi và kiểm tra sự thật
        # - Tính điểm độ tin cậy
        # - Chiến lược dự phòng cho truy vấn không xác định
```

**5. Xử lý Tài liệu (document_processor.py):**
```python
# Tạo pipeline xử lý tài liệu hoàn chỉnh:
import PyPDF2
import docx
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader, UnstructuredWordDocumentLoader
import re
from typing import List, Dict
import os

class VietnameseLegalDocumentProcessor:
    def __init__(self):
        # Tạo triển khai hoàn chỉnh bao gồm:
        # - Phân tích tài liệu PDF và Word
        # - Tiền xử lý văn bản pháp lý Việt Nam
        # - Phân đoạn tài liệu với bảo tồn ngữ cảnh pháp lý
        # - Trích xuất metadata (tên luật, số điều, ngày tháng)
        # - Làm sạch và chuẩn hóa văn bản cho tiếng Việt
        # - Nhận dạng cấu trúc pháp lý (chương, điều, khoản)
        # - Xác thực chất lượng và lọc
        # - Khả năng xử lý hàng loạt
```

### 4. BỘ KIỂM THỬ (Chỉ Python)

Tạo kiểm thử toàn diện:

**Triển khai Kiểm thử:**
```python
# Tạo bộ kiểm thử hoàn chỉnh sử dụng pytest:

# tests/test_pinecone_service.py
import pytest
from app.services.pinecone_service import PineconeService
import numpy as np

class TestPineconeService:
    # Tạo kiểm thử toàn diện bao gồm:
    # - Kiểm thử kết nối và xác thực
    # - Kiểm thử embedding và truy xuất tài liệu
    # - Xác thực độ chính xác tìm kiếm
    # - Đánh giá hiệu suất
    # - Xác minh xử lý lỗi

# tests/test_legal_rag.py
import pytest
from app.models.legal_rag import VietnameseLegalRAG

class TestVietnameseLegalRAG:
    # Tạo kiểm thử bao gồm:
    # - Độ chính xác xử lý truy vấn pháp lý
    # - Xác thực trích xuất trích dẫn
    # - Đánh giá chất lượng phản hồi
    # - Kiểm thử xử lý ngôn ngữ Việt Nam
    # - Xử lý trường hợp biên

# tests/test_document_processor.py
import pytest
from app.services.document_processor import VietnameseLegalDocumentProcessor

class TestDocumentProcessor:
    # Tạo kiểm thử bao gồm:
    # - Độ chính xác phân tích tài liệu
    # - Xác thực xử lý văn bản tiếng Việt
    # - Xác minh trích xuất metadata
    # - Đánh giá chất lượng phân đoạn
    # - Kiểm thử hiệu suất cho tài liệu lớn
```

### 5. TRIỂN KHAI (Dựa trên Python)

**Cấu hình Docker:**
```dockerfile
# Tạo Dockerfile hoàn chỉnh:
FROM python:3.9-slim

WORKDIR /app

# Sao chép requirements và cài đặt dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép mã ứng dụng
COPY app/ ./app/
COPY scripts/ ./scripts/

# Mở cổng cho cả FastAPI và Streamlit
EXPOSE 8000 8501

# Tạo script khởi động cho cả hai dịch vụ
CMD ["python", "scripts/start_services.py"]
```

**Scripts Thiết lập và Triển khai:**
```python
# scripts/setup_pinecone.py
# Tạo script thiết lập Pinecone hoàn chỉnh bao gồm:
# - Tạo chỉ mục với cấu hình tối ưu
# - Tải tài liệu ban đầu
# - Tạo và tải lên embedding
# - Xác thực và kiểm thử

# scripts/deploy.py  
# Tạo script triển khai bao gồm:
# - Thiết lập môi trường
# - Khởi tạo dịch vụ
# - Kiểm tra sức khỏe
# - Thiết lập giám sát
```

### 6. TÀI LIỆU & TRÌNH BÀY

Tạo tài liệu toàn diện:

**README.md:**
```markdown
# Chatbot AI Pháp lý Việt Nam

## Tổng quan
Tài liệu hoàn chỉnh bao gồm:
- Mô tả dự án và tính năng
- Hướng dẫn cài đặt và thiết lập
- Ví dụ sử dụng và tài liệu API
- Hướng dẫn cấu hình cho Pinecone
- Hướng dẫn triển khai
- Hướng dẫn khắc phục sự cố
```

**Tài liệu API:**
Tạo tài liệu tự động FastAPI hoàn chỉnh với ví dụ cho tất cả endpoints.

**Hướng dẫn Người dùng:**
Tạo hướng dẫn người dùng toàn diện cho giao diện Streamlit với hướng dẫn tiếng Việt.

## YÊU CẦU PHÁP LÝ VIỆT NAM

Đảm bảo hệ thống giải quyết:

**Phạm vi Các Lĩnh vực Pháp lý:**
- Hiến pháp Việt Nam (Hiến pháp)
- Bộ luật Dân sự (Bộ luật Dân sự)
- Bộ luật Hình sự (Bộ luật Hình sự)
- Bộ luật Lao động (Bộ luật Lao động)
- Luật Thương mại (Luật Thương mại)
- Luật Hành chính (Luật Hành chính)
- Luật Thuế (Luật Thuế)
- Luật Bất động sản (Luật Bất động sản)

**Xử lý Ngôn ngữ Việt Nam:**
- Xử lý và token hóa văn bản tiếng Việt phù hợp
- Nhận dạng và xử lý thuật ngữ pháp lý
- Định dạng trích dẫn cho tài liệu pháp lý Việt Nam
- Hỗ trợ cho cấu trúc tài liệu pháp lý Việt Nam

**Cấu hình Pinecone:**
- Tối ưu hóa cho embedding văn bản tiếng Việt
- Lọc metadata hiệu quả cho các lĩnh vực pháp lý
- Lập chỉ mục có thể mở rộng cho bộ sưu tập tài liệu pháp lý lớn
- Mô hình lưu trữ và truy xuất hiệu quả về chi phí

## TIÊU CHUẨN CHẤT LƯỢNG

Đảm bảo tất cả mã Python đáp ứng:
- Hướng dẫn style PEP 8
- Type hints trong toàn bộ codebase
- Docstrings toàn diện
- Xử lý lỗi và ghi log
- Tối ưu hóa hiệu suất cho các thao tác Pinecone
- Thực tiễn bảo mật tốt nhất cho API keys và dữ liệu người dùng
- Kiến trúc có thể mở rộng hỗ trợ 100+ người dùng đồng thời
- Thời gian phản hồi dưới 2 giây cho truy vấn pháp lý
- >85% độ chính xác cho trả lời câu hỏi pháp lý

Tạo tất cả tài liệu như mã Python sẵn sàng production phù hợp cho triển khai doanh nghiệp với kiểm thử và tài liệu toàn diện.
```
