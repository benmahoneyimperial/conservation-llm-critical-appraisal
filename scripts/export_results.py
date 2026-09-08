"""Merge per-paper files into one JSON per model/method for analysis."""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from pipeline import store
from pipeline.config import METHODS, MODELS, RESULTS_DIR, model_tag

OUTPUT_DIR = RESULTS_DIR.parent / "exports"


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for model in MODELS:
        for method in METHODS:
            results = store.load_all(model, method)
            if not results:
                continue

            payload = {
                "model": model,
                "method": method,
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                "domains": store.DOMAINS,
                "results": results,
            }

            path = OUTPUT_DIR / f"{method}_{model_tag(model)}.json"
            path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
            print(f"{len(results):>4} papers -> {path.relative_to(RESULTS_DIR.parent.parent)}")


if __name__ == "__main__":
    main()
