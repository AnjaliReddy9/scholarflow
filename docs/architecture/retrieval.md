# Retrieval architecture

Semantic retrieval for ScholarFlow is isolated from orchestration and inference. The flow is explicit, typed, and instrumented for future evaluation.

## Layers

| Layer | Responsibility |
|-------|----------------|
| `embedding/` | Provider interface; local deterministic stub today |
| `indexing/` | Vector store abstraction; Qdrant (dev) and in-memory (tests) |
| `retrieval/` | Query embedding, search, ranking, response assembly |
| `observability/` | Retrieval event hooks (logging stub) |

Contracts live in `packages/schemas` (`scholarflow_schemas.retrieval`).

## Indexing flow

1. Read `chunks.jsonl` from `data/processed/{ingest_run_id}/`
2. Batch-embed chunk text via `EmbeddingProvider`
3. Upsert vectors + `IndexedChunkPayload` into collection `scholarflow_{ingest_run_id}`
4. Payload preserves `chunk_id`, provenance, section metadata, and raw text

## Retrieval flow

1. Accept `RetrievalQuery` (`query`, `top_k`, optional filters)
2. Embed query
3. Vector similarity search (cosine)
4. Rank by score, tie-break on `chunk_id`
5. Map hits to `EvidenceItem` with full provenance
6. Return `RetrievalResponse` with timing and instrumentation metadata

No answer synthesis, reranking, or LLM calls in this phase.

## Embedding abstraction

`EmbeddingProvider` exposes `embed()` and `embed_query()`. The default `LocalHashEmbeddingProvider` is deterministic and replaceable—intended for pipeline wiring and tests, not production semantic quality.

Hosted or self-hosted models plug in behind the same interface in a later session.

## Vector store abstraction

`VectorStore` supports `ensure_collection`, `upsert`, `search`, and `count`. Filters: `ingest_run_id`, `source_type` (for future hybrid constraints).

## Instrumentation

`RetrievalInstrumentation.on_retrieval` receives latency breakdown, candidate count, top-k, and model id. Default implementation logs structured fields; no metrics backend yet.

## Out of scope

- Reranking
- Hybrid BM25
- Orchestrator integration
- API HTTP surface (phase 4)
- Distributed tracing
