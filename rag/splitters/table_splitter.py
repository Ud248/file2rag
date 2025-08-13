import math
from langchain_core.documents import Document
from typing import List

# Cấu hình cho table splitter
CHUNK_SIZE = 20  # Số hàng trên mỗi chunk

def chunk_documents_by_rows(documents: List[Document], chunk_size: int = CHUNK_SIZE) -> List[Document]:
    """
    Chunk documents by row (separated by double newlines).
    Works for CSV and XLSX loaded in key: value format.
    
    Args:
        documents: List of documents to chunk
        chunk_size: Number of rows per chunk
        
    Returns:
        List of chunked documents with enhanced metadata
    """
    chunked_docs = []
    
    for doc in documents:
        rows = doc.page_content.split("\n\n")
        num_chunks = math.ceil(len(rows) / chunk_size)

        for chunk_idx in range(num_chunks):
            start = chunk_idx * chunk_size
            end = min((chunk_idx + 1) * chunk_size, len(rows))
            chunk_text = "\n\n".join(rows[start:end])

            # Enhanced metadata
            enhanced_metadata = {
                **doc.metadata,  # Giữ metadata gốc
                "chunk_index": chunk_idx + 1,
                "total_chunks": num_chunks,
                "chunk_size": len(rows[start:end]),
                "is_complete_document": num_chunks == 1,
                "original_rows_count": len(rows),
                "splitter_type": "table_rows",
                "chunk_size_config": chunk_size
            }

            chunked_docs.append(
                Document(
                    page_content=chunk_text,
                    metadata=enhanced_metadata
                )
            )

    return chunked_docs

# Convenience functions với presets
def chunk_table_small(documents: List[Document]) -> List[Document]:
    """Small table chunks (10 rows per chunk)"""
    return chunk_documents_by_rows(documents, chunk_size=10)

def chunk_table_medium(documents: List[Document]) -> List[Document]:
    """Medium table chunks (20 rows per chunk) - DEFAULT"""
    return chunk_documents_by_rows(documents, chunk_size=CHUNK_SIZE)

def chunk_table_large(documents: List[Document]) -> List[Document]:
    """Large table chunks (50 rows per chunk)"""
    return chunk_documents_by_rows(documents, chunk_size=50)
