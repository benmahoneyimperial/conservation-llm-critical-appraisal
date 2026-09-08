"""Builds the work list and runs it. Models run in parallel; papers run in order."""

import json
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path

from . import store
from .config import CHUNK_SIZE, PAPER_FIRST, PAPER_LAST, PAPERS_DIR
from .methods import METHODS


@dataclass
class Task:
    model: str
    method: str
    paper_ids: list[str]

    def __str__(self) -> str:
        return f"{self.model} | {self.method} | {self.paper_ids[0]}-{self.paper_ids[-1]}"


def find_papers(papers_dir: Path = PAPERS_DIR, first: int = PAPER_FIRST, last: int = PAPER_LAST) -> list[str]:
    """Paper IDs in the configured range that actually exist on disk."""
    ids = []
    for path in sorted(papers_dir.glob("*.json")):
        if path.stem.isdigit() and first <= int(path.stem) <= last:
            ids.append(path.stem)
    return ids


def read_paper(paper_id: str, papers_dir: Path = PAPERS_DIR) -> str:
    data = json.loads((papers_dir / f"{paper_id}.json").read_text(encoding="utf-8"))
    return json.dumps(data, indent=2, ensure_ascii=False)


def build_tasks(models: list[str], methods: list[str], paper_ids: list[str], chunk_size: int = CHUNK_SIZE) -> list[Task]:
    """One task per model/method/chunk, containing only papers still to do."""
    tasks = []
    for model in models:
        for method in methods:
            todo = [pid for pid in paper_ids if not store.is_complete(model, method, pid)]
            for start in range(0, len(todo), chunk_size):
                tasks.append(Task(model, method, todo[start:start + chunk_size]))
    return tasks


def run_task(task: Task, papers_dir: Path = PAPERS_DIR) -> dict:
    """Evaluate a chunk, saving after every paper."""
    run_method = METHODS[task.method]
    done, failed = 0, 0

    for paper_id in task.paper_ids:
        if store.is_complete(task.model, task.method, paper_id):
            continue

        try:
            result = run_method(read_paper(paper_id, papers_dir), task.model)
        except Exception as exc:  # noqa: BLE001 - saved so this paper retries next run
            result = {"overall": f"ERROR: {exc}"}

        store.save(task.model, task.method, paper_id, result)

        if str(result.get("overall", "")).startswith("ERROR:"):
            failed += 1
            print(f"  FAILED {task.model} {task.method} {paper_id}")
        else:
            done += 1
            print(f"  ok     {task.model} {task.method} {paper_id}")

    return {"task": str(task), "completed": done, "failed": failed}


def run_all(tasks: list[Task], workers: int, papers_dir: Path = PAPERS_DIR) -> list[dict]:
    """Run tasks concurrently. Keep workers close to the number of models."""
    if workers <= 1:
        return [run_task(task, papers_dir) for task in tasks]

    with ThreadPoolExecutor(max_workers=workers) as pool:
        return list(pool.map(lambda task: run_task(task, papers_dir), tasks))
