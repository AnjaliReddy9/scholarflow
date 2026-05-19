from __future__ import annotations

from functools import lru_cache
from typing import Annotated, Protocol

from fastapi import Depends

from campusiq_api.config import Settings


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]


class OrchestratorClient(Protocol):
    """Placeholder for orchestrator service client (phase 3)."""

    async def ping(self) -> bool: ...


def get_orchestrator_client(
    _settings: Annotated[Settings, Depends(get_settings)],
) -> OrchestratorClient | None:
    return None


SettingsDep = Annotated[Settings, Depends(get_settings)]
OrchestratorDep = Annotated[OrchestratorClient | None, Depends(get_orchestrator_client)]
