import pandas as pd
from langchain_core.documents import Document

def load_xlsx(file_path: str) -> list[Document]:
    documents = []
    excel_file = pd.ExcelFile(file_path)
    for sheet_name in excel_file.sheet_names:
        df = pd.read_excel(excel_file, sheet_name=sheet_name)

        #convert to text(similar with csv format)
        text_content = df.to_csv(index=False)

        doc = Document(
            page_content=text_content,
            metadata = {"sheet": sheet_name, "source": file_path}
        )

        documents.append(doc)

    return documents