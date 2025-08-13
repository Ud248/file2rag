# 🚀 File2RAG

Hệ thống RAG (Retrieval-Augmented Generation) đơn giản và hiệu quả, giúp chuyển đổi tài liệu thành cơ sở tri thức có thể tìm kiếm bằng công nghệ vector embedding và Milvus vector database.

## ⚡ Quick Start

```bash
# 1. Clone và cài đặt
git clone https://github.com/yourusername/file2rag.git
cd file2rag
pip install -r requirements.txt

# 2. Tạo .env file với Gemini API key
echo "GEMINI_API_KEY=your_gemini_api_key_here" > .env

# 3. Khởi động Milvus
docker run -d --name milvus-standalone -p 19530:19530 milvusdb/milvus:v2.3.3

# 4. Xử lý document đầu tiên
python -c "
from rag.pipeline.rag_pipeline import RAGPipeline
rag = RAGPipeline(collection_name='demo')
doc_id = rag.process_document('your_document.pdf')
print(f'✅ Processed: {doc_id}')
"
```

## 📖 Demo nhanh

### Xử lý file PDF:
```python
from rag.pipeline.rag_pipeline import RAGPipeline

# Khởi tạo và xử lý document
rag = RAGPipeline(collection_name="my_docs")
doc_id = rag.process_document("report.pdf")

# Output:
# 🚀 Initializing RAG Pipeline...
# ✅ RAG Pipeline initialized successfully!
# 📄 Processing document: report.pdf
# 📂 Loading document... (2.1s)
# ✂️ Chunking documents... (0.3s)
# 🧠 Creating embeddings... (8.7s)
# 💾 Storing in vector database... (1.2s)
# ✅ Document processed successfully in 12.34s
```

### Batch processing:
```python
files = ["doc1.pdf", "data.csv", "notes.txt", "sheet.xlsx"]
for file in files:
    doc_id = rag.process_document(file)
    print(f"✅ {file} → {doc_id}")
```

## ✨ Tính năng chính

- **📄 Hỗ trợ đa định dạng**: PDF, DOCX, TXT, CSV, XLSX và URL web
- **🧠 Text Chunking thông minh**: Tự động chọn chiến lược phù hợp cho từng loại tài liệu
- **🔍 Tìm kiếm vector**: Powered by Google Gemini text-embedding-004 (768 dimensions)
- **💾 Milvus Vector Database**: Lưu trữ và tìm kiếm COSINE similarity hiệu suất cao
- **⚡ Pipeline tự động**: Load → Chunk → Embed → Store trong một lệnh
- **🔧 Chunking linh hoạt**: Cấu hình chunk size cho text và table data
- **🧹 Text preprocessing**: Tự động làm sạch excessive whitespace

## 🏗️ Kiến trúc đơn giản

```
📄 Documents → 📥 Loaders → ✂️ Splitters → 🧠 Gemini Embedder → 💾 Milvus Store
```

### Thành phần thực tế

| Module | Implementation | Hỗ trợ |
|--------|----------------|---------|
| **Loaders** | LangChain document loaders | PyPDF, Docx2txt, TextLoader, WebBaseLoader |
| **Splitters** | RecursiveCharacterTextSplitter + Table splitter | Text (1000 chars) + Table (20 rows) |
| **Embedders** | Google Gemini text-embedding-004 | 768-dim vectors, retrieval_document/query |
| **Vector Store** | Milvus with COSINE metric | IVF_FLAT index, auto schema |
| **Pipeline** | RAGPipeline class | Automatic processing workflow |
| **Utils** | Text cleaner | Regex-based whitespace normalization |

## 🚀 Cài đặt và sử dụng

### Yêu cầu hệ thống

- **Python**: 3.8+ (khuyến nghị 3.9+)
- **Docker**: Để chạy Milvus server
- **Memory**: Tối thiểu 4GB RAM (8GB+ khuyến nghị)
- **Disk**: 2GB+ dung lượng trống

### Bước 1: Cài đặt dự án

```bash
# Clone repository
git clone https://github.com/yourusername/file2rag.git
cd file2rag

# Tạo virtual environment (khuyến nghị)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Cài đặt dependencies
pip install -r requirements.txt
```

### Bước 2: Lấy Gemini API Key

1. Truy cập [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Đăng nhập với Google account
3. Tạo API key mới
4. Copy API key để sử dụng

### Bước 3: Cấu hình môi trường

```bash
# Tạo file .env trong thư mục gốc của project
echo "GEMINI_API_KEY=your_actual_api_key_here" > .env
echo "MILVUS_HOST=localhost" >> .env
echo "MILVUS_PORT=19530" >> .env

# Kiểm tra file .env
cat .env
```

### Bước 4: Khởi động Milvus

Xem phần **Khởi động Milvus (Docker)** bên dưới để có hướng dẫn chi tiết.

### Bước 5: Test installation

```python
# Test script - tạo file test_installation.py
import os
from dotenv import load_dotenv

print("🧪 Testing File2RAG installation...")

# Test 1: Environment variables
load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
print(f"✅ Gemini API key loaded: {'Yes' if api_key else 'No'}")

# Test 2: Milvus connection
try:
    from pymilvus import connections
    connections.connect("default", host="localhost", port="19530")
    print("✅ Milvus connection: Success")
    connections.disconnect("default")
except Exception as e:
    print(f"❌ Milvus connection: Failed - {e}")

# Test 3: Gemini API
try:
    import google.generativeai as genai
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('models/text-embedding-004')
    print("✅ Gemini API: Success")
except Exception as e:
    print(f"❌ Gemini API: Failed - {e}")

# Test 4: RAG Pipeline
try:
    from rag.pipeline.rag_pipeline import RAGPipeline
    print("✅ RAG Pipeline import: Success")
except Exception as e:
    print(f"❌ RAG Pipeline import: Failed - {e}")

print("\n🎉 Installation test completed!")
```

Chạy test:
```bash
python test_installation.py
```

### Khởi động Milvus (Docker)

#### Phương pháp 1: Milvus Standalone (Đơn giản - Khuyến nghị)

```bash
# Bước 1: Pull và chạy Milvus standalone
docker run -d \
  --name milvus-standalone \
  --security-opt seccomp:unconfined \
  -p 19530:19530 \
  -p 9091:9091 \
  -v ${PWD}/volumes/milvus:/var/lib/milvus \
  milvusdb/milvus:v2.3.3

# Bước 2: Kiểm tra container đã chạy
docker ps | findstr milvus

# Bước 3: Kiểm tra logs
docker logs milvus-standalone

# Bước 4: Test kết nối
python -c "from pymilvus import connections; connections.connect('default', host='localhost', port='19530'); print('✅ Milvus connected successfully!')"
```

#### Phương pháp 2: Docker Compose (Production)

Tạo file `docker-compose.yml`:

```yaml
version: '3.5'

services:
  etcd:
    container_name: milvus-etcd
    image: quay.io/coreos/etcd:v3.5.5
    environment:
      - ETCD_AUTO_COMPACTION_MODE=revision
      - ETCD_AUTO_COMPACTION_RETENTION=1000
      - ETCD_QUOTA_BACKEND_BYTES=4294967296
      - ETCD_SNAPSHOT_COUNT=50000
    volumes:
      - ${DOCKER_VOLUME_DIRECTORY:-.}/volumes/etcd:/etcd
    command: etcd -advertise-client-urls=http://127.0.0.1:2379 -listen-client-urls http://0.0.0.0:2379 --data-dir /etcd
    healthcheck:
      test: ["CMD", "etcdctl", "endpoint", "health"]
      interval: 30s
      timeout: 20s
      retries: 3

  minio:
    container_name: milvus-minio
    image: minio/minio:RELEASE.2023-03-20T20-16-18Z
    environment:
      MINIO_ACCESS_KEY: minioadmin
      MINIO_SECRET_KEY: minioadmin
    ports:
      - "9001:9001"
      - "9000:9000"
    volumes:
      - ${DOCKER_VOLUME_DIRECTORY:-.}/volumes/minio:/minio_data
    command: minio server /minio_data --console-address ":9001"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9000/minio/health/live"]
      interval: 30s
      timeout: 20s
      retries: 3

  milvus:
    container_name: milvus-standalone
    image: milvusdb/milvus:v2.3.3
    command: ["milvus", "run", "standalone"]
    environment:
      ETCD_ENDPOINTS: etcd:2379
      MINIO_ADDRESS: minio:9000
    volumes:
      - ${DOCKER_VOLUME_DIRECTORY:-.}/volumes/milvus:/var/lib/milvus
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9091/healthz"]
      interval: 30s
      start_period: 90s
      timeout: 20s
      retries: 3
    ports:
      - "19530:19530"
      - "9091:9091"
    depends_on:
      - "etcd"
      - "minio"
```

Chạy với Docker Compose:
```bash
docker-compose up -d
```

#### Troubleshooting Milvus

```bash
# Kiểm tra các container đang chạy
docker ps -a

# Xem logs của Milvus
docker logs milvus-standalone -f

# Restart Milvus nếu cần
docker restart milvus-standalone

# Dọn dẹp và khởi động lại
docker stop milvus-standalone
docker rm milvus-standalone
# Chạy lại lệnh docker run ở trên

# Test kết nối từ Python
python -c "
from pymilvus import connections, utility
try:
    connections.connect('default', host='localhost', port='19530')
    print('✅ Kết nối Milvus thành công!')
    print(f'Server version: {utility.get_server_version()}')
except Exception as e:
    print(f'❌ Lỗi kết nối: {e}')
"
```

## 📋 Hướng dẫn sử dụng thực tế

### Chuẩn bị environment

```bash
# 1. Tạo file .env trong thư mục dự án
echo "GEMINI_API_KEY=your_gemini_api_key_here" > .env
echo "MILVUS_HOST=localhost" >> .env
echo "MILVUS_PORT=19530" >> .env

# 2. Cài đặt Python dependencies
pip install -r requirements.txt

# 3. Khởi động Milvus (xem phần trên)
```

### Ví dụ 1: Xử lý file PDF đơn giản

```python
import os
from dotenv import load_dotenv
from rag.pipeline.rag_pipeline import RAGPipeline

# Load environment variables
load_dotenv()

# Khởi tạo pipeline với collection name
rag = RAGPipeline(collection_name="my_research_papers")

# Xử lý file PDF
document_id = rag.process_document("./data/machine_learning_paper.pdf")
print(f"✅ Document processed with ID: {document_id}")

# Output mẫu:
# 🚀 Initializing RAG Pipeline...
# ✅ RAG Pipeline initialized successfully!
# 
# 📄 Processing document: ./data/machine_learning_paper.pdf
# 📂 Loading document...
#    Loaded 15 document sections  
# ✂️ Chunking documents...
#    Created 47 chunks
# 🧠 Creating embeddings...
#    Generated 47 embeddings
# 💾 Storing in vector database...
# ✅ Document processed successfully in 12.34s
#    Document ID: doc_1703123456789
```

### Ví dụ 2: Xử lý nhiều loại file

```python
from rag.pipeline.rag_pipeline import RAGPipeline

# Khởi tạo pipeline cho collection khác nhau
knowledge_base = RAGPipeline(collection_name="company_knowledge")

# Xử lý các loại file khác nhau
files_to_process = [
    "./documents/company_handbook.pdf",      # PDF document
    "./documents/employee_data.csv",         # CSV table  
    "./documents/quarterly_report.docx",     # Word document
    "./documents/meeting_notes.txt",         # Text file
    "./documents/budget_2024.xlsx",          # Excel spreadsheet
    "https://company.com/blog/new-policy"    # Web URL
]

processed_docs = []
for file_path in files_to_process:
    try:
        doc_id = knowledge_base.process_document(file_path)
        processed_docs.append({
            'file': file_path,
            'document_id': doc_id,
            'status': 'success'
        })
        print(f"✅ Processed: {file_path}")
    except Exception as e:
        processed_docs.append({
            'file': file_path,
            'document_id': None,
            'status': 'failed',
            'error': str(e)
        })
        print(f"❌ Failed: {file_path} - {e}")

# In kết quả
for doc in processed_docs:
    print(f"File: {doc['file']}")
    print(f"Status: {doc['status']}")
    if doc['status'] == 'success':
        print(f"Document ID: {doc['document_id']}")
    else:
        print(f"Error: {doc['error']}")
    print("-" * 50)
```

### Ví dụ 3: Xử lý và kiểm tra dữ liệu trong Milvus

```python
from rag.pipeline.rag_pipeline import RAGPipeline
from pymilvus import connections, Collection

# Khởi tạo pipeline
rag = RAGPipeline(collection_name="document_store")

# Xử lý document
doc_id = rag.process_document("./sample.pdf")

# Kết nối trực tiếp với Milvus để kiểm tra dữ liệu
connections.connect("default", host="localhost", port="19530")
collection = Collection("document_store")

# Kiểm tra thông tin collection
print(f"Collection name: {collection.name}")
print(f"Collection entities: {collection.num_entities}")
print(f"Collection schema: {collection.schema}")

# Load collection để có thể query
collection.load()

# Tìm kiếm vector tương tự (demo - cần embedding của query)
# search_results = collection.search(
#     data=[query_embedding],  # Cần tạo embedding cho query
#     anns_field="embedding",
#     param={"metric_type": "COSINE", "params": {"nprobe": 10}},
#     limit=5,
#     output_fields=["content", "source", "page"]
# )
```

### 3. Chunking strategies được áp dụng tự động

```python
# Text files (.pdf, .docx, .txt, URLs): chunk_text_medium
# - Chunk size: 1000 characters
# - Overlap: 200 characters  
# - Splitter: RecursiveCharacterTextSplitter

# Table files (.csv, .xlsx): chunk_documents_by_rows  
# - Chunk size: 20 rows per chunk
# - Split by double newlines (\n\n)
```

### 4. Vector store operations

```python
# Dữ liệu được lưu trong Milvus với schema:
# - id: INT64 (auto-generated primary key)
# - embedding: FLOAT_VECTOR (768 dimensions)
# - content: VARCHAR(65535) 
# - source: VARCHAR(1000)
# - page: INT64
# - content_type: VARCHAR(100)
# - chunk_index: INT64

# Index: IVF_FLAT với COSINE similarity
```

## 🔧 Cấu hình và customization

### Text Splitter Settings

```python
# File: rag/splitters/text_splitter.py
CHUNK_SIZE = 1000  # Characters per chunk
CHUNK_OVERLAP = 200  # Overlap between chunks

# Presets có sẵn:
chunk_text_small(documents)   # 500 chars, 100 overlap
chunk_text_medium(documents)  # 1000 chars, 200 overlap  
chunk_text_large(documents)   # 2000 chars, 400 overlap
```

### Table Splitter Settings

```python
# File: rag/splitters/table_splitter.py  
CHUNK_SIZE = 20  # Rows per chunk

# Presets có sẵn:
chunk_table_small(documents)   # 10 rows per chunk
chunk_table_medium(documents)  # 20 rows per chunk
chunk_table_large(documents)   # 50 rows per chunk
```

### Gemini Embedder Configuration

```python
# File: rag/embedders/gemini_embedder.py
model_name = "models/text-embedding-004"
dimension = 768
task_type = "retrieval_document" hoặc "retrieval_query"
```

### Milvus Vector Store Schema

```python
# Auto-created schema trong MilvusVectorStore:
fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=768),
    FieldSchema(name="content", dtype=DataType.VARCHAR, max_length=65535),
    FieldSchema(name="source", dtype=DataType.VARCHAR, max_length=1000),
    FieldSchema(name="page", dtype=DataType.INT64),
    FieldSchema(name="content_type", dtype=DataType.VARCHAR, max_length=100),
    FieldSchema(name="chunk_index", dtype=DataType.INT64)
]
```

## 📁 Cấu trúc dự án thực tế

```
file2rag/
├── 📁 rag/                           # Core RAG modules
│   ├── 📁 embedders/                 # AI embedding providers  
│   │   ├── __init__.py
│   │   └── gemini_embedder.py        # Google Gemini text-embedding-004
│   ├── 📁 loaders/                   # Document loaders
│   │   ├── __init__.py
│   │   ├── manager.py                # DocumentLoaderManager class
│   │   ├── pdf_loader.py             # PyPDFLoader wrapper
│   │   ├── docx_loader.py            # Docx2txtLoader wrapper
│   │   ├── text_loader.py            # TextLoader wrapper
│   │   ├── csv_loader.py             # Pandas-based CSV loader
│   │   ├── xlsx_loader.py            # Pandas-based Excel loader
│   │   └── url_loader.py             # WebBaseLoader wrapper
│   ├── 📁 splitters/                 # Text chunking strategies
│   │   ├── __init__.py
│   │   ├── text_splitter.py          # RecursiveCharacterTextSplitter
│   │   └── table_splitter.py         # Row-based table splitting
│   ├── 📁 vector_stores/             # Vector database interfaces
│   │   ├── __init__.py
│   │   └── milvus_vector_store.py    # Milvus client wrapper
│   └── 📁 pipeline/                  # Main pipeline
│       └── rag_pipeline.py           # RAGPipeline class
├── 📁 utils/                         # Utility functions
│   ├── __init__.py
│   └── text_cleaner.py               # Regex-based text cleaning
├── 📄 requirements.txt               # Python dependencies
└── 📄 README.md                     # Tài liệu này
```

### Key Dependencies

```pip-requirements
# Core framework
langchain-community     # Document loaders
langchain-core         # Document classes
langchain             # Text splitters

# Document processing
docx2txt              # DOCX extraction
pypdf                 # PDF processing  
pandas                # CSV/Excel handling
openpyxl              # Excel support
beautifulsoup4        # Web scraping
requests              # HTTP requests

# AI & Vector DB
google-generativeai   # Gemini embeddings
pymilvus              # Milvus client

# Environment
python-dotenv         # .env file support
```


## 📊 Hiệu suất và giới hạn

### Processing Performance

| Operation | Typical Time | Notes |
|-----------|-------------|-------|
| PDF Loading (10 pages) | ~2-5s | Depends on PDF complexity |
| Text Chunking | ~100-500ms | For 1000 chars/chunk |
| Gemini Embedding | ~300-800ms per request | Rate limited by API |
| Milvus Storage | ~50-200ms | Per batch of chunks |
| Vector Search | <100ms | For top-k retrieval |

### Current Limitations

- **No search interface**: Chỉ có process_document, chưa có search method
- **No batch embedding**: Embed từng chunk riêng lẻ 
- **Limited error handling**: Basic exception catching
- **No persistence**: Không save/load pipeline state
- **Memory usage**: Không tối ưu cho large documents
- **API rate limits**: Gemini API có giới hạn requests/minute

### Chunking Behavior

```python
# Text files (.pdf, .docx, .txt, URLs):
# - RecursiveCharacterTextSplitter
# - Default: 1000 chars, 200 overlap
# - Separators: ["\n\n", "\n", " ", ""]

# Table files (.csv, .xlsx):  
# - Split by rows (double newlines)
# - Default: 20 rows per chunk
# - Format: key:value pairs per row
```

### 🚦 Lỗi thường gặp và cách khắc phục

#### 1. Lỗi kết nối Milvus

**Lỗi:** `pymilvus.exceptions.MilvusException: <MilvusException: (code=1, message=Fail connecting to server on localhost:19530...)`

**Nguyên nhân & Khắc phục:**
```bash
# Kiểm tra Milvus container
docker ps | findstr milvus

# Nếu không có container nào, khởi động Milvus
docker run -d --name milvus-standalone -p 19530:19530 -p 9091:9091 milvusdb/milvus:v2.3.3

# Nếu container đã tồn tại nhưng stopped
docker start milvus-standalone

# Kiểm tra logs để debug
docker logs milvus-standalone --tail 50

# Test kết nối
python -c "from pymilvus import connections; connections.connect('default', host='localhost', port='19530'); print('✅ Connected!')"
```

#### 2. Lỗi Gemini API

**Lỗi:** `google.api_core.exceptions.Unauthorized: 401 API_KEY_INVALID`

**Nguyên nhân & Khắc phục:**
```bash
# Kiểm tra API key trong .env file
cat .env | findstr GEMINI_API_KEY

# Tạo API key mới tại: https://aistudio.google.com/app/apikey
# Thêm vào .env file:
echo "GEMINI_API_KEY=your_actual_api_key_here" > .env

# Test API key
python -c "
import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
print('✅ Gemini API key valid!')
"
```

#### 3. Lỗi import modules

**Lỗi:** `ModuleNotFoundError: No module named 'rag.loaders'`

**Nguyên nhân & Khắc phục:**
```python
# Trong rag_pipeline.py, đảm bảo có:
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Hoặc chạy từ thư mục gốc của project:
cd /path/to/file2rag
python -c "from rag.pipeline.rag_pipeline import RAGPipeline; print('✅ Import successful!')"
```

#### 4. Lỗi xử lý file

**Lỗi:** `FileNotFoundError: Document not found: document.pdf`

**Khắc phục:**
```python
import os

file_path = "document.pdf"
print(f"File exists: {os.path.exists(file_path)}")
print(f"Absolute path: {os.path.abspath(file_path)}")

# Sử dụng đường dẫn tuyệt đối
full_path = os.path.abspath(file_path)
doc_id = rag.process_document(full_path)
```

#### 5. Lỗi memory với file lớn

**Lỗi:** `MemoryError` hoặc quá trình xử lý quá chậm

**Khắc phục:**
```python
# Điều chỉnh chunk size nhỏ hơn
from rag.splitters.text_splitter import chunk_text_small

# Hoặc tùy chỉnh chunk size
from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,      # Giảm từ 1000
    chunk_overlap=50,    # Giảm từ 200
    length_function=len,
)
```

#### 6. Lỗi encoding với file text

**Lỗi:** `UnicodeDecodeError: 'utf-8' codec can't decode byte...`

**Khắc phục:**
```python
# Kiểm tra encoding của file
import chardet

with open("file.txt", "rb") as f:
    encoding = chardet.detect(f.read())
    print(f"Detected encoding: {encoding}")

# Convert sang UTF-8 nếu cần
with open("file.txt", "r", encoding="latin-1") as f:
    content = f.read()
    
with open("file_utf8.txt", "w", encoding="utf-8") as f:
    f.write(content)
```

#### 7. Performance issues

**Vấn đề:** Xử lý file quá chậm

**Tối ưu hóa:**
```python
# 1. Giảm chunk size
# 2. Batch embedding (cần implement)
# 3. Parallel processing (future feature)

# Monitor performance
import time
start = time.time()
doc_id = rag.process_document("large_file.pdf")
print(f"Processing time: {time.time() - start:.2f}s")

# Ước tính thời gian cho file lớn:
# - 1MB PDF: ~5-10 giây
# - 10MB PDF: ~30-60 giây  
# - 100MB file: có thể mất vài phút
``` 
## 📝 Development Notes

### Current Implementation Status

✅ **Hoàn thành:**
- Document loaders cho 6 định dạng (PDF, DOCX, TXT, CSV, XLSX, URL)
- Text và table splitters với presets
- Gemini embedder integration
- Milvus vector store với auto schema
- End-to-end pipeline workflow
- Basic text cleaning utilities
- Test framework cho pipeline

🔄 **Cần hoàn thiện:**
- Search/retrieval interface (chỉ có embedding/storage)
- Batch processing optimization  
- Advanced filtering và metadata queries
- Performance monitoring
- Error recovery mechanisms
- Documentation examples với real data

### Code Structure Notes

- **Loaders**: Wrapper functions around LangChain loaders
- **Splitters**: Preset configurations, easily customizable
- **Pipeline**: Single `process_document()` method handles full workflow
- **Vector Store**: Auto-creates schema, COSINE similarity default
- **Utils**: Minimal text preprocessing (whitespace cleaning)

### Next Development Steps

1. Implement search/retrieval methods
2. Add batch embedding support  
3. Improve error handling và retry logic
4. Add performance metrics và monitoring
5. Create web interface hoặc API endpoints
6. Add support for more embedding models

## 📄 License

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) for details.