from campusiq_retrieval.normalize.sections import split_paragraphs


def split_section_body(body: str, max_chars: int) -> list[str]:
    text = body.strip()
    if not text:
        return []
    if len(text) <= max_chars:
        return [text]

    paragraphs = split_paragraphs(text)
    if not paragraphs:
        return [text]

    parts: list[str] = []
    current: list[str] = []
    current_len = 0
    for paragraph in paragraphs:
        addition = len(paragraph) + (2 if current else 0)
        if current and current_len + addition > max_chars:
            parts.append("\n\n".join(current))
            current = [paragraph]
            current_len = len(paragraph)
            continue
        current.append(paragraph)
        current_len += addition
    if current:
        parts.append("\n\n".join(current))
    return parts
