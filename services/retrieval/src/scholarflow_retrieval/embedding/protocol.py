from typing import Protocol

from scholarflow_schemas.retrieval import EmbeddingRequest, EmbeddingResponse


class EmbeddingProvider(Protocol):
    @property
    def model_id(self) -> str: ...

    @property
    def dimensions(self) -> int: ...

    def embed(self, request: EmbeddingRequest) -> EmbeddingResponse: ...

    def embed_query(self, text: str) -> list[float]: ...
