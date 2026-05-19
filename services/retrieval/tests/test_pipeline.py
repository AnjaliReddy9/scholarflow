import json
from datetime import UTC, datetime
from pathlib import Path

from campusiq_retrieval.pipeline.ingest import run_ingestion


def test_run_ingestion_persists_artifacts(
    raw_dir: Path,
    tmp_path: Path,
    fixture_run_id: str,
    fixture_time: datetime,
) -> None:
    manifest = run_ingestion(
        raw_dir=raw_dir,
        processed_dir=tmp_path,
        ingest_run_id=fixture_run_id,
        ingested_at=fixture_time,
    )
    assert manifest.document_count == 4
    assert manifest.chunk_count > 0

    output = tmp_path / fixture_run_id
    documents = [
        json.loads(line) for line in (output / "documents.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    chunks = [
        json.loads(line) for line in (output / "chunks.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    assert len(documents) == 4
    assert len(chunks) == manifest.chunk_count
    assert all(chunk["provenance"]["ingest_run_id"] == fixture_run_id for chunk in chunks)


def test_ingestion_is_deterministic_for_fixed_run(
    raw_dir: Path,
    tmp_path: Path,
    fixture_run_id: str,
    fixture_time: datetime,
) -> None:
    first = run_ingestion(
        raw_dir=raw_dir,
        processed_dir=tmp_path / "a",
        ingest_run_id=fixture_run_id,
        ingested_at=fixture_time,
    )
    second = run_ingestion(
        raw_dir=raw_dir,
        processed_dir=tmp_path / "b",
        ingest_run_id=fixture_run_id,
        ingested_at=fixture_time,
    )
    assert first.chunk_count == second.chunk_count
    assert first.document_count == second.document_count

    first_chunks = (tmp_path / "a" / fixture_run_id / "chunks.jsonl").read_text(encoding="utf-8")
    second_chunks = (tmp_path / "b" / fixture_run_id / "chunks.jsonl").read_text(encoding="utf-8")
    assert first_chunks == second_chunks
