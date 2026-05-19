from datetime import UTC, datetime
from pathlib import Path

from scholarflow_schemas.ingestion import (
    NormalizedDocument,
    ProvenanceMetadata,
    SectionNode,
    VersionMetadata,
)

from scholarflow_retrieval.constants import PIPELINE_VERSION
from scholarflow_retrieval.ids import checksum_hex, document_id_for
from scholarflow_retrieval.loaders.raw_source import RawSource
from scholarflow_retrieval.normalize.sections import extract_markdown_sections


def normalize_document(
    raw: RawSource,
    ingest_run_id: str,
    ingested_at: datetime | None = None,
) -> NormalizedDocument:
    source_uri = raw.path.as_posix()
    content_bytes = raw.body.encode("utf-8")
    doc_id = document_id_for(source_uri, raw.source_type.value)
    section_rows = extract_markdown_sections(raw.body)
    sections = [
        SectionNode(title=row_titles[-1], level=level, anchor=anchor, body=body)
        for row_titles, body, level, anchor in section_rows
    ]
    hierarchy = section_rows[-1][0] if section_rows else ["Document"]
    return NormalizedDocument(
        document_id=doc_id,
        source_type=raw.source_type,
        title=raw.title,
        sections=sections,
        section_hierarchy=hierarchy,
        source_reference=raw.source_reference,
        ingested_at=ingested_at or datetime.now(UTC),
        version=VersionMetadata(pipeline_version=PIPELINE_VERSION),
        provenance=ProvenanceMetadata(
            source_uri=source_uri,
            ingest_run_id=ingest_run_id,
            content_checksum=checksum_hex(content_bytes),
            loader="markdown",
        ),
    )


def source_uri_for_path(path: Path) -> str:
    return path.as_posix()
