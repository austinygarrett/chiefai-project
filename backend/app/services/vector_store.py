import faiss
import numpy as np

class CalendarVectorStore:
    def __init__(self, dim: int = 1536):
        self.dim = dim
        self.user_indices: dict[int, tuple[faiss.IndexFlatL2, list[tuple]]] = {}

    def build_user_index(self, user_id: int, embeddings: list[list[float]], metadata: list[tuple]):
        index = faiss.IndexFlatL2(self.dim)
        index.add(np.array(embeddings).astype("float32"))
        self.user_indices[user_id] = (index, metadata)

    def search(self, user_id: int, query_vector: list[float], k: int = 5) -> list[str]:
        if user_id not in self.user_indices:
            return []

        index, metadata = self.user_indices[user_id]
        query = np.array([query_vector]).astype("float32")
        _, I = index.search(query, k)

        chunks = []
        for idx in I[0]:
            summary, status, rrule, start, end = metadata[idx]
            chunks.append(
                f"Event: {summary}\nStatus: {status}\nRecurrence: {rrule}\nFrom: {start}\nTo: {end}"
            )

        return chunks

# Singleton instance
calendar_vector_store = CalendarVectorStore()
