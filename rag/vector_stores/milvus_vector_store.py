from pymilvus import connections, Collection, CollectionSchema, FieldSchema, DataType, utility
from typing import List, Dict, Any, Optional
import os
from dotenv import load_dotenv

load_dotenv()

class MilvusVectorStore:
    def __init__(self, collection_name: str = "documents", dimension: int = 768):
        """Initialize Milvus vector store"""
        self.collection_name = collection_name
        self.dimension = dimension
        
        # Connect to Milvus
        connections.connect(
            alias="default",
            host=os.getenv("MILVUS_HOST", "localhost"),
            port=os.getenv("MILVUS_PORT", "19530")
        )
        
        # Create collection if not exists
        self._create_collection()
    
    def _create_collection(self):
        """Create collection with schema"""
        if utility.has_collection(self.collection_name):
            self.collection = Collection(self.collection_name)
            return
        
        # Define schema
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=self.dimension),
            FieldSchema(name="content", dtype=DataType.VARCHAR, max_length=65535),
            FieldSchema(name="source", dtype=DataType.VARCHAR, max_length=1000),
            FieldSchema(name="page", dtype=DataType.INT64),
            FieldSchema(name="content_type", dtype=DataType.VARCHAR, max_length=100),
            FieldSchema(name="chunk_index", dtype=DataType.INT64)
        ]
        
        schema = CollectionSchema(fields, f"Collection for {self.collection_name}")
        self.collection = Collection(self.collection_name, schema)
        
        # Create index for vector field
        index_params = {
            "metric_type": "COSINE",
            "index_type": "IVF_FLAT",
            "params": {"nlist": 128}
        }
        self.collection.create_index("embedding", index_params)
        print(f"Created collection: {self.collection_name}")
    
    def add_documents(self, 
                     texts: List[str], 
                     embeddings: List[List[float]], 
                     metadatas: List[Dict[str, Any]]):
        """Add documents to collection"""
        for text, embedding, metadata in zip(texts, embeddings, metadatas):
            data = {
                "embedding": embedding,
                "content": text[:65535],  # Truncate if too long
                "source": metadata.get("source", ""),
                "page": metadata.get("page", 0),
                "content_type": metadata.get("content_type", "text"),
                "chunk_index": metadata.get("chunk_index", 0)
            }
            self.collection.insert(data)
            self.collection.flush()
        print(f"Added {len(texts)} documents to {self.collection_name}")