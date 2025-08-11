from typing import List
from langchain_core.documents import Document
import os
from dotenv import load_dotenv
from utils import clean_documents_spaces
# Load environment variables from .env file at the module level
load_dotenv()

from .csv_loader import load_csv
from .docx_loader import load_docx
from .pdf_loader import load_pdf
from .text_loader import load_text
from .url_loader import load_url
from .xlsx_loader import load_xlsx

class DocumentLoaderManager:
    def __init__(self):
        # Ensure USER_AGENT is set
        if 'USER_AGENT' not in os.environ:
            os.environ['USER_AGENT'] = 'file2rag/1.0 (Document Processing Tool)'

    def load(self, file_path: str) -> List[Document]:
        if(file_path.startswith("http://") or file_path.startswith("https://")):
            documents = load_url(file_path)
        else:
            extension = os.path.splitext(file_path)[1].lower()

            match extension:
                case '.csv':
                    return load_csv(file_path)
                case '.xlsx':
                    return load_xlsx(file_path)
                case '.docx':
                    documents = load_docx(file_path)
                case '.pdf':
                    documents = load_pdf(file_path)
                case '.txt':
                    documents = load_text(file_path)
                case _:
                    raise ValueError(f"Unsupported file type: {extension}")
                
        return clean_documents_spaces(documents)
