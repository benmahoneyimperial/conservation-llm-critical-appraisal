"""Show progress per model and method."""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from pipeline import runner, store
from pipeline.config import METHODS, MODELS


def main() -> None:
    paper_ids = runner.find_papers()
    print(f"Papers in range: {len(paper_ids)}\n")
    print(f"{'model':<28} {'method':<18} {'done':>6} {'failed':>7} {'todo':>6}")
    print("-" * 70)

    for model in MODELS:
        for method in METHODS:
            saved = store.load_all(model, method)
            done = sum(1 for pid in paper_ids if store.is_complete(model, method, pid))
            failed = sum(
                1
                for pid in paper_ids
                if pid in saved and not store.is_complete(model, method, pid)
            )
            print(f"{model:<28} {method:<18} {done:>6} {failed:>7} {len(paper_ids) - done:>6}")


if __name__ == "__main__":
    main()
