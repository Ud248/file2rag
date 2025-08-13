from langchain_community.document_loaders import WebBaseLoader
from typing import List
from langchain_core.documents import Document

def load_url(url: str) -> List[Document]:
    loader = WebBaseLoader(url)
    return loader.load()
