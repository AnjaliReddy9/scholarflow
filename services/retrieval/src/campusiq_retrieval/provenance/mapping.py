from campusiq_schemas.ingestion import ChunkProvenance, NormalizedDocument, SectionNode


def chunk_provenance_for(
    document: NormalizedDocument,
    section: SectionNode,
    chunk_index: int,
    lineage: list[str],
) -> ChunkProvenance:
    return ChunkProvenance(
        document_id=document.document_id,
        source_uri=document.provenance.source_uri,
        source_type=document.source_type,
        ingest_run_id=document.provenance.ingest_run_id,
        section_title=section.title,
        section_anchor=section.anchor,
        chunk_index=chunk_index,
        lineage=lineage,
    )
