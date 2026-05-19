# Retrieval service

Ingestion (phase 1), embedding, vector indexing, and semantic retrieval (phase 2).

## Commands

From repository root:

```bash
make ingest RUN_ID=local-dev-001
make index RUN_ID=local-dev-001
make retrieve RUN_ID=local-dev-001 QUERY="student records access"
```

Or directly:

```bash
scholarflow-ingest ingest --ingest-run-id local-dev-001
scholarflow-index index --ingest-run-id local-dev-001
scholarflow-retrieve retrieve --ingest-run-id local-dev-001 --query "..." --json
```

Use `--in-memory` on index/retrieve for tests without Qdrant.

## Layout

```
src/scholarflow_retrieval/
  embedding/        Provider interface + local stub
  indexing/         Vector store, index pipeline
  retrieval/        Semantic search + RetrievalService
  observability/    Instrumentation hooks
  pipeline/         Ingestion (phase 1)
```

Docs: [docs/architecture/ingestion.md](../../docs/architecture/ingestion.md), [retrieval.md](../../docs/architecture/retrieval.md).
