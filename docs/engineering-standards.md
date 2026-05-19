# Engineering standards

## Commits

- Conventional commits: `type(scope): description`
- Types: `feat`, `fix`, `docs`, `chore`, `build`, `test`, `refactor`, `ci`
- One logical change per commit; avoid mixed refactors and features
- Imperative subject line, ≤72 characters; body explains why when non-obvious

## Branching

- `main` is always deployable for the current phase scope
- Feature branches: `feat/<short-name>`, `fix/<short-name>`, `docs/<short-name>`
- No long-lived integration branches without documented reason

## API standards

- All endpoints use Pydantic request/response models from `packages/schemas` where shared
- Version paths under `/v1/` when public contract stabilizes
- Errors return consistent shape: `code`, `message`, optional `detail`
- OpenAPI generated from FastAPI models; no hand-maintained duplicate specs
- Idempotent read endpoints; writes document side effects in handler docstrings only when non-obvious

## Testing expectations

- Unit tests for pure logic and schema validation
- API integration tests for health and future query paths using `httpx` + `TestClient`
- Service tests mock external I/O (vector DB, inference)
- Golden-set evaluation tests run in CI only when artifact size and runtime are controlled
- No tests that assert on LLM wording; assert structure, citations present, retrieval IDs

## Typing

- Python 3.11+ with strict mypy on `apps/api` and `packages/*`
- Explicit return types on public functions
- `Annotated` + `Depends` for FastAPI injection
- TypeScript strict mode in `apps/web`

## Architecture principles

- Boundaries: apps orchestrate HTTP; services own domain logic; packages hold contracts only
- Prefer composition over inheritance
- No god modules; target &lt;300 lines per file unless data-driven
- Dependencies point inward: services may depend on packages, not on apps
- Feature flags via configuration, not compile-time branches

## Observability expectations

- Structured JSON logs in production paths (phase 5)
- Trace ID propagated from API through service calls
- Health (`/health`) vs readiness (`/ready`) separation when dependencies exist
- Metrics: request latency, retrieval hit rate, inference tokens (when implemented)—no placeholder counters in phase 0
