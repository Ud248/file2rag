import re
from langchain_core.documents import Document
from typing import List

def clean_documents_spaces(documents: List[Document]) -> List[Document]:
    """
    Clean excessive whitespace from a list of LangChain Document objects.
    
    This function removes redundant spaces, tabs, and newlines in each document's 
    `page_content`, replacing them with a single space. It also trims leading and 
    trailing whitespace, preserving the document's original metadata.
    
    Args:
        docs (List[Document]): 
            List of Document objects to clean.
        
    Returns:
        List[Document]: 
            A new list of Document objects with cleaned `page_content` and 
            original metadata intact.
    """

    cleaned_docs = []
    for doc in documents:
        cleaned_page_content = re.sub(r'\s+', ' ', doc.page_content).strip()
        cleaned_docs.append(Document(
            page_content=cleaned_page_content,
            metadata=doc.metadata
        ))
    
    return cleaned_docs