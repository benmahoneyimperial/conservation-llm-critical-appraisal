"""One JSON file per (model, method, paper). Makes resume simple and safe."""

import json
import os
from pathlib import Path

from .config import RESULTS_DIR, model_tag

DOMAINS = [str(i) for i in range(1, 8)]


def result_path(model: str, method: str, paper_id: str) -> Path:
    return RESULTS_DIR / model_tag(model) / method / f"{paper_id}.json"


def is_complete(model: str, method: str, paper_id: str) -> bool:
    """A paper is done only if its saved result has all 7 domains and no errors."""
    path = result_path(model, method, paper_id)
    if not path.exists():
        return False

    try:
        result = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return False

    if not isinstance(result, dict) or str(result.get("overall", "")).startswith("ERROR:"):
        return False

    for domain in DOMAINS:
        entry = result.get(domain)
        if not isinstance(entry, dict) or entry.get("error") or entry.get("failed_node"):
            return False

    return True


def save(model: str, method: str, paper_id: str, result: dict) -> Path:
    """Write atomically so an interruption can never leave a half-written file."""
    path = result_path(model, method, paper_id)
    path.parent.mkdir(parents=True, exist_ok=True)

    temp_path = path.with_suffix(".json.tmp")
    temp_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    os.replace(temp_path, path)
    return path


def load_all(model: str, method: str) -> dict:
    """Load every saved result for a model/method, keyed by paper ID."""
    directory = RESULTS_DIR / model_tag(model) / method
    if not directory.exists():
        return {}

    results = {}
    for path in sorted(directory.glob("*.json")):
        try:
            results[path.stem] = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
    return results
