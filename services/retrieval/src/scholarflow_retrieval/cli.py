import argparse
import json
from pathlib import Path

from scholarflow_schemas.ingestion import SourceType
from scholarflow_schemas.retrieval import RetrievalQuery

from scholarflow_retrieval.config import load_settings, resolve_chunks_path
from scholarflow_retrieval.factory import build_embedder, build_retrieval_service, build_vector_store
from scholarflow_retrieval.indexing.pipeline import index_chunks_file
from scholarflow_retrieval.pipeline.ingest import run_ingestion


def _cmd_ingest(args: argparse.Namespace) -> None:
    manifest = run_ingestion(
        raw_dir=args.raw_dir,
        processed_dir=args.processed_dir,
        ingest_run_id=args.ingest_run_id,
    )
    print(
        f"ingest_run_id={manifest.ingest_run_id} "
        f"documents={manifest.document_count} chunks={manifest.chunk_count}"
    )


def _cmd_index(args: argparse.Namespace) -> None:
    settings = load_settings()
    chunks_path = resolve_chunks_path(args.processed_dir, args.ingest_run_id)
    if not chunks_path.exists():
        raise SystemExit(f"chunks file not found: {chunks_path}")

    embedder = build_embedder(settings)
    store = build_vector_store(settings, args.ingest_run_id, in_memory=args.in_memory)
    indexed = index_chunks_file(chunks_path, embedder, store)
    print(
        f"collection={store.collection} indexed={indexed} "
        f"total={store.count()} backend={'memory' if args.in_memory else 'qdrant'}"
    )


def _cmd_retrieve(args: argparse.Namespace) -> None:
    settings = load_settings()
    service = build_retrieval_service(
        settings,
        args.ingest_run_id,
        in_memory=args.in_memory,
    )
    source_type = SourceType(args.source_type) if args.source_type else None
    response = service.retrieve(
        RetrievalQuery(
            query=args.query,
            top_k=args.top_k,
            ingest_run_id=args.ingest_run_id if args.filter_run else None,
            source_type=source_type,
        )
    )
    if args.json:
        print(json.dumps(response.model_dump(mode="json"), indent=2))
        return
    print(
        f"results={len(response.results)} "
        f"embedding_ms={response.timing.embedding_ms:.2f} "
        f"search_ms={response.timing.search_ms:.2f}"
    )
    for item in response.results:
        print(f"  score={item.score:.4f} ref={item.source_reference} section={item.section_title}")


def main() -> None:
    parser = argparse.ArgumentParser(description="ScholarFlow corpus and retrieval commands")
    subparsers = parser.add_subparsers(dest="command", required=True)

    ingest_parser = subparsers.add_parser("ingest", help="Run ingestion pipeline")
    ingest_parser.add_argument("--raw-dir", type=Path, default=Path("data/raw"))
    ingest_parser.add_argument("--processed-dir", type=Path, default=Path("data/processed"))
    ingest_parser.add_argument("--ingest-run-id", type=str, default=None)
    ingest_parser.set_defaults(func=_cmd_ingest)

    index_parser = subparsers.add_parser("index", help="Index processed chunks")
    index_parser.add_argument("--processed-dir", type=Path, default=Path("data/processed"))
    index_parser.add_argument("--ingest-run-id", type=str, required=True)
    index_parser.add_argument("--in-memory", action="store_true")
    index_parser.set_defaults(func=_cmd_index)

    retrieve_parser = subparsers.add_parser("retrieve", help="Semantic retrieval over index")
    retrieve_parser.add_argument("--ingest-run-id", type=str, required=True)
    retrieve_parser.add_argument("--query", type=str, required=True)
    retrieve_parser.add_argument("--top-k", type=int, default=5)
    retrieve_parser.add_argument("--filter-run", action="store_true")
    retrieve_parser.add_argument("--source-type", type=str, default=None)
    retrieve_parser.add_argument("--in-memory", action="store_true")
    retrieve_parser.add_argument("--json", action="store_true")
    retrieve_parser.set_defaults(func=_cmd_retrieve)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
