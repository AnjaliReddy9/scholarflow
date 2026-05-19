from scholarflow_schemas.ingestion import SourceType
from scholarflow_schemas.retrieval import IndexedChunkPayload


def sample_payload(
    chunk_id: str,
    *,
    ingest_run_id: str = "test-ingest-001",
    text: str = "sample text",
    source_reference: str = "catalog/sample",
) -> IndexedChunkPayload:
    return IndexedChunkPayload(
        chunk_id=chunk_id,
        document_id="doc_test",
        source_reference=source_reference,
        source_uri=f"data/raw/{source_reference}.md",
        section_title="Section",
        source_anchor="section",
        chunk_index=0,
        text=text,
        source_type=SourceType.COURSE_CATALOG,
        ingest_run_id=ingest_run_id,
        lineage=["section"],
    )
