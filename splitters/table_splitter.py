import math
from langchain_core.documents import Document
from typing import List

def chunk_documents_by_rows(documents: List[Document], chunk_size: int = 20) -> List[Document]:
    """
    Chunk documents by row (separated by double newlines).
    Works for CSV and XLSX loaded in key: value format.
    """
    chunked_docs = []
    for doc in documents:
        rows = doc.page_content.split("\n\n")
        num_chunks = math.ceil(len(rows) / chunk_size)

        for chunk_idx in range(num_chunks):
            start = chunk_idx * chunk_size
            end = min((chunk_idx + 1) * chunk_size, len(rows))
            chunk_text = "\n\n".join(rows[start:end])

            chunked_docs.append(
                Document(
                    page_content=chunk_text,
                    metadata={**doc.metadata, "chunk_index": chunk_idx + 1}
                )
            )

    return chunked_docs
