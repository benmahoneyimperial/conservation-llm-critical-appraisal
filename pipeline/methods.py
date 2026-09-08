"""The three appraisal methods, each evaluating one paper and returning 7 domains.

All three share the same signature so the runner can treat them identically.
Existing appraisal logic is reused, not reimplemented.
"""

import functools

from domain_shot import evaluation as ds_eval
from domain_shot.build_question_scoring_prompt import build_prompt_messages as qs_messages
from domain_shot.build_question_scoring_prompt import load_domain_questions
from domain_shot.build_tree_guided_prompt import build_prompt_messages as tg_messages
from domain_shot.build_tree_guided_prompt import (
    load_default_domain_prompt_parts,
    load_default_guidance_intro,
)
from sequential_decision_tree.llm_client import ask_llm
from sequential_decision_tree.trees import TREES
from sequential_decision_tree.evaluator import traverse_tree

from .config import GUIDANCE_PATH

DOMAIN_NAMES = [f"domain_{i}" for i in range(1, 8)]


@functools.lru_cache(maxsize=1)
def _guidance_intro() -> str:
    return load_default_guidance_intro()


@functools.lru_cache(maxsize=1)
def _guidance_text() -> str:
    return GUIDANCE_PATH.read_text(encoding="utf-8")


@functools.lru_cache(maxsize=1)
def _tree_parts() -> dict:
    return load_default_domain_prompt_parts()


def run_sequential(paper_text: str, model: str) -> dict:
    """Walk each decision tree question by question."""
    results = {}
    guidance = _guidance_text()

    for tree_id, tree in TREES.items():
        start_node = "start" if "start" in tree else f"q_{tree_id}_1"
        output = traverse_tree(
            tree,
            paper_text,
            start_node=start_node,
            guidance_text=guidance,
            verbose=False,
            ask=lambda *a, **kw: ask_llm(*a, model=model, **kw),
        )

        results[tree_id] = {"result": output["result"], "path": output["path"]}
        if output.get("error"):
            results[tree_id]["error"] = output["error"]
            results[tree_id]["failed_node"] = output.get("failed_node")
            results["overall"] = f"ERROR: Tree {tree_id} failed at {output.get('failed_node')}"
            return results

    results["overall"] = _overall_risk(results)
    return results


def run_tree_guided(paper_text: str, model: str) -> dict:
    """One call per domain, giving the model the full decision tree."""
    results = {}
    for domain, payload in _tree_parts().items():
        messages = tg_messages(
            domain,
            _guidance_intro(),
            payload["decision_tree_text"],
            payload["domain_questions_text"],
            paper_text,
        )
        results[_domain_key(domain)] = _call(domain, messages, model)
    return _finalise(results)


def run_question_scoring(paper_text: str, model: str) -> dict:
    """One call per domain, asking for a 0-10 risk score."""
    results = {}
    for domain in DOMAIN_NAMES:
        messages = qs_messages(domain, _guidance_intro(), load_domain_questions(domain), paper_text)
        results[_domain_key(domain)] = _call(domain, messages, model)
    return _finalise(results)


METHODS = {
    "sequential": run_sequential,
    "tree_guided": run_tree_guided,
    "question_scoring": run_question_scoring,
}


def _domain_key(domain_name: str) -> str:
    """Store domains as "1".."7" so all methods share one result shape."""
    return domain_name.replace("domain_", "")


def _call(domain: str, messages: list, model: str) -> dict:
    try:
        return ds_eval.call_llm_and_process(domain, messages, model)
    except Exception as exc:  # noqa: BLE001 - recorded so the paper is retried later
        return {"error": str(exc)}


def _finalise(results: dict) -> dict:
    for domain, entry in results.items():
        if entry.get("error"):
            results["overall"] = f"ERROR: Domain {domain} failed"
            return results

    results["overall"] = _overall_risk(results)
    return results


def _overall_risk(results: dict) -> str:
    """Highest risk across domains wins."""
    text = " ".join(str(entry) for key, entry in results.items() if key != "overall").lower()
    if "high" in text:
        return "HIGH RISK"
    if "med" in text:
        return "MEDIUM RISK"
    return "LOW RISK"
