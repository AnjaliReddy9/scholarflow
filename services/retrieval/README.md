# Retrieval and ingestion service

Owns corpus ingestion (phase 1), and will own embedding and search in later phases.

## Ingestion CLI

From repository root:

```bash
make ingest-install
make ingest RUN_ID=local-dev-001
```

Artifacts are written to `data/processed/{ingest_run_id}/`.

## Layout

```
src/campusiq_retrieval/
  loaders/       Source file loading
  normalize/     Document and section normalization
  chunking/      Structure-aware chunking
  provenance/    Chunk lineage mapping
  pipeline/      Run orchestration and persistence
```

Architecture: [docs/architecture/ingestion.md](../../docs/architecture/ingestion.md).
