import argparse
import json
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from domain_shot.build_domain_shot_prompt import DEFAULT_PAPERS_DIR
from domain_shot.evaluation import DEFAULT_MODEL, evaluate_all


def main() -> None:
	parser = argparse.ArgumentParser(
		description="Run domain-shot LLM evaluation over one or more markdown papers."
	)
	parser.add_argument(
		"--papers_dir",
		type=str,
		default=DEFAULT_PAPERS_DIR,
		help="Directory containing markdown papers to evaluate.",
	)
	parser.add_argument(
		"--model",
		type=str,
		default=DEFAULT_MODEL,
		help="Model identifier to send to OpenRouter.",
	)
	parser.add_argument(
		"--prompt_mode",
		type=str,
		choices=["domain_guidance", "tree_questions"],
		default="domain_guidance",
		help="Prompt builder mode.",
	)
	parser.add_argument(
		"--output_json",
		type=str,
		default=None,
		help="Optional path to save full results as JSON.",
	)
	args = parser.parse_args()

	results = evaluate_all(
		papers_dir=args.papers_dir,
		model=args.model,
		prompt_mode=args.prompt_mode,
	)

	if args.output_json:
		with open(args.output_json, "w", encoding="utf-8") as handle:
			json.dump(results, handle, indent=2, ensure_ascii=False)
		print(f"Saved results to {args.output_json}")
	else:
		print(f"Completed evaluation for {len(results)} paper(s) using mode '{args.prompt_mode}'.")


if __name__ == "__main__":
	main()
