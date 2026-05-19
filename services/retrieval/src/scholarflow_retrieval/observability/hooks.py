import logging
from dataclasses import dataclass
from typing import Protocol

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class RetrievalEvent:
    query: str
    top_k: int
    collection: str
    embedding_ms: float
    search_ms: float
    total_ms: float
    candidate_count: int
    result_count: int
    embedding_model_id: str


class RetrievalInstrumentation(Protocol):
    def on_retrieval(self, event: RetrievalEvent) -> None: ...


class LoggingRetrievalInstrumentation:
    def on_retrieval(self, event: RetrievalEvent) -> None:
        logger.info(
            "retrieval collection=%s top_k=%d embedding_ms=%.2f search_ms=%.2f "
            "candidates=%d results=%d model=%s query_len=%d",
            event.collection,
            event.top_k,
            event.embedding_ms,
            event.search_ms,
            event.candidate_count,
            event.result_count,
            event.embedding_model_id,
            len(event.query),
        )


class NoOpRetrievalInstrumentation:
    def on_retrieval(self, event: RetrievalEvent) -> None:
        return None
