from scholarflow_retrieval.config import RetrievalSettings
from scholarflow_retrieval.embedding.local import LocalHashEmbeddingProvider
from scholarflow_retrieval.embedding.protocol import EmbeddingProvider
from scholarflow_retrieval.indexing.memory import InMemoryVectorStore
from scholarflow_retrieval.indexing.qdrant import QdrantVectorStore
from scholarflow_retrieval.indexing.store import VectorStore
from scholarflow_retrieval.observability.hooks import LoggingRetrievalInstrumentation, RetrievalInstrumentation
from scholarflow_retrieval.retrieval.service import RetrievalService


def build_embedder(settings: RetrievalSettings) -> EmbeddingProvider:
    return LocalHashEmbeddingProvider(
        model_id=settings.embedding_model_id,
        dimensions=settings.embedding_dimensions,
    )


def build_vector_store(settings: RetrievalSettings, ingest_run_id: str, in_memory: bool = False) -> VectorStore:
    collection = settings.collection_for_run(ingest_run_id)
    if in_memory:
        return InMemoryVectorStore(collection=collection)
    return QdrantVectorStore(url=settings.vector_store_url, collection=collection)


def build_retrieval_service(
    settings: RetrievalSettings,
    ingest_run_id: str,
    in_memory: bool = False,
    instrumentation: RetrievalInstrumentation | None = None,
) -> RetrievalService:
    embedder = build_embedder(settings)
    store = build_vector_store(settings, ingest_run_id, in_memory=in_memory)
    hooks = instrumentation or LoggingRetrievalInstrumentation()
    return RetrievalService(embedder=embedder, store=store, instrumentation=hooks)
