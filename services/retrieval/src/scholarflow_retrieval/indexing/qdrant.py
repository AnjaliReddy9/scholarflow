from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels

from scholarflow_schemas.retrieval import IndexedChunkPayload

from scholarflow_retrieval.indexing.store import ScoredPoint


class QdrantVectorStore:
    def __init__(self, url: str, collection: str) -> None:
        self._client = QdrantClient(url=url)
        self._collection = collection

    @property
    def collection(self) -> str:
        return self._collection

    def ensure_collection(self, dimensions: int) -> None:
        if self._client.collection_exists(self._collection):
            info = self._client.get_collection(self._collection)
            existing = info.config.params.vectors.size  # type: ignore[union-attr]
            if existing != dimensions:
                raise ValueError(
                    f"collection {self._collection} expects {existing} dims, got {dimensions}"
                )
            return
        self._client.create_collection(
            collection_name=self._collection,
            vectors_config=qmodels.VectorParams(size=dimensions, distance=qmodels.Distance.COSINE),
        )

    def upsert(self, points: list[tuple[str, list[float], IndexedChunkPayload]]) -> int:
        if not points:
            return 0
        qdrant_points = [
            qmodels.PointStruct(
                id=chunk_id,
                vector=vector,
                payload=payload.model_dump(mode="json"),
            )
            for chunk_id, vector, payload in points
        ]
        self._client.upsert(collection_name=self._collection, points=qdrant_points)
        return len(qdrant_points)

    def search(
        self,
        query_vector: list[float],
        top_k: int,
        ingest_run_id: str | None = None,
        source_type: str | None = None,
    ) -> list[ScoredPoint]:
        filters: list[qmodels.FieldCondition] = []
        if ingest_run_id is not None:
            filters.append(
                qmodels.FieldCondition(
                    key="ingest_run_id",
                    match=qmodels.MatchValue(value=ingest_run_id),
                )
            )
        if source_type is not None:
            filters.append(
                qmodels.FieldCondition(
                    key="source_type",
                    match=qmodels.MatchValue(value=source_type),
                )
            )
        query_filter = qmodels.Filter(must=filters) if filters else None
        hits = self._client.search(
            collection_name=self._collection,
            query_vector=query_vector,
            limit=top_k,
            query_filter=query_filter,
        )
        results: list[ScoredPoint] = []
        for hit in hits:
            payload = IndexedChunkPayload.model_validate(hit.payload or {})
            results.append(
                ScoredPoint(
                    chunk_id=str(hit.id),
                    score=float(hit.score or 0.0),
                    payload=payload,
                    vector=[],
                )
            )
        return results

    def count(self) -> int:
        info = self._client.get_collection(self._collection)
        return int(info.points_count or 0)
