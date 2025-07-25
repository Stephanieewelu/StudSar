from src.managers.manager import StudSarManager
from sentence_transformers import SentenceTransformer
import numpy as np

class RAGConnector:
    def __init__(self, manager: StudSarManager):
        self.manager = manager
        self.memory = {}
        self.next_source_id = 1
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

    def add_document(self, file_path: str, metadata_extra: dict = None):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # For simplicity, we'll treat the entire document as one chunk.
            # In a real RAG system, you'd chunk the document into smaller pieces.
            source_id = f"doc_{self.next_source_id}"
            self.next_source_id += 1
            
            embedding = self.embedding_model.encode(content)
            
            self.memory[source_id] = {
                "content": content,
                "embedding": embedding,
                "metadata": {"file_path": file_path, **(metadata_extra if metadata_extra else {})}
            }
            return source_id
        except Exception as e:
            print(f"Error adding document: {e}")
            return None

    def query(self, query_text: str, top_k: int = 3):
        query_embedding = self.embedding_model.encode(query_text)
        
        similarities = []
        for source_id, doc_info in self.memory.items():
            doc_embedding = doc_info["embedding"]
            # Calculate cosine similarity
            similarity = np.dot(query_embedding, doc_embedding) / (np.linalg.norm(query_embedding) * np.linalg.norm(doc_embedding))
            similarities.append((similarity, doc_info))
        
        similarities.sort(key=lambda x: x[0], reverse=True);
        
        results = []
        for sim, doc_info in similarities[:top_k]:
            results.append({
                "source_id": doc_info["source_id"],
                "content": doc_info["content"],
                "metadata": doc_info["metadata"],
                "similarity": sim
            })
        
        return results

    def get_source_statistics(self):
        return {
            "total_documents": len(self.memory),
            "memory_keys": list(self.memory.keys())
        }