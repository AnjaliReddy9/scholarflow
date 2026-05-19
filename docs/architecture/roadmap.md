# Delivery roadmap

## Phase 0 — Foundation (current)

- Monorepo layout, documentation, engineering standards
- FastAPI skeleton with health endpoint and DI placeholders
- Angular shell with query page placeholder
- Docker Compose: Postgres, vector store placeholder
- Pre-commit, Makefile, CI skeleton (future)

**Exit criteria:** Local stack starts; API returns typed health; web serves layout and query route.

## Phase 1 — Ingestion (in progress)

- [x] Document loaders and normalization
- [x] Structure-aware chunking with version metadata
- [x] Provenance mapping and processed artifact layout
- [x] Ingestion CLI (`scholarflow-ingest`)
- [x] Synthetic academic corpus under `data/raw/`
- [ ] Embedding pipeline (deferred to phase 2)

**Exit criteria:** Repeatable ingest from sample corpus to processed chunks on disk. **Met** for normalization and chunking; embeddings remain out of scope.

## Phase 2 — Retrieval

- Embedding pipeline
- Vector index create/update
- Search API with filters and stable chunk IDs
- Integration tests against local Qdrant

**Exit criteria:** Query returns ranked chunks with provenance; no synthesis yet.

## Phase 3 — Orchestration and inference

- OpenAI-compatible inference adapter
- Orchestrator workflow: retrieve → generate → cite
- `POST /v1/query` end-to-end
- Structured errors for timeout and empty context

**Exit criteria:** Web client receives answer + citations against dev corpus.

## Phase 4 — Evaluation

- Golden set format and runner
- Scorers: citation coverage, retrieval recall@k (where labeled)
- CI gate on smoke golden set
- Run artifact storage

**Exit criteria:** PR fails on intentional regression in smoke set.

## Phase 5 — Observability and operations

- Trace propagation
- Dashboards for latency and failure modes
- Runbooks for index rebuild and eval failures

## Phase 6 — Self-hosted inference

- Local model deployment path
- Config switch without API contract change
- Eval reproducibility notes per model revision
