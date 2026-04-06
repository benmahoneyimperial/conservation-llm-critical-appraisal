import os
import sys
import argparse
import re

# Add the project root to the python path so we can import the appraisal package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from appraisal.llm_evaluator import run_all_trees

def analyse_single_paper(file_path: str):
    """
    Reads a single .txt file, runs analysis on it, and prints the results.
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

    results = run_all_trees(paper_text)

    print("\n" + "="*30)
    print(f"=== FINAL RESULTS for {paper_name} ===")
    print("="*30)

    if isinstance(results, dict):
        for tree_name, tree_data in results.items():
            print(f"\n--- {tree_name} ---")
            final_judgment = tree_data.get("result", "N/A")
            for step in tree_data.get("path", []):
                print(f"  Node: {step['node']}")
                print(f"  LLM Final Answer: {step['answer']}")
                print(f"  LLM Full Response:\n{step['full_response']}\n")
            print(f"  Final Judgment for Tree {tree_name}: {final_judgment}")
    else:
        print(f"  - {results}") # Fallback for unexpected format (e.g., if run_all_trees returns a string error)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the critical appraisal pipeline on a single processed text file.")
    parser.add_argument("file_path", type=str, help="The path to the processed .txt paper file to analyze.")
    args = parser.parse_args()
    analyse_single_paper(args.file_path)