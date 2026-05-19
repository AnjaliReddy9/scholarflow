import hashlib
import math
import struct

from scholarflow_schemas.retrieval import EmbeddingRequest, EmbeddingResponse

from scholarflow_retrieval.embedding.protocol import EmbeddingProvider

_DEFAULT_DIMENSIONS = 384


def _deterministic_vector(text: str, dimensions: int) -> list[float]:
    digest = hashlib.sha256(text.encode("utf-8")).digest()
    values: list[float] = []
    while len(values) < dimensions:
        for offset in range(0, len(digest) - 3, 4):
            raw = struct.unpack(">i", digest[offset : offset + 4])[0]
            values.append((raw % 2001) / 1000.0 - 1.0)
            if len(values) >= dimensions:
                break
        digest = hashlib.sha256(digest).digest()
    norm = math.sqrt(sum(v * v for v in values)) or 1.0
    return [v / norm for v in values]


class LocalHashEmbeddingProvider:
    """Deterministic local embedder for development and tests. Not semantic."""

    def __init__(
        self,
        model_id: str = "local-hash-v1",
        dimensions: int = _DEFAULT_DIMENSIONS,
    ) -> None:
        self._model_id = model_id
        self._dimensions = dimensions

    @property
    def model_id(self) -> str:
        return self._model_id

    @property
    def dimensions(self) -> int:
        return self._dimensions

    def embed(self, request: EmbeddingRequest) -> EmbeddingResponse:
        vectors = [_deterministic_vector(text, self._dimensions) for text in request.texts]
        return EmbeddingResponse(
            model_id=self._model_id,
            dimensions=self._dimensions,
            vectors=vectors,
        )

    def embed_query(self, text: str) -> list[float]:
        return _deterministic_vector(text, self._dimensions)
