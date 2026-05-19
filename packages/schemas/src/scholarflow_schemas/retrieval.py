from pydantic import BaseModel, Field

from scholarflow_schemas.ingestion import ChunkProvenance, SourceType


class EmbeddingRequest(BaseModel):
    texts: list[str] = Field(..., min_length=1)


class EmbeddingResponse(BaseModel):
    model_id: str
    dimensions: int
    vectors: list[list[float]]


class IndexedChunkPayload(BaseModel):
    chunk_id: str
    document_id: str
    source_reference: str
    source_uri: str
    section_title: str
    source_anchor: str
    chunk_index: int = Field(..., ge=0)
    text: str
    source_type: SourceType
    ingest_run_id: str
    lineage: list[str] = Field(default_factory=list)


class RetrievalQuery(BaseModel):
    query: str = Field(..., min_length=1)
    top_k: int = Field(default=5, ge=1, le=50)
    ingest_run_id: str | None = None
    source_type: SourceType | None = None


class EvidenceItem(BaseModel):
    evidence_id: str = Field(..., description="Stable identifier; equals chunk_id")
    chunk_id: str
    document_id: str
    source_reference: str
    section_title: str
    source_anchor: str
    score: float = Field(..., ge=0.0, le=1.0)
    text: str
    provenance: ChunkProvenance


class RetrievalTiming(BaseModel):
    embedding_ms: float
    search_ms: float
    total_ms: float


class RetrievalInstrumentationMeta(BaseModel):
    top_k: int
    candidate_count: int
    collection: str
    embedding_model_id: str


class RetrievalResponse(BaseModel):
    query: str
    results: list[EvidenceItem]
    timing: RetrievalTiming
    instrumentation: RetrievalInstrumentationMeta
