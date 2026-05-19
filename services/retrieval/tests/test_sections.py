from scholarflow_retrieval.normalize.sections import extract_markdown_sections, split_paragraphs


def test_extract_markdown_sections_preserves_hierarchy() -> None:
    body = "# Root\n\nIntro.\n\n## Child\n\nDetail paragraph."
    sections = extract_markdown_sections(body)
    assert len(sections) == 2
    assert sections[0][0] == ["Root"]
    assert sections[1][0] == ["Root", "Child"]
    assert "Detail paragraph" in sections[1][1]


def test_split_paragraphs_is_deterministic() -> None:
    text = "First paragraph.\n\nSecond paragraph.\n\nThird paragraph."
    assert split_paragraphs(text) == split_paragraphs(text)
