from datetime import UTC, datetime
from pathlib import Path

import pytest

FIXTURE_TIME = datetime(2026, 3, 1, 12, 0, 0, tzinfo=UTC)
FIXTURE_RUN_ID = "test-ingest-001"


@pytest.fixture
def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


@pytest.fixture
def raw_dir(repo_root: Path) -> Path:
    return repo_root / "data" / "raw"


@pytest.fixture
def fixture_time() -> datetime:
    return FIXTURE_TIME


@pytest.fixture
def fixture_run_id() -> str:
    return FIXTURE_RUN_ID
