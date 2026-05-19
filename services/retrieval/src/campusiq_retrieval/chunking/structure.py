from campusiq_schemas.ingestion import DocumentChunk, NormalizedDocument, SectionNode

from campusiq_retrieval.chunking.split import split_section_body
from campusiq_retrieval.constants import MAX_SECTION_CHARS
from campusiq_retrieval.ids import chunk_id_for
from campusiq_retrieval.provenance.mapping import chunk_provenance_for


def chunks_for_document(document: NormalizedDocument) -> list[DocumentChunk]:
    chunks: list[DocumentChunk] = []
    for section in document.sections:
        lineage = _lineage_for_section(document, section)
        parts = split_section_body(section.body, MAX_SECTION_CHARS)
        for index, text in enumerate(parts):
            provenance = chunk_provenance_for(
                document=document,
                section=section,
                chunk_index=index,
                lineage=lineage,
            )
            chunks.append(
                DocumentChunk(
                    chunk_id=chunk_id_for(document.document_id, section.anchor, index),
                    document_id=document.document_id,
                    section_title=section.title,
                    chunk_index=index,
                    source_reference=document.source_reference,
                    source_anchor=section.anchor,
                    provenance=provenance,
                    text=text,
                )
            )
    return chunks


def _lineage_for_section(document: NormalizedDocument, section: SectionNode) -> list[str]:
    lineage: list[str] = []
    for node in document.sections:
        lineage.append(node.anchor)
        if node.anchor == section.anchor:
            break
    return lineage or [section.anchor]
