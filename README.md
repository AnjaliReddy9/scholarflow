# CampusIQ

Applied AI platform for campus-domain question answering with retrieval, orchestration, evaluation, and citation-aware responses. The codebase is organized as a monorepo with explicit service boundaries and typed contracts at every API surface.

## Purpose

CampusIQ demonstrates production-style Applied AI engineering: agentic orchestration over retrieval pipelines, measurable answer quality, structured observability, and a path to self-hosted inference. It is an internal platform project, not a demo chatbot.

## Architecture summary

| Layer | Responsibility |
|-------|----------------|
| `apps/web` | Angular client; query submission and citation display |
| `apps/api` | FastAPI gateway; request validation, routing, error mapping |
| `services/orchestrator` | Agent workflow, tool calls, answer assembly |
| `services/retrieval` | Indexing, embedding, search |
| `services/evaluation` | Golden-set runs, regression gates |
| `services/inference` | OpenAI-compatible provider abstraction; self-host later |
| `packages/schemas` | Shared Pydantic models |
| `packages/common` | Cross-cutting utilities (logging helpers, IDs) |

Logical flow: client → API → orchestrator → retrieval + inference → structured response with citations. Evaluation runs offline against golden sets and gates merges.

See [docs/architecture/overview.md](docs/architecture/overview.md).

## Core capabilities (planned)

- Citation-grounded answers over campus knowledge
- Retrieval-augmented generation with explicit chunk provenance
- Orchestrated multi-step queries (retrieve, synthesize, verify)
- Evaluation harness with golden-set regression
- OpenAI-compatible inference interface
- Local Docker stack for Postgres and vector store
- CI quality gates (lint, typecheck, tests, eval smoke)

## Phased roadmap

| Phase | Focus |
|-------|--------|
| 0 | Monorepo, API skeleton, web shell, Docker baseline (current) |
| 1 | Ingestion, chunking, embedding pipeline |
| 2 | Retrieval service and index management |
| 3 | Orchestrator and inference integration |
| 4 | Evaluation harness and CI gates |
| 5 | Observability, tracing, operational runbooks |
| 6 | Self-hosted inference option |

Details: [docs/architecture/roadmap.md](docs/architecture/roadmap.md).

## Local development

Prerequisites: Python 3.11+, Node 20+, Docker, Make.

```bash
cp .env.example .env
make infra-up          # Postgres + vector placeholder
make api-install
make api-dev           # http://localhost:8000/health
make web-install
make web-dev           # http://localhost:4200
```

API docs (when running): `http://localhost:8000/docs`

## Engineering principles

- Explicit boundaries between apps, services, and packages
- Pydantic models for all request/response contracts
- No framework-heavy abstractions; small focused modules
- Evaluation before feature expansion
- Observability as a first-class concern, not an afterthought
- Self-hosting path for inference without rewriting clients

Standards: [docs/engineering-standards.md](docs/engineering-standards.md).

## Repository layout

```
campusiq/
  apps/api/          FastAPI gateway
  apps/web/          Angular client
  services/          Domain services (orchestrator, retrieval, evaluation, inference)
  packages/          Shared schemas and common code
  infra/docker/      Compose and local infra
  docs/              Architecture, ADRs, articles
  data/              Raw, processed, golden_set (gitignored contents)
```
