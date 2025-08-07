from langchain_community.document_loaders import Docx2txtLoader
from typing import List
from langchain_core.documents import Document

def load_docx(file_path: str) -> List[Document]:
    loader = Docx2txtLoader(file_path)
    return loader.load()