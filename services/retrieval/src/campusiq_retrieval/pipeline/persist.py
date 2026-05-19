import json
from pathlib import Path

from campusiq_schemas.ingestion import DocumentChunk, IngestionManifest, NormalizedDocument


def write_jsonl(path: Path, rows: list[NormalizedDocument] | list[DocumentChunk]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row.model_dump(mode="json"), ensure_ascii=False))
            handle.write("\n")


def write_manifest(path: Path, manifest: IngestionManifest) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(manifest.model_dump(mode="json"), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
