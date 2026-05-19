import hashlib
import re


def slugify(value: str) -> str:
    lowered = value.lower().strip()
    slug = re.sub(r"[^a-z0-9]+", "-", lowered)
    return slug.strip("-") or "section"


def document_id_for(source_uri: str, source_type: str) -> str:
    digest = hashlib.sha256(f"{source_type}:{source_uri}".encode()).hexdigest()
    return f"doc_{digest[:16]}"


def chunk_id_for(document_id: str, section_anchor: str, chunk_index: int) -> str:
    return f"{document_id}::{section_anchor}::{chunk_index}"


def checksum_hex(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()
