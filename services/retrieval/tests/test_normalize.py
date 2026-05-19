from campusiq_retrieval.loaders.markdown import load_markdown_file
from campusiq_retrieval.normalize.document import normalize_document


def test_normalize_document_preserves_metadata(raw_dir, fixture_run_id, fixture_time) -> None:
    path = raw_dir / "course_catalog" / "undergraduate-computer-science.md"
    source = load_markdown_file(path)
    document = normalize_document(source, fixture_run_id, ingested_at=fixture_time)

    assert document.title == "Undergraduate Computer Science Programs"
    assert document.source_reference == "catalog/undergraduate-computer-science"
    assert document.provenance.loader == "markdown"
    assert document.provenance.content_checksum
    assert len(document.sections) >= 3
    assert document.ingested_at == fixture_time
