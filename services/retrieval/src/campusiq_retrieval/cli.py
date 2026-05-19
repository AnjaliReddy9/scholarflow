import argparse
from pathlib import Path

from campusiq_retrieval.pipeline.ingest import run_ingestion


def main() -> None:
    parser = argparse.ArgumentParser(description="Run ScholarFlow corpus ingestion")
    parser.add_argument(
        "--raw-dir",
        type=Path,
        default=Path("data/raw"),
        help="Directory containing markdown source files",
    )
    parser.add_argument(
        "--processed-dir",
        type=Path,
        default=Path("data/processed"),
        help="Directory for ingestion output artifacts",
    )
    parser.add_argument(
        "--ingest-run-id",
        type=str,
        default=None,
        help="Optional stable ingest run identifier",
    )
    args = parser.parse_args()
    manifest = run_ingestion(
        raw_dir=args.raw_dir,
        processed_dir=args.processed_dir,
        ingest_run_id=args.ingest_run_id,
    )
    print(
        f"ingest_run_id={manifest.ingest_run_id} "
        f"documents={manifest.document_count} chunks={manifest.chunk_count}"
    )


if __name__ == "__main__":
    main()
