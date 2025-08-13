from langchain_community.document_loaders import TextLoader
from typing import List
from langchain_core.documents import Document

def load_text(file_path: str) -> List[Document]:
    loader = TextLoader(file_path)
    return loader.load()