import faiss
import numpy as np

class CalendarVectorIndex:
    def __init__(self, dim: int = 1536):
        self.index = faiss.IndexFlatL2(dim)
        self.event_mapping = []  # list of (summary, status, rrule, start, end)

    def build_index(self, embeddings: list[list[float]], events: list[tuple]):
        vectors = np.array(embeddings).astype("float32")
        self.index.add(vectors)
        self.event_mapping = events

    def search(self, query_vector: list[float], k: int = 5) -> list[str]:
        query = np.array([query_vector]).astype("float32")
        _, I = self.index.search(query, k)
        context_chunks = []

        for idx in I[0]:
            summary, status, rrule, start, end = self.event_mapping[idx]
            chunk = (
                f"Event: {summary}\n"
                f"Status: {status}\n"
                f"Recurrence: {rrule}\n"
                f"From: {start}\n"
                f"To: {end}"
            )
            context_chunks.append(chunk)

        return context_chunks