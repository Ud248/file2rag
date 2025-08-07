from langchain_community.document_loaders import CSVLoader
from typing import List
from langchain_core.documents import Document

def load_csv(file_path: str) -> List[Document]:
    loader = CSVLoader(file_path)
    return loader.load()