# Architecture overview

## Logical architecture

```
┌─────────────┐     ┌─────────────┐     ┌──────────────────┐
│  apps/web   │────▶│  apps/api   │────▶│ services/        │
│  (Angular)  │     │  (FastAPI)  │     │ orchestrator     │
└─────────────┘     └─────────────┘     └────────┬─────────┘
                                                  │
                    ┌─────────────────────────────┼─────────────────────────────┐
                    ▼                             ▼                             ▼
           ┌────────────────┐          ┌────────────────┐          ┌────────────────┐
           │ retrieval      │          │ inference      │          │ evaluation     │
           │ (index/search) │          │ (LLM I/O)      │          │ (offline runs) │
           └────────┬───────┘          └────────────────┘          └────────────────┘
                    │
                    ▼
           ┌────────────────┐
           │ Postgres       │
           │ vector store   │
           └────────────────┘
```

`apps/api` is the only HTTP entry point for the web client in phase 0. Internal services will expose typed interfaces (HTTP or in-process adapters) behind stable contracts in `packages/schemas`.

## Request lifecycle

1. Client submits a query with session metadata to `POST /v1/query` (future).
2. API validates input, assigns a trace ID, emits structured logs.
3. Orchestrator plans steps: retrieval scope, synthesis, optional verification.
4. Retrieval returns ranked chunks with stable source IDs.
5. Inference generates an answer constrained to retrieved context.
6. Orchestrator attaches citations (chunk ID → excerpt → source URI).
7. API returns a typed response; errors map to structured error bodies.

Phase 0 implements health checks and routing layout only. No orchestration or retrieval execution yet.

## Orchestration model

The orchestrator owns workflow state: which tools run, in what order, and when to stop. It does not embed retrieval or inference logic; it calls service interfaces and aggregates results.

Design constraints:

- Deterministic step logging for replay and evaluation
- Timeouts and cancellation per step
- No hidden prompt chains in the API layer
- Tool boundaries align with service ownership

Implementation lands in `services/orchestrator` during phase 3.

## Retrieval model

Retrieval is a separate service responsible for:

- Document ingestion metadata (not raw file storage in the API)
- Chunking policy versioning
- Embedding and index updates
- Search with filters (source, date, document type)

Answers must cite retrieval results by chunk ID. The API never fabricates sources; missing retrieval yields an explicit empty-context response.

Implementation lands in `services/retrieval` during phases 1–2.

## Evaluation philosophy

Quality is measured, not assumed.

- Golden sets live under `data/golden_set/` (content gitignored; structure versioned).
- Evaluation runs produce versioned artifacts (scores, failures, latency).
- CI runs a smoke subset; full runs are scheduled or manual pre-release.
- Regressions block merge when configured thresholds fail.

No synthetic “accuracy” metrics in application code. Report what was measured.

## Self-hosted inference

Inference is behind an OpenAI-compatible interface in `services/inference`. Swapping providers (hosted API vs local vLLM/Ollama) should not change orchestrator or API contracts—only configuration and capability flags (context length, streaming).

Reasons to plan for self-hosting:

- Data residency for campus documents
- Cost predictability at scale
- Reproducible eval runs against fixed model weights
- Reduced vendor coupling for core query path

Phase 0 defines the package boundary only; no provider implementation.
