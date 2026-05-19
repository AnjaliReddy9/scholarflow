# Ingestion architecture

ScholarFlow ingestion converts markdown corpus sources into normalized documents and citation-ready chunks. The pipeline is deterministic, provenance-aware, and independent of embedding or retrieval execution.

## Pipeline stages

```
raw markdown → load → normalize document → extract sections → chunk → map provenance → persist JSONL
```

| Stage | Module | Output |
|-------|--------|--------|
| Load | `loaders/markdown.py` | `RawSource` |
| Normalize | `normalize/document.py` | `NormalizedDocument` |
| Section extract | `normalize/sections.py` | `SectionNode` list |
| Chunk | `chunking/structure.py` | `DocumentChunk` list |
| Provenance | `provenance/mapping.py` | `ChunkProvenance` on each chunk |
| Persist | `pipeline/persist.py` | `documents.jsonl`, `chunks.jsonl`, `manifest.json` |

Orchestration lives in `pipeline/ingest.py` as explicit sequential calls—no framework registry.

## Contracts

Shared Pydantic models live in `packages/schemas` (`campusiq_schemas.ingestion`):

- `NormalizedDocument` — document-level metadata and section tree
- `DocumentChunk` — retrievable unit with `chunk_id`, ordering, and provenance
- `IngestionManifest` — run summary for operational traceability

## Chunking policy

1. Split on markdown heading boundaries (`#` … `######`).
2. Never merge content across sections.
3. Within a section, merge paragraphs until `MAX_SECTION_CHARS` (2400); split on paragraph boundaries only.
4. Assign monotonic `chunk_index` per section.

Same input bytes produce the same chunk IDs and text.

## Citation and provenance

Each chunk carries:

- `source_anchor` — stable section slug
- `source_reference` — catalog label (e.g. `syllabus/cs301-spring2026`)
- `provenance.lineage` — ordered section anchors from document root
- `provenance.ingest_run_id` — ties artifacts to a single run

Future retrieval and evaluation consume these fields directly; the API does not rewrite provenance.

## Processed layout

```
data/processed/{ingest_run_id}/
  documents.jsonl
  chunks.jsonl
  manifest.json
```

Processed directories are gitignored. Rebuild by re-running ingestion.

## Out of scope (this phase)

- Embeddings and vector indexing
- Semantic splitting or token-based chunkers
- Orchestrator or LLM calls
- Incremental diff ingestion
