from dataclasses import dataclass
from typing import Protocol

from scholarflow_schemas.retrieval import IndexedChunkPayload


@dataclass(frozen=True)
class ScoredPoint:
    chunk_id: str
    score: float
    payload: IndexedChunkPayload
    vector: list[float]


class VectorStore(Protocol):
    @property
    def collection(self) -> str: ...

    def ensure_collection(self, dimensions: int) -> None: ...

    def upsert(self, points: list[tuple[str, list[float], IndexedChunkPayload]]) -> int: ...

    def search(
        self,
        query_vector: list[float],
        top_k: int,
        ingest_run_id: str | None = None,
        source_type: str | None = None,
    ) -> list[ScoredPoint]: ...

    def count(self) -> int: ...
