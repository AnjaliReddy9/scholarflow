from scholarflow_retrieval.chunking.structure import chunks_for_document
from scholarflow_retrieval.ids import chunk_id_for
from scholarflow_retrieval.loaders.markdown import load_markdown_file
from scholarflow_retrieval.normalize.document import normalize_document


def test_chunks_respect_section_boundaries(raw_dir, fixture_run_id, fixture_time) -> None:
    source = load_markdown_file(raw_dir / "syllabi" / "cs301-algorithms-spring2026.md")
    document = normalize_document(source, fixture_run_id, ingested_at=fixture_time)
    chunks = chunks_for_document(document)

    anchors = {chunk.source_anchor for chunk in chunks}
    assert "instructor-and-meetings" in anchors
    assert "grading" in anchors
    for chunk in chunks:
        assert chunk.document_id == document.document_id
        assert chunk.provenance.ingest_run_id == fixture_run_id


def test_chunk_ordering_is_stable(raw_dir, fixture_run_id, fixture_time) -> None:
    source = load_markdown_file(raw_dir / "policies" / "student-records-access.md")
    document = normalize_document(source, fixture_run_id, ingested_at=fixture_time)
    first = chunks_for_document(document)
    second = chunks_for_document(document)
    assert [c.chunk_id for c in first] == [c.chunk_id for c in second]
    assert [c.chunk_index for c in first] == [c.chunk_index for c in second]


def test_chunk_id_format() -> None:
    assert chunk_id_for("doc_abcd", "scope", 0) == "doc_abcd::scope::0"
