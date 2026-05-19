# ScholarFlow

Self-hosted academic intelligence and agentic RAG platform for universities. Monorepo with explicit service boundaries, typed contracts, deterministic ingestion, and provenance-aware semantic retrieval.

## Purpose

ScholarFlow demonstrates production-style Applied AI engineering: retrieval pipelines with measurable quality, citation traceability, evaluation hooks, and a path to agentic orchestration and self-hosted inference. Internal platform code—not a chatbot wrapper.

## Architecture summary

| Layer | Responsibility |
|-------|----------------|
| `apps/web` | Angular client; query submission and citation display |
| `apps/api` | FastAPI gateway; request validation, routing, error mapping |
| `services/retrieval` | Ingestion, embedding, vector index, semantic search |
| `services/orchestrator` | Agent workflow (planned) |
| `services/evaluation` | Golden-set runs (planned) |
| `services/inference` | OpenAI-compatible provider (planned) |
| `packages/schemas` | Shared Pydantic models |

See [docs/architecture/overview.md](docs/architecture/overview.md), [ingestion.md](docs/architecture/ingestion.md), [retrieval.md](docs/architecture/retrieval.md).

## Current phase

| Phase | Status |
|-------|--------|
| 0 — Foundation | Complete |
| 1 — Ingestion | Complete |
| 2 — Retrieval | **Complete** — embedding abstraction, vector index, semantic search, instrumentation |
| 3 — Orchestration + inference | Planned |
| 4 — Evaluation + CI gates | Planned |
| 5+ | Observability, self-hosted inference |

## Retrieval lifecycle

1. **Ingest** — markdown corpus → normalized chunks (`data/processed/{run_id}/`)
2. **Index** — embed chunks → Qdrant collection `scholarflow_{run_id}`
3. **Retrieve** — query embedding → top-k evidence with scores and provenance

```bash
make infra-up
make ingest RUN_ID=local-dev-001
make index RUN_ID=local-dev-001
make retrieve RUN_ID=local-dev-001 QUERY="academic integrity policy"
```

### Semantic retrieval flow

Query → `EmbeddingProvider.embed_query` → vector search → score ranking → `RetrievalResponse` with `EvidenceItem` list (chunk text, `source_reference`, section metadata, provenance, timing).

### Embedding abstraction

`EmbeddingProvider` isolates model choice. Default: `LocalHashEmbeddingProvider` (deterministic, for wiring and tests). Replace with hosted or self-hosted models without changing retrieval or indexing contracts.

### Provenance-aware retrieval

Indexed payloads and retrieval results preserve `chunk_id`, `document_id`, `source_reference`, `source_uri`, section anchors, and lineage—ready for citations and evaluation, not answer synthesis.

### Design tradeoffs

| Decision | Rationale |
|----------|-----------|
| Separate ingest / index / retrieve CLIs | Explicit stages, easy to test and replay |
| Collection per ingest run | Isolates corpus versions for eval |
| Local hash embedder | No external API dependency in phase 2 |
| In-memory store in tests | Fast deterministic CI without Qdrant |

## Ingestion (phase 1)

```bash
make ingest RUN_ID=local-dev-001
```

Corpus under `data/raw/` (`course_catalog/`, `syllabi/`, `faculty_publications/`, `policies/`). Structure-aware chunking with provenance metadata.

## Core capabilities

| Capability | Status |
|------------|--------|
| Provenance-aware ingestion | Done |
| Structure-aware chunking | Done |
| Embedding provider abstraction | Done |
| Vector indexing (Qdrant) | Done |
| Semantic retrieval + contracts | Done |
| Retrieval instrumentation hooks | Done |
| Citation-grounded answers (LLM) | Planned |
| Agent orchestration | Planned |
| Evaluation harness | Planned |

## Local development

Prerequisites: Python 3.11+, Node 20+, Docker, Make.

```bash
cp .env.example .env
make infra-up
make ingest-install
make ingest RUN_ID=local-dev-001
make index RUN_ID=local-dev-001
make retrieve RUN_ID=local-dev-001 QUERY="course requirements"
make api-dev                       # http://localhost:8000/health
make ingest-test
```

## Engineering principles

- Explicit boundaries; typed contracts at every stage
- Deterministic ingestion; retrieval instrumentation for measurement
- No framework-heavy abstractions
- Evaluation before orchestration expansion

Standards: [docs/engineering-standards.md](docs/engineering-standards.md).

## Repository layout

```
scholarflow/
  apps/api/                 FastAPI gateway
  apps/web/                 Angular client
  services/retrieval/       Ingestion, embedding, indexing, retrieval
  packages/schemas/         Ingestion + retrieval contracts
  data/raw/                 Corpus sources
  data/processed/           Ingest outputs (gitignored)
  infra/docker/             Postgres, Qdrant
  docs/architecture/
```
