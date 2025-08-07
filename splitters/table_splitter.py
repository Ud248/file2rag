import pandas as pd
from langchain_core.documents import Document
from typing import List
from io import StringIO

class TableDocumentSplitter:
    def split(self, documents: List[Document]) -> List[Document]:
        chunked_docs = []

        for doc in documents:
            # Đọc CSV từ page_content (dạng chuỗi)
            df = pd.read_csv(StringIO(doc.page_content))

            for idx, row in df.iterrows():
                # Tùy chỉnh format: bạn có thể dùng to_json(), to_dict() hoặc format mô tả
                content = row.to_csv()

                chunked_docs.append(Document(
                    page_content=content,
                    metadata={**doc.metadata, "row_index": idx}
                ))

        return chunked_docs
