from pathlib import Path

from scholarflow_schemas.retrieval import EmbeddingRequest, IndexedChunkPayload

from scholarflow_retrieval.embedding.protocol import EmbeddingProvider
from scholarflow_retrieval.indexing.chunks import indexed_payload_from_chunk, load_chunks_jsonl
from scholarflow_retrieval.indexing.store import VectorStore


def index_chunks_file(
    chunks_path: Path,
    embedder: EmbeddingProvider,
    store: VectorStore,
) -> int:
    chunks = load_chunks_jsonl(chunks_path)
    if not chunks:
        store.ensure_collection(embedder.dimensions)
        return 0

    texts = [chunk.text for chunk in chunks]
    response = embedder.embed(EmbeddingRequest(texts=texts))
    store.ensure_collection(response.dimensions)

    points: list[tuple[str, list[float], IndexedChunkPayload]] = []
    for chunk, vector in zip(chunks, response.vectors, strict=True):
        points.append((chunk.chunk_id, vector, indexed_payload_from_chunk(chunk)))
    return store.upsert(points)
