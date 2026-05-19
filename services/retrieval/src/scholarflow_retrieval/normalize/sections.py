import re

from scholarflow_retrieval.ids import slugify

_HEADING = re.compile(r"^(#{1,6})\s+(.+)$")


def split_paragraphs(text: str) -> list[str]:
    blocks: list[str] = []
    current: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            if current:
                blocks.append("\n".join(current).strip())
                current = []
            continue
        current.append(stripped)
    if current:
        blocks.append("\n".join(current).strip())
    return [block for block in blocks if block]


def extract_markdown_sections(body: str) -> list[tuple[list[str], str, int, str]]:
    """Return (hierarchy titles, body, heading level, anchor) per section."""
    lines = body.splitlines()
    results: list[tuple[list[str], str, int, str]] = []
    hierarchy: list[tuple[int, str]] = []
    current_lines: list[str] = []
    current_level = 1

    def hierarchy_titles() -> list[str]:
        return [title for _, title in hierarchy]

    def flush() -> None:
        text = "\n".join(current_lines).strip()
        if not text:
            return
        titles = hierarchy_titles() or ["Document"]
        results.append((titles, text, current_level, slugify(titles[-1])))

    for line in lines:
        match = _HEADING.match(line.strip())
        if match:
            flush()
            current_lines = []
            level = len(match.group(1))
            title = match.group(2).strip()
            while hierarchy and hierarchy[-1][0] >= level:
                hierarchy.pop()
            hierarchy.append((level, title))
            current_level = level
            continue
        current_lines.append(line)

    flush()
    if not results:
        return [(["Document"], body.strip(), 1, "document")]
    return results
