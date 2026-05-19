from pathlib import Path

from scholarflow_retrieval.embedding.local import LocalHashEmbeddingProvider
from scholarflow_retrieval.indexing.memory import InMemoryVectorStore
from scholarflow_retrieval.indexing.pipeline import index_chunks_file
from helpers import sample_payload


def test_memory_store_top_k_ordering() -> None:
    store = InMemoryVectorStore(collection="test-order")
    store.ensure_collection(3)
    store.upsert(
        [
            ("c-low", [0.0, 1.0, 0.0], sample_payload("c-low")),
            ("c-high", [1.0, 0.0, 0.0], sample_payload("c-high")),
            ("c-mid", [0.9, 0.1, 0.0], sample_payload("c-mid")),
        ]
    )
    hits = store.search(query_vector=[1.0, 0.0, 0.0], top_k=2)
    assert [hit.chunk_id for hit in hits] == ["c-high", "c-mid"]


def test_index_chunks_file(tmp_path: Path, raw_dir: Path, fixture_run_id: str, fixture_time) -> None:
    from scholarflow_retrieval.pipeline.ingest import run_ingestion

    manifest = run_ingestion(
        raw_dir=raw_dir,
        processed_dir=tmp_path,
        ingest_run_id=fixture_run_id,
        ingested_at=fixture_time,
    )
    chunks_path = tmp_path / manifest.ingest_run_id / "chunks.jsonl"
    store = InMemoryVectorStore(collection="test-index")
    embedder = LocalHashEmbeddingProvider(dimensions=32)
    indexed = index_chunks_file(chunks_path, embedder, store)
    assert indexed == manifest.chunk_count
    assert store.count() == manifest.chunk_count
