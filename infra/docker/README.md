# Local infrastructure

Postgres holds application metadata and ingestion state. Qdrant is the vector store placeholder for retrieval (phase 2).

```bash
docker compose -f infra/docker/docker-compose.yml up -d
```

From repository root, `make infra-up` wraps the same command.
