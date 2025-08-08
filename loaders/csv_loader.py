import pandas as pd
from langchain_core.documents import Document
from typing import List

def load_csv(file_path: str) -> List[Document]:
    """
    Load CSV file and return a single Document (no chunking).
    Each row is formatted as key: value pairs for better readability.
    """
    try:
        df = pd.read_csv(file_path).fillna("")

        # Chuyển tất cả row thành key: value
        rows_text = []
        for _, row in df.iterrows():
            row_text = "\n".join([f"{col}: {row[col]}" for col in df.columns])
            rows_text.append(row_text)

        doc_text = "\n\n".join(rows_text)

        return [
            Document(
                page_content=doc_text,
                metadata={
                    "source": file_path,
                    "file_type": "csv",
                    "total_rows": len(df),
                    "columns": list(df.columns)
                }
            )
        ]

    except Exception as e:
        return [
            Document(
                page_content=f"Error loading CSV file: {str(e)}",
                metadata={
                    "source": file_path,
                    "file_type": "csv",
                    "error": True,
                    "error_message": str(e)
                }
            )
        ]
