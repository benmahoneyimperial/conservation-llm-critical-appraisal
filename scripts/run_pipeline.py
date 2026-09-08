"""Main entry point. Run the appraisal methods across models, in chunks, resumably.

Examples:
    python scripts/run_pipeline.py --dry-run
    python scripts/run_pipeline.py --limit 2
    python scripts/run_pipeline.py
"""

import argparse
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from pipeline import runner
from pipeline.config import CHUNK_SIZE, METHODS, MODELS, PAPER_FIRST, PAPER_LAST, PAPERS_DIR


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--models", nargs="+", default=MODELS)
    parser.add_argument("--methods", nargs="+", default=METHODS)
    parser.add_argument("--first", type=int, default=PAPER_FIRST, help="Lowest paper ID to include.")
    parser.add_argument("--last", type=int, default=PAPER_LAST, help="Highest paper ID to include.")
    parser.add_argument("--chunk-size", type=int, default=CHUNK_SIZE)
    parser.add_argument("--workers", type=int, default=len(MODELS))
    parser.add_argument("--limit", type=int, help="Only use the first N papers (cheap smoke test).")
    parser.add_argument("--dry-run", action="store_true", help="Show the plan without calling any API.")
    args = parser.parse_args()

    paper_ids = runner.find_papers(first=args.first, last=args.last)
    if args.limit:
        paper_ids = paper_ids[: args.limit]

    tasks = runner.build_tasks(args.models, args.methods, paper_ids, args.chunk_size)
    remaining = sum(len(task.paper_ids) for task in tasks)
    total = len(paper_ids) * len(args.models) * len(args.methods)

    print(f"Papers {args.first}-{args.last} found in {PAPERS_DIR.name}: {len(paper_ids)}")
    print(f"Models: {', '.join(args.models)}")
    print(f"Methods: {', '.join(args.methods)}")
    print(f"Appraisals: {total} total, {total - remaining} already done, {remaining} to run")
    print(f"Tasks: {len(tasks)} (chunk size {args.chunk_size}, {args.workers} workers)\n")

    if args.dry_run:
        for task in tasks:
            print(f"  {task}  ({len(task.paper_ids)} papers)")
        print("\nDry run only. Nothing was called.")
        return

    if not tasks:
        print("Nothing to do.")
        return

    summaries = runner.run_all(tasks, args.workers)

    completed = sum(item["completed"] for item in summaries)
    failed = sum(item["failed"] for item in summaries)
    print(f"\nDone. {completed} succeeded, {failed} failed.")
    if failed:
        print("Re-run the same command to retry only the failures.")


if __name__ == "__main__":
    main()
