# ScholarFlow

Self-hosted academic intelligence and agentic RAG platform for universities. The codebase is a monorepo with explicit service boundaries, typed contracts, and deterministic ingestion for citation traceability.

## Purpose

ScholarFlow demonstrates production-style Applied AI engineering: agentic orchestration over retrieval pipelines, measurable answer quality, structured observability, and a path to self-hosted inference. Internal platform code—not a chatbot wrapper.

## Architecture summary

| Layer | Responsibility |
|-------|----------------|
| `apps/web` | Angular client; query submission and citation display |
| `apps/api` | FastAPI gateway; request validation, routing, error mapping |
| `services/orchestrator` | Agent workflow, tool calls, answer assembly |
| `services/retrieval` | Ingestion, indexing, search |
| `services/evaluation` | Golden-set runs, regression gates |
| `services/inference` | OpenAI-compatible provider abstraction; self-host later |
| `packages/schemas` | Shared Pydantic models |
| `packages/common` | Cross-cutting utilities |

Flow: client → API → orchestrator → retrieval + inference → structured response with citations.

See [docs/architecture/overview.md](docs/architecture/overview.md) and [docs/architecture/ingestion.md](docs/architecture/ingestion.md).

## Current phase

| Phase | Status |
|-------|--------|
| 0 — Foundation | Complete (API shell, web shell, Docker baseline) |
| 1 — Ingestion | **In progress** — normalization, chunking, provenance, synthetic corpus |
| 2 — Retrieval | Planned (embeddings, vector index) |
| 3+ | Orchestration, evaluation, observability, self-hosted inference |

## Ingestion (phase 1)

Corpus sources live under `data/raw/` by type: `course_catalog/`, `syllabi/`, `faculty_publications/`, `policies/`.

Pipeline stages: load → normalize → section extract → structure-aware chunk → provenance attach → persist JSONL.

```bash
make ingest-install
make ingest RUN_ID=local-dev-001
```

Outputs: `data/processed/{ingest_run_id}/documents.jsonl`, `chunks.jsonl`, `manifest.json`.

**Corpus philosophy:** small, realistic university documents—structured markdown with YAML frontmatter, no bulk synthetic dumps. **Citation strategy:** every chunk carries `chunk_id`, `source_anchor`, `source_reference`, and `provenance.lineage` for deterministic replay in evaluation.

**Determinism:** fixed source bytes and ingest run metadata produce identical chunk boundaries and IDs. Timestamps are run-scoped, not hidden randomness in chunk text.

## Core capabilities

| Capability | Status |
|------------|--------|
| Provenance-aware ingestion | Implemented |
| Structure-aware chunking | Implemented |
| Citation-grounded answers | Planned |
| Vector retrieval | Planned |
| Agent orchestration | Planned |
| Evaluation harness | Planned |

## Local development

Prerequisites: Python 3.11+, Node 20+, Docker, Make.

```bash
cp .env.example .env
make infra-up
make api-install && make api-dev      # http://localhost:8000/health
make ingest-install && make ingest    # corpus → data/processed/
make web-install && make web-dev      # http://localhost:4200
```

## Engineering principles

- Explicit boundaries between apps, services, and packages
- Pydantic models for all contracts
- Deterministic ingestion before semantic retrieval
- Evaluation before feature expansion
- No framework-heavy pipeline abstractions

Standards: [docs/engineering-standards.md](docs/engineering-standards.md).

## Repository layout

```
campusiq/                          # repository root (ScholarFlow codebase)
  apps/api/                        FastAPI gateway
  apps/web/                        Angular client
  services/retrieval/              Ingestion (and future search)
  packages/schemas/                Shared models
  data/raw/                        Versioned corpus sources
  data/processed/                  Ingestion outputs (gitignored)
  infra/docker/                    Postgres, Qdrant placeholder
  docs/architecture/               System and ingestion design
```
