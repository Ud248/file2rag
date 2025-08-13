import google.generativeai as genai
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

class GeminiEmbedder:
    def __init__(self):
        """Initialize Gemini embedder with text-embedding-004"""
        api_key=os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        genai.configure(api_key=api_key)
        self.model_name = "models/text-embedding-004"
        self.dimension = 768  # text-embedding-004 dimension
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed multiple documents for storage"""
        embeddings = []
        for text in texts:
            try:
                result = genai.embed_content(
                    model=self.model_name,
                    content=text,
                    task_type="retrieval_document"
                )
                embeddings.append(result['embedding'])
            except Exception as e:
                print(f"Error embedding document: {str(e)}")
                # Fallback với zero vector
                embeddings.append([0.0] * self.dimension)
        return embeddings
    
    def embed_query(self, query: str) -> List[float]:
        """Embed query for retrieval"""
        try:
            result = genai.embed_content(
                model=self.model_name,
                content=query,
                task_type="retrieval_query"
            )
            return result['embedding']
        except Exception as e:
            print(f"Error embedding query: {str(e)}")
            return [0.0] * self.dimension
    
    def get_dimension(self) -> int:
        """Get embedding dimension"""
        return self.dimension