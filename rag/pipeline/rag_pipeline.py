import sys
import os
from pathlib import Path
from typing import Optional
import time

sys.path.insert(0, str(Path(__file__).parent.parent))

from loaders import DocumentLoaderManager
from splitters import *
from embedders import GeminiEmbedder
from vector_stores import MilvusVectorStore

class RAGPipeline:
    def __init__(self, collection_name: str = "document"):
        """Initialize RAG Pipeline"""
        print("🚀 Initializing RAG Pipeline...")

        try:
            self.load_manager = DocumentLoaderManager()
            self.embedder = GeminiEmbedder()
            self.vector_store = MilvusVectorStore(
                collection_name=collection_name,
                dimension=self.embedder.get_dimension()
            )
            print("✅ RAG Pipeline initialized successfully!")

        except Exception as e:
            print(f"❌ Failed to initialize RAG Pipeline: {str(e)}")
            raise

    def process_document(self, file_path: str, document_id: Optional[str] = None) -> str:
        """Complete pipeline: Load -> Chunk -> Embed -> Store"""
        start_time = time.time()
        print(f"\n📄 Processing document: {file_path}")

        if not os.path.exists(file_path) and not file_path.startswith(('http://', 'https://')):
            raise FileNotFoundError(f"Document not found: {file_path}")

        try:
            # Step 1: Load documents
            print("📂 Loading document...")
            documents = self.load_manager.load(file_path)
            print(f"   Loaded {len(documents)} document sections")
            
            if not documents:
                print("⚠️ No content found in document")
                return None
            
            # Step 2: Chunk documents
            print("✂️ Chunking documents...")
            if(file_path.startswith("http://") or file_path.startswith("https://")):
                chunks = chunk_text_medium(documents)
            else:
                extension = os.path.splitext(file_path)[1].lower()
                match extension:
                    case '.csv':
                        chunks = chunk_documents_by_rows(documents)
                    case '.xlsx':
                        chunks = chunk_documents_by_rows(documents)
                    case '.docx':
                        chunks = chunk_text_medium(documents)
                    case '.pdf':
                        chunks = chunk_text_medium(documents)
                    case '.txt':
                        chunks = chunk_text_medium(documents)
                    case _:
                        raise ValueError(f"Unsupported file type: {extension}")
            print(f"   Created {len(chunks)} chunks")

            # Step 3: Prepare data for embedding
            texts = []
            metadatas = []

            for i, chunk in enumerate(chunks):
                texts.append(chunk.page_content)
                metadata = chunk.metadata.copy()
                metadata["chunk_index"] = i
                metadatas.append(metadata)

            # Step 4: Create embeddings
            print("🧠 Creating embeddings...")
            embeddings = self.embedder.embed_documents(texts)
            print(f"   Generated {len(embeddings)} embeddings")

            # Step 5: Store in vector database
            print("💾 Storing in vector database...")
            doc_id = self.vector_store.add_documents(
                texts=texts,
                embeddings=embeddings,
                metadatas=metadatas
            )

            elapsed_time = time.time() - start_time
            print(f"✅ Document processed successfully in {elapsed_time:.2f}s")
            print(f"   Document ID: {doc_id}")
            
            return doc_id
        except Exception as e:
            print(f"❌ Error processing document: {str(e)}")
            raise