from datetime import datetime
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, Field


class SourceType(StrEnum):
    COURSE_CATALOG = "course_catalog"
    SYLLABUS = "syllabus"
    FACULTY_PUBLICATION = "faculty_publication"
    UNIVERSITY_POLICY = "university_policy"


class VersionMetadata(BaseModel):
    schema_version: Literal["1"] = "1"
    pipeline_version: str = Field(..., description="Ingestion pipeline semantic version")


class ProvenanceMetadata(BaseModel):
    source_uri: str = Field(..., description="Stable URI or path to raw source")
    ingest_run_id: str
    content_checksum: str = Field(..., description="SHA-256 hex digest of normalized source bytes")
    loader: str = Field(..., description="Loader implementation identifier")


class SectionNode(BaseModel):
    title: str
    level: int = Field(..., ge=1, le=6)
    anchor: str = Field(..., description="Stable slug within the document")
    body: str = Field(default="")


class NormalizedDocument(BaseModel):
    document_id: str
    source_type: SourceType
    title: str
    sections: list[SectionNode]
    section_hierarchy: list[str] = Field(
        default_factory=list,
        description="Ordered section titles from root to leaf for navigation",
    )
    source_reference: str = Field(..., description="Human-readable source label")
    ingested_at: datetime
    version: VersionMetadata
    provenance: ProvenanceMetadata


class ChunkProvenance(BaseModel):
    document_id: str
    source_uri: str
    source_type: SourceType
    ingest_run_id: str
    section_title: str
    section_anchor: str
    chunk_index: int = Field(..., ge=0)
    lineage: list[str] = Field(
        default_factory=list,
        description="Ordered anchors from document root to this chunk",
    )


class DocumentChunk(BaseModel):
    chunk_id: str
    document_id: str
    section_title: str
    chunk_index: int = Field(..., ge=0)
    source_reference: str
    source_anchor: str
    provenance: ChunkProvenance
    text: str = Field(..., min_length=1)


class IngestionManifest(BaseModel):
    ingest_run_id: str
    started_at: datetime
    completed_at: datetime
    pipeline_version: str
    document_count: int
    chunk_count: int
    documents_path: str
    chunks_path: str
