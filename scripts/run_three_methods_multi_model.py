import argparse
import json
import sys
from pathlib import Path

repo_root = Path(__file__).resolve().parents[1]
sys.path.append(str(repo_root))

from domain_shot import evaluation as ds_eval
from domain_shot.build_question_scoring_prompt import build_prompt_messages as qs_messages
from domain_shot.build_question_scoring_prompt import load_domain_questions
from domain_shot.build_tree_guided_prompt import build_prompt_messages as tg_messages
from domain_shot.build_tree_guided_prompt import load_default_domain_prompt_parts, load_default_guidance_intro
from sequential_decision_tree import evaluator as seq_eval
from sequential_decision_tree import llm_client as seq_client


def _safe(name: str) -> str:
    return name.replace("/", "_").replace(":", "_").replace(" ", "_")


def _load_papers(papers_dir: Path) -> dict[str, str]:
    papers = {}
    for p in sorted(papers_dir.glob("*.json")):
        papers[p.name] = json.dumps(json.loads(p.read_text(encoding="utf-8")), ensure_ascii=False)
    return papers


def _run_tree_guided(model: str, intro: str, parts: dict, papers: dict[str, str]) -> dict:
    out = {}
    for paper_name, paper_text in papers.items():
        out[paper_name] = {}
        for domain, payload in parts.items():
            messages = tg_messages(domain, intro, payload["decision_tree_text"], payload["domain_questions_text"], paper_text)
            out[paper_name][domain] = ds_eval.call_llm_and_process(domain, messages, model)
    return {"model": model, "results": out}


def _run_question_scoring(model: str, intro: str, domains: list[str], papers: dict[str, str]) -> dict:
    out = {}
    for paper_name, paper_text in papers.items():
        out[paper_name] = {}
        for domain in domains:
            messages = qs_messages(domain, intro, load_domain_questions(domain), paper_text)
            out[paper_name][domain] = ds_eval.call_llm_and_process(domain, messages, model)
    return {"model": model, "results": out}


def _run_sequential(model: str, papers_dir: Path, guidance_path: Path, checkpoint_path: Path) -> dict:
    original_ask = seq_eval.ask_llm

    def ask_with_model(prompt, context, prior_context=None, guidance_text=None, valid_answers=None):
        return seq_client.ask_llm(
            prompt,
            context,
            prior_context=prior_context,
            guidance_text=guidance_text,
            valid_answers=valid_answers,
            model=model,
        )

    try:
        seq_eval.ask_llm = ask_with_model
        results = seq_eval.analyse_all_papers(
            processed_dir=str(papers_dir),
            guidance_path=str(guidance_path),
            verbose=False,
            checkpoint_path=str(checkpoint_path),
            resume=True,
        )
    finally:
        seq_eval.ask_llm = original_ask

    return {"model": model, "results": results}


def main():
    parser = argparse.ArgumentParser(description="Run sequential, tree-guided, and question-scoring across models.")
    parser.add_argument("--models", nargs="+", required=True)
    parser.add_argument("--papers-dir", default="data/papers/json/1_to_100")
    parser.add_argument("--output-dir", default="output/three_methods_multi_model/1_to_100")
    parser.add_argument("--guidance-path", default="data/guidance_intro_md/guidance_intro.md")
    args = parser.parse_args()

    papers_dir = Path(args.papers_dir)
    output_dir = Path(args.output_dir)
    guidance_path = Path(args.guidance_path)
    output_dir.mkdir(parents=True, exist_ok=True)

    intro = load_default_guidance_intro()
    tree_parts = load_default_domain_prompt_parts()
    domains = sorted(tree_parts.keys())
    papers = _load_papers(papers_dir)

    for model in args.models:
        tag = _safe(model)
        print(f"\n=== Model: {model} ===")

        sequential = _run_sequential(
            model,
            papers_dir,
            guidance_path,
            papers_dir / f".sequential_checkpoint_{tag}.json",
        )
        tree_guided = _run_tree_guided(model, intro, tree_parts, papers)
        question_scoring = _run_question_scoring(model, intro, domains, papers)

        (output_dir / f"sequential_{tag}.json").write_text(json.dumps(sequential, indent=2, ensure_ascii=False), encoding="utf-8")
        (output_dir / f"tree_guided_{tag}.json").write_text(json.dumps(tree_guided, indent=2, ensure_ascii=False), encoding="utf-8")
        (output_dir / f"question_scoring_{tag}.json").write_text(json.dumps(question_scoring, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Saved: sequential_{tag}.json, tree_guided_{tag}.json, question_scoring_{tag}.json")


if __name__ == "__main__":
    main()