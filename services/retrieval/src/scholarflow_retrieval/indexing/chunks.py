import json
from pathlib import Path

from scholarflow_schemas.ingestion import DocumentChunk
from scholarflow_schemas.retrieval import IndexedChunkPayload


def load_chunks_jsonl(path: Path) -> list[DocumentChunk]:
    chunks: list[DocumentChunk] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        chunks.append(DocumentChunk.model_validate(json.loads(line)))
    return chunks


def indexed_payload_from_chunk(chunk: DocumentChunk) -> IndexedChunkPayload:
    return IndexedChunkPayload(
        chunk_id=chunk.chunk_id,
        document_id=chunk.document_id,
        source_reference=chunk.source_reference,
        source_uri=chunk.provenance.source_uri,
        section_title=chunk.section_title,
        source_anchor=chunk.source_anchor,
        chunk_index=chunk.chunk_index,
        text=chunk.text,
        source_type=chunk.provenance.source_type,
        ingest_run_id=chunk.provenance.ingest_run_id,
        lineage=list(chunk.provenance.lineage),
    )
