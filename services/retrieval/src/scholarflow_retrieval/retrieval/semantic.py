import time

from scholarflow_schemas.ingestion import ChunkProvenance
from scholarflow_schemas.retrieval import (
    EvidenceItem,
    RetrievalInstrumentationMeta,
    RetrievalQuery,
    RetrievalResponse,
    RetrievalTiming,
)

from scholarflow_retrieval.embedding.protocol import EmbeddingProvider
from scholarflow_retrieval.indexing.store import ScoredPoint, VectorStore
from scholarflow_retrieval.observability.hooks import RetrievalEvent, RetrievalInstrumentation


def _evidence_from_point(point: ScoredPoint) -> EvidenceItem:
    payload = point.payload
    provenance = ChunkProvenance(
        document_id=payload.document_id,
        source_uri=payload.source_uri,
        source_type=payload.source_type,
        ingest_run_id=payload.ingest_run_id,
        section_title=payload.section_title,
        section_anchor=payload.source_anchor,
        chunk_index=payload.chunk_index,
        lineage=payload.lineage,
    )
    return EvidenceItem(
        evidence_id=payload.chunk_id,
        chunk_id=payload.chunk_id,
        document_id=payload.document_id,
        source_reference=payload.source_reference,
        section_title=payload.section_title,
        source_anchor=payload.source_anchor,
        score=point.score,
        text=payload.text,
        provenance=provenance,
    )


def semantic_retrieve(
    query: RetrievalQuery,
    embedder: EmbeddingProvider,
    store: VectorStore,
    instrumentation: RetrievalInstrumentation,
) -> RetrievalResponse:
    started = time.perf_counter()

    embed_started = time.perf_counter()
    query_vector = embedder.embed_query(query.query)
    embedding_ms = (time.perf_counter() - embed_started) * 1000.0

    search_started = time.perf_counter()
    source_type = query.source_type.value if query.source_type else None
    hits = store.search(
        query_vector=query_vector,
        top_k=query.top_k,
        ingest_run_id=query.ingest_run_id,
        source_type=source_type,
    )
    search_ms = (time.perf_counter() - search_started) * 1000.0
    total_ms = (time.perf_counter() - started) * 1000.0

    candidate_count = store.count()
    results = [_evidence_from_point(hit) for hit in hits]

    instrumentation.on_retrieval(
        RetrievalEvent(
            query=query.query,
            top_k=query.top_k,
            collection=store.collection,
            embedding_ms=embedding_ms,
            search_ms=search_ms,
            total_ms=total_ms,
            candidate_count=candidate_count,
            result_count=len(results),
            embedding_model_id=embedder.model_id,
        )
    )

    return RetrievalResponse(
        query=query.query,
        results=results,
        timing=RetrievalTiming(
            embedding_ms=embedding_ms,
            search_ms=search_ms,
            total_ms=total_ms,
        ),
        instrumentation=RetrievalInstrumentationMeta(
            top_k=query.top_k,
            candidate_count=candidate_count,
            collection=store.collection,
            embedding_model_id=embedder.model_id,
        ),
    )
