from pathlib import Path

from campusiq_schemas.ingestion import SourceType

from campusiq_retrieval.loaders.raw_source import RawSource

_DIRECTORY_SOURCE_TYPE: dict[str, SourceType] = {
    "course_catalog": SourceType.COURSE_CATALOG,
    "syllabi": SourceType.SYLLABUS,
    "faculty_publications": SourceType.FACULTY_PUBLICATION,
    "policies": SourceType.UNIVERSITY_POLICY,
}


def _parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text
    _, _, remainder = text.partition("---\n")
    header, _, body = remainder.partition("\n---\n")
    if not body:
        return {}, text
    metadata: dict[str, str] = {}
    for line in header.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip()
    return metadata, body.lstrip("\n")


def _infer_source_type(path: Path) -> SourceType:
    for part in path.parts:
        if part in _DIRECTORY_SOURCE_TYPE:
            return _DIRECTORY_SOURCE_TYPE[part]
    raise ValueError(f"cannot infer source_type for path: {path}")


def load_markdown_file(path: Path) -> RawSource:
    raw_bytes = path.read_bytes()
    text = raw_bytes.decode("utf-8")
    metadata, body = _parse_frontmatter(text)
    source_type = SourceType(metadata["source_type"]) if "source_type" in metadata else _infer_source_type(path)
    title = metadata.get("title") or path.stem.replace("-", " ").title()
    source_reference = metadata.get("source_reference") or f"{source_type.value}/{path.name}"
    return RawSource(
        path=path,
        source_type=source_type,
        title=title,
        body=body,
        source_reference=source_reference,
    )


def discover_markdown_sources(raw_dir: Path) -> list[RawSource]:
    paths = sorted(raw_dir.rglob("*.md"))
    return [load_markdown_file(path) for path in paths]
