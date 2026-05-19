from fastapi import APIRouter

from scholarflow_api import __version__
from scholarflow_schemas.health import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(version=__version__)
