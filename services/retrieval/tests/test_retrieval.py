from scholarflow_schemas.retrieval import RetrievalQuery

from scholarflow_retrieval.embedding.local import LocalHashEmbeddingProvider
from scholarflow_retrieval.indexing.memory import InMemoryVectorStore
from scholarflow_retrieval.indexing.pipeline import index_chunks_file
from scholarflow_retrieval.observability.hooks import NoOpRetrievalInstrumentation
from scholarflow_retrieval.retrieval.service import RetrievalService
from helpers import sample_payload


def test_retrieval_preserves_metadata(tmp_path, raw_dir, fixture_run_id, fixture_time) -> None:
    from scholarflow_retrieval.pipeline.ingest import run_ingestion

    manifest = run_ingestion(
        raw_dir=raw_dir,
        processed_dir=tmp_path,
        ingest_run_id=fixture_run_id,
        ingested_at=fixture_time,
    )
    chunks_path = tmp_path / manifest.ingest_run_id / "chunks.jsonl"
    store = InMemoryVectorStore(collection="test-meta")
    embedder = LocalHashEmbeddingProvider(dimensions=32)
    index_chunks_file(chunks_path, embedder, store)

    service = RetrievalService(
        embedder=embedder,
        store=store,
        instrumentation=NoOpRetrievalInstrumentation(),
    )
    response = service.retrieve(
        RetrievalQuery(query="algorithms grading policy", top_k=3, ingest_run_id=fixture_run_id)
    )
    assert response.results
    first = response.results[0]
    assert first.evidence_id == first.chunk_id
    assert first.source_reference
    assert first.provenance.ingest_run_id == fixture_run_id
    assert response.instrumentation.top_k == 3
    assert response.timing.total_ms >= 0.0


def test_retrieval_is_deterministic() -> None:
    store = InMemoryVectorStore(collection="test-deterministic")
    store.ensure_collection(4)
    store.upsert(
        [
            ("a", [1.0, 0.0, 0.0, 0.0], sample_payload("a", text="alpha")),
            ("b", [0.0, 1.0, 0.0, 0.0], sample_payload("b", text="beta")),
        ]
    )
    embedder = LocalHashEmbeddingProvider(dimensions=4)
    service = RetrievalService(
        embedder=embedder,
        store=store,
        instrumentation=NoOpRetrievalInstrumentation(),
    )
    query = RetrievalQuery(query="alpha", top_k=1)
    first = service.retrieve(query)
    second = service.retrieve(query)
    assert [item.chunk_id for item in first.results] == [item.chunk_id for item in second.results]
