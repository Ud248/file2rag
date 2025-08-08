from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from typing import List

# Cấu hình cho text splitter
CHUNK_SIZE = 1000  # Số ký tự trên mỗi chunk
CHUNK_OVERLAP = 200  # Số ký tự overlap giữa các chunk

def chunk_documents_by_text(documents: List[Document], chunk_size: int = CHUNK_SIZE, chunk_overlap: int = CHUNK_OVERLAP) -> List[Document]:
    """
    Chunk documents using LangChain's RecursiveCharacterTextSplitter with enhanced metadata.
    
    Args:
        documents: List of documents to chunk
        chunk_size: Number of characters per chunk
        chunk_overlap: Number of characters to overlap between chunks
        
    Returns:
        List of chunked documents with enhanced metadata
    """
    # Sử dụng RecursiveCharacterTextSplitter của LangChain
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]  # Ưu tiên split theo paragraph, line, space
    )
    
    chunked_docs = []
    
    for doc in documents:
        # Split document thành chunks
        chunks = text_splitter.split_documents([doc])
        
        # Thêm metadata chi tiết cho từng chunk
        for chunk_idx, chunk in enumerate(chunks):
            # Enhanced metadata
            enhanced_metadata = {
                **doc.metadata,  # Giữ metadata gốc
                "chunk_index": chunk_idx + 1,
                "total_chunks": len(chunks),
                "chunk_size": len(chunk.page_content),
                "is_complete_document": len(chunks) == 1,
                "original_text_length": len(doc.page_content),
                "splitter_type": "recursive_character",
                "chunk_overlap_config": chunk_overlap
            }
            
            chunk.metadata = enhanced_metadata
            chunked_docs.append(chunk)
    
    return chunked_docs

def chunk_documents_by_sentences(documents: List[Document], chunk_size: int = 1000, chunk_overlap: int = 200) -> List[Document]:
    """
    Chunk documents by sentences using RecursiveCharacterTextSplitter with sentence separators.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=[". ", "! ", "? ", "\n\n", "\n", " ", ""]  # Ưu tiên split theo câu
    )
    
    chunked_docs = []
    
    for doc in documents:
        chunks = text_splitter.split_documents([doc])
        
        for chunk_idx, chunk in enumerate(chunks):
            enhanced_metadata = {
                **doc.metadata,
                "chunk_index": chunk_idx + 1,
                "total_chunks": len(chunks),
                "chunk_size": len(chunk.page_content),
                "is_complete_document": len(chunks) == 1,
                "original_text_length": len(doc.page_content),
                "splitter_type": "sentence_aware",
                "chunk_overlap_config": chunk_overlap
            }
            
            chunk.metadata = enhanced_metadata
            chunked_docs.append(chunk)
    
    return chunked_docs

def chunk_documents_by_paragraphs(documents: List[Document], chunk_size: int = 2000, chunk_overlap: int = 400) -> List[Document]:
    """
    Chunk documents by paragraphs using RecursiveCharacterTextSplitter with paragraph separators.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""]  # Ưu tiên split theo đoạn văn
    )
    
    chunked_docs = []
    
    for doc in documents:
        chunks = text_splitter.split_documents([doc])
        
        for chunk_idx, chunk in enumerate(chunks):
            enhanced_metadata = {
                **doc.metadata,
                "chunk_index": chunk_idx + 1,
                "total_chunks": len(chunks),
                "chunk_size": len(chunk.page_content),
                "is_complete_document": len(chunks) == 1,
                "original_text_length": len(doc.page_content),
                "splitter_type": "paragraph_aware",
                "chunk_overlap_config": chunk_overlap
            }
            
            chunk.metadata = enhanced_metadata
            chunked_docs.append(chunk)
    
    return chunked_docs

# Convenience functions với presets
def chunk_text_small(documents: List[Document]) -> List[Document]:
    """Small text chunks (500 chars, 100 overlap)"""
    return chunk_documents_by_text(documents, chunk_size=500, chunk_overlap=100)

def chunk_text_medium(documents: List[Document]) -> List[Document]:
    """Medium text chunks (1000 chars, 200 overlap) - DEFAULT"""
    return chunk_documents_by_text(documents, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)

def chunk_text_large(documents: List[Document]) -> List[Document]:
    """Large text chunks (2000 chars, 400 overlap)"""
    return chunk_documents_by_text(documents, chunk_size=2000, chunk_overlap=400)

# Advanced splitter cho code, markdown, etc.
def chunk_documents_by_code(documents: List[Document], chunk_size: int = 1500, chunk_overlap: int = 300) -> List[Document]:
    """
    Chunk code documents with code-aware separators.
    """
    from langchain.text_splitter import Language, RecursiveCharacterTextSplitter
    
    # Code-aware splitter
    text_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.PYTHON,  # Có thể config theo file type
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    
    chunked_docs = []
    
    for doc in documents:
        chunks = text_splitter.split_documents([doc])
        
        for chunk_idx, chunk in enumerate(chunks):
            enhanced_metadata = {
                **doc.metadata,
                "chunk_index": chunk_idx + 1,
                "total_chunks": len(chunks),
                "chunk_size": len(chunk.page_content),
                "is_complete_document": len(chunks) == 1,
                "original_text_length": len(doc.page_content),
                "splitter_type": "code_aware",
                "chunk_overlap_config": chunk_overlap
            }
            
            chunk.metadata = enhanced_metadata
            chunked_docs.append(chunk)
    
    return chunked_docs