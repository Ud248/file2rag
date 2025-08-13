import pandas as pd
from langchain_core.documents import Document
from typing import List
import os

def load_xlsx(file_path: str) -> List[Document]:
    """
    Load XLSX file and return one Document per sheet (no chunking).
    Each row is formatted as key: value pairs for better readability.
    """
    documents = []
    excel_file = pd.ExcelFile(file_path)

    for sheet_name in excel_file.sheet_names:
        df = pd.read_excel(file_path, sheet_name=sheet_name).fillna("")

        rows_text = []
        for _, row in df.iterrows():
            row_text = "\n".join([f"{col}: {row[col]}" for col in df.columns])
            rows_text.append(row_text)

        doc_text = "\n\n".join(rows_text)

        documents.append(
            Document(
                page_content=doc_text,
                metadata={
                    "source": os.path.basename(file_path),
                    "file_type": "xlsx",
                    "sheet": sheet_name,
                    "total_rows": len(df),
                    "columns": list(df.columns)
                }
            )
        )

    return documents
