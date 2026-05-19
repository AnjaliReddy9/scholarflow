from scholarflow_schemas.retrieval import IndexedChunkPayload

from scholarflow_retrieval.indexing.rank import cosine_similarity
from scholarflow_retrieval.indexing.store import ScoredPoint


class InMemoryVectorStore:
    def __init__(self, collection: str) -> None:
        self._collection = collection
        self._points: dict[str, tuple[list[float], IndexedChunkPayload]] = {}
        self._dimensions: int | None = None

    @property
    def collection(self) -> str:
        return self._collection

    def ensure_collection(self, dimensions: int) -> None:
        self._dimensions = dimensions

    def upsert(self, points: list[tuple[str, list[float], IndexedChunkPayload]]) -> int:
        for chunk_id, vector, payload in points:
            if self._dimensions is not None and len(vector) != self._dimensions:
                raise ValueError("vector dimension mismatch")
            self._dimensions = len(vector)
            self._points[chunk_id] = (vector, payload)
        return len(points)

    def search(
        self,
        query_vector: list[float],
        top_k: int,
        ingest_run_id: str | None = None,
        source_type: str | None = None,
    ) -> list[ScoredPoint]:
        scored: list[ScoredPoint] = []
        for chunk_id, (vector, payload) in self._points.items():
            if ingest_run_id is not None and payload.ingest_run_id != ingest_run_id:
                continue
            if source_type is not None and payload.source_type.value != source_type:
                continue
            score = cosine_similarity(query_vector, vector)
            scored.append(
                ScoredPoint(
                    chunk_id=chunk_id,
                    score=score,
                    payload=payload,
                    vector=vector,
                )
            )
        scored.sort(key=lambda item: (-item.score, item.chunk_id))
        return scored[:top_k]

    def count(self) -> int:
        return len(self._points)
