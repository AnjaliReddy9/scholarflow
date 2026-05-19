from dataclasses import dataclass
from pathlib import Path

from scholarflow_schemas.ingestion import SourceType


@dataclass(frozen=True)
class RawSource:
    path: Path
    source_type: SourceType
    title: str
    body: str
    source_reference: str
