# 🚀 File2RAG

Hệ thống RAG (Retrieval-Augmented Generation) đơn giản và hiệu quả, giúp chuyển đổi tài liệu thành cơ sở tri thức có thể tìm kiếm bằng công nghệ vector embedding và Milvus vector database.

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

- **Python**: 3.8+
- **Milvus**: Server instance (local/cloud)
- **API Key**: Google AI Studio (cho Gemini embeddings)

### Cài đặt nhanh

```bash
# 1. Clone repository
git clone https://github.com/yourusername/file2rag.git
cd file2rag

# 2. Cài đặt dependencies
pip install -r requirements.txt

# 3. Thiết lập môi trường
# Tạo file .env và thêm API key
GEMINI_API_KEY=your_gemini_api_key_here
MILVUS_HOST=localhost
MILVUS_PORT=19530
```

### Khởi động Milvus (Docker)

```bash
# Download và chạy Milvus standalone
docker run -d --name milvus-standalone \
  -p 19530:19530 \
  -v milvus_data:/var/lib/milvus \
  milvusdb/milvus:latest

# Kiểm tra status
docker ps | grep milvus
```

## 📋 Hướng dẫn sử dụng thực tế

### 1. Sử dụng cơ bản

```python
from rag.pipeline.rag_pipeline import RAGPipeline

# Khởi tạo pipeline
rag = RAGPipeline(collection_name="my_documents")

# Xử lý tài liệu (tự động: load → chunk → embed → store)
document_id = rag.process_document("path/to/document.pdf")
print(f"✅ Processed document: {document_id}")

# Tìm kiếm (cần implement thêm search method)
# results = rag.search("Machine learning trong healthcare", k=5)
```

### 2. Xử lý các loại file khác nhau

```python
# PDF documents
doc_id = rag.process_document("research_paper.pdf")

# Word documents  
doc_id = rag.process_document("report.docx")

# Text files
doc_id = rag.process_document("notes.txt")

# CSV files (sẽ dùng table splitter)
doc_id = rag.process_document("data.csv")

# Excel files (sẽ dùng table splitter)  
doc_id = rag.process_document("spreadsheet.xlsx")

# Web URLs
doc_id = rag.process_document("https://example.com/article")
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
├── 📁 test/                          # Test suite
│   ├── test_chunkers.py
│   ├── test_embedding.py
│   ├── test_loaders.py
│   └── test_pipeline.py              # Pipeline testing
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

## 🧪 Testing

Chạy tests có sẵn:

```bash
# Test process_document với file cụ thể
python test\test_pipeline.py "path/to/file.pdf"

# Test với URL
python test\test_pipeline.py "https://example.com"

# Test với document ID custom
python test\test_pipeline.py "file.txt" --doc-id "custom_123" 

# Test multiple file types
python test\test_pipeline.py --multi

# Test error handling
python test\test_pipeline.py --errors

# Chạy tất cả tests
python test\test_pipeline.py --all
```

Test output example:
```
🧪 TESTING PROCESS_DOCUMENT FUNCTION ONLY
File: sample.pdf
Document ID: Auto-generated
======================================================================

🚀 Initializing RAG Pipeline...
✅ RAG Pipeline initialized successfully!

📄 Calling process_document('sample.pdf', 'None')...
--------------------------------------------------
📂 Loading document...
   Loaded 1 document sections
✂️ Chunking documents...
   Created 5 chunks
🧠 Creating embeddings...
   Generated 5 embeddings
💾 Storing in vector database...
Added 5 documents to test_process_doc
✅ Document processed successfully in 3.45s
   Document ID: 1234567890
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

## 🚦 Troubleshooting

### Lỗi thường gặp

**1. Milvus Connection Error**
```bash
# Kiểm tra Milvus container
docker ps | grep milvus
docker logs <milvus_container_id>

# Khởi động lại Milvus
docker run -d --name milvus-standalone -p 19530:19530 milvusdb/milvus:latest
```

**2. Gemini API Error**  
```python
# Kiểm tra API key trong .env
import os
from dotenv import load_dotenv
load_dotenv()
print(f"API Key exists: {bool(os.getenv('GEMINI_API_KEY'))}")
```

**3. File Loading Error**
```python
# Check file path và supported extensions
supported = ['.pdf', '.docx', '.txt', '.csv', '.xlsx']
file_ext = os.path.splitext(file_path)[1].lower()
print(f"Extension {file_ext} supported: {file_ext in supported}")
```

**4. Import Error**
```python
# Check sys.path trong rag_pipeline.py
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
```

### Debug Steps

1. **Test từng component**:
```bash
python -c "from rag.embedders.gemini_embedder import GeminiEmbedder; e=GeminiEmbedder(); print('Embedder OK')"
python -c "from rag.vector_stores.milvus_vector_store import MilvusVectorStore; v=MilvusVectorStore(); print('Milvus OK')"
```

2. **Check dependencies**:
```bash
pip list | grep -E "(langchain|pymilvus|google-generativeai)"
```

3. **Verbose logging**:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
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

## 🙏 Acknowledgments

- **Google AI Studio** - Gemini embeddings API
- **Milvus Team** - Vector database excellence
- **LangChain Community** - RAG inspiration
- **Vietnamese AI Community** - Support and feedback

## 📞 Support & Contact

- 🐛 **Issues**: [GitHub Issues](https://github.com/yourusername/file2rag/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/yourusername/file2rag/discussions)
- 📧 **Email**: support@file2rag.com
- 🌐 **Website**: [file2rag.com](https://file2rag.com)

---

<div align="center">

**🇻🇳 Made with ❤️ for Vietnamese AI Community**

[⭐ Star this repo](https://github.com/yourusername/file2rag) • [🐛 Report Bug](https://github.com/yourusername/file2rag/issues)