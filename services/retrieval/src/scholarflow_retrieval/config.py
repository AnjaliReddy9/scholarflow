import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class RetrievalSettings:
    vector_store_url: str
    collection_prefix: str
    embedding_model_id: str
    embedding_dimensions: int

    def collection_for_run(self, ingest_run_id: str) -> str:
        safe = ingest_run_id.replace("/", "-")
        return f"{self.collection_prefix}_{safe}"


def load_settings() -> RetrievalSettings:
    return RetrievalSettings(
        vector_store_url=os.environ.get("SCHOLARFLOW_VECTOR_STORE_URL", "http://localhost:6333"),
        collection_prefix=os.environ.get("SCHOLARFLOW_COLLECTION_PREFIX", "scholarflow"),
        embedding_model_id=os.environ.get("SCHOLARFLOW_EMBEDDING_MODEL", "local-hash-v1"),
        embedding_dimensions=int(os.environ.get("SCHOLARFLOW_EMBEDDING_DIMENSIONS", "384")),
    )


def resolve_chunks_path(processed_dir: Path, ingest_run_id: str) -> Path:
    return processed_dir / ingest_run_id / "chunks.jsonl"
