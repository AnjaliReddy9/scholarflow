from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

from campusiq_schemas.ingestion import IngestionManifest, NormalizedDocument

from campusiq_retrieval.chunking.structure import chunks_for_document
from campusiq_retrieval.constants import PIPELINE_VERSION
from campusiq_retrieval.loaders.markdown import discover_markdown_sources
from campusiq_retrieval.normalize.document import normalize_document
from campusiq_retrieval.pipeline.persist import write_jsonl, write_manifest


def run_ingestion(
    raw_dir: Path,
    processed_dir: Path,
    ingest_run_id: str | None = None,
    ingested_at: datetime | None = None,
) -> IngestionManifest:
    started_at = ingested_at or datetime.now(UTC)
    run_id = ingest_run_id or started_at.strftime("%Y%m%dT%H%M%SZ") + "-" + uuid4().hex[:8]
    output_dir = processed_dir / run_id

    sources = discover_markdown_sources(raw_dir)
    stamp = ingested_at or started_at
    documents: list[NormalizedDocument] = [
        normalize_document(source, ingest_run_id=run_id, ingested_at=stamp) for source in sources
    ]
    chunks = [chunk for document in documents for chunk in chunks_for_document(document)]

    documents_path = output_dir / "documents.jsonl"
    chunks_path = output_dir / "chunks.jsonl"
    write_jsonl(documents_path, documents)
    write_jsonl(chunks_path, chunks)

    completed_at = ingested_at or datetime.now(UTC)
    manifest = IngestionManifest(
        ingest_run_id=run_id,
        started_at=started_at,
        completed_at=completed_at,
        pipeline_version=PIPELINE_VERSION,
        document_count=len(documents),
        chunk_count=len(chunks),
        documents_path=documents_path.as_posix(),
        chunks_path=chunks_path.as_posix(),
    )
    write_manifest(output_dir / "manifest.json", manifest)
    return manifest
