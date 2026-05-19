from scholarflow_schemas.retrieval import EmbeddingRequest

from scholarflow_retrieval.embedding.local import LocalHashEmbeddingProvider


def test_local_embedding_is_deterministic() -> None:
    provider = LocalHashEmbeddingProvider(dimensions=32)
    first = provider.embed(EmbeddingRequest(texts=["academic policy retention"]))
    second = provider.embed(EmbeddingRequest(texts=["academic policy retention"]))
    assert first.vectors == second.vectors
    assert len(first.vectors[0]) == 32


def test_embed_query_matches_batch() -> None:
    provider = LocalHashEmbeddingProvider(dimensions=16)
    text = "course catalog requirements"
    batch = provider.embed(EmbeddingRequest(texts=[text])).vectors[0]
    single = provider.embed_query(text)
    assert batch == single
