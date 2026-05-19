from scholarflow_schemas.retrieval import RetrievalQuery, RetrievalResponse

from scholarflow_retrieval.embedding.protocol import EmbeddingProvider
from scholarflow_retrieval.indexing.store import VectorStore
from scholarflow_retrieval.observability.hooks import RetrievalInstrumentation
from scholarflow_retrieval.retrieval.semantic import semantic_retrieve


class RetrievalService:
    def __init__(
        self,
        embedder: EmbeddingProvider,
        store: VectorStore,
        instrumentation: RetrievalInstrumentation,
    ) -> None:
        self._embedder = embedder
        self._store = store
        self._instrumentation = instrumentation

    @property
    def collection(self) -> str:
        return self._store.collection

    def retrieve(self, query: RetrievalQuery) -> RetrievalResponse:
        return semantic_retrieve(
            query=query,
            embedder=self._embedder,
            store=self._store,
            instrumentation=self._instrumentation,
        )
