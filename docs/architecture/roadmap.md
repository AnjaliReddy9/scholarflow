# Delivery roadmap

## Phase 0 — Foundation

- Monorepo, API shell, web shell, Docker baseline, engineering standards

**Exit criteria:** Met.

## Phase 1 — Ingestion

- [x] Loaders, normalization, structure-aware chunking, provenance
- [x] Synthetic corpus, ingestion CLI, processed JSONL artifacts

**Exit criteria:** Met.

## Phase 2 — Retrieval (complete)

- [x] `EmbeddingProvider` abstraction and local deterministic provider
- [x] Vector indexing pipeline (Qdrant + in-memory for tests)
- [x] Semantic retrieval flow and `RetrievalResponse` contracts
- [x] `RetrievalService` and instrumentation hooks
- [x] CLI: `index`, `retrieve`; tests for ordering, metadata, determinism

**Exit criteria:** Met — query returns ranked evidence with provenance; no synthesis.

## Phase 3 — Orchestration and inference

- OpenAI-compatible inference adapter
- Orchestrator: retrieve → generate → cite
- `POST /v1/query` on API
- Web client wired to query endpoint

## Phase 4 — Evaluation

- Golden set runner, retrieval recall@k where labeled
- CI gate on smoke set

## Phase 5 — Observability

- Trace propagation, operational runbooks

## Phase 6 — Self-hosted inference

- Local model path without contract changes
