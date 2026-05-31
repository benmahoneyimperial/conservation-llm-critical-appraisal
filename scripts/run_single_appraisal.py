import os
import sys
import argparse
import re

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from appraisal.evaluator import run_all_trees

def analyse_single_paper(file_path: str, quiet: bool = False):
    """
    Reads a single .md or .txt file, runs analysis on it, and prints the results.
    """
    if not os.path.exists(file_path):
        print(f"Error: File not found at '{file_path}'")
        return

    paper_name = os.path.basename(file_path)
    print(f"\n--- Analyzing: {paper_name} ---")

    with open(file_path, "r", encoding="utf-8") as f:
        paper_text = f.read()

    if not paper_text.strip():
        print("  - Warning: Text file is empty, skipping.")
        return

    results = run_all_trees(paper_text, verbose=not quiet)

    print("\n" + "="*30)
    print(f"=== FINAL RESULTS for {paper_name} ===")
    print("="*30)

    if isinstance(results, dict):
        for tree_name, tree_data in results.items():
            if tree_name == "overall":
                print(f"\n--- OVERALL BIAS RISK ---")
                print(f"  Final Judgment: {tree_data}")
                continue
            print(f"\n--- {tree_name} ---")
            final_judgment = tree_data.get("result", "N/A")
            if tree_data.get("error"):
                print(f"  Error: {tree_data['error']}")
                failed_node = tree_data.get("failed_node")
                if failed_node:
                    print(f"  Failed Node: {failed_node}")
            for step in tree_data.get("path", []):
                print(f"  Node: {step['node']}")
                print(f"  LLM Final Answer: {step['answer']}")
                if not quiet:
                    print(f"  LLM Full Response:\n{step['full_response']}\n")
            print(f"  Final Judgment for Tree {tree_name}: {final_judgment}")
    else:
        print(f"  - {results}") # Fallback for unexpected format (e.g., if run_all_trees returns a string error)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the critical appraisal pipeline on a single processed markdown or text file.")
    parser.add_argument("file_path", type=str, help="The path to the processed .md or .txt paper file to analyse.")
    parser.add_argument("--quiet", action="store_true", help="Suppress detailed step-by-step reasoning logs.")
    args = parser.parse_args()
    analyse_single_paper(args.file_path, quiet=args.quiet)
