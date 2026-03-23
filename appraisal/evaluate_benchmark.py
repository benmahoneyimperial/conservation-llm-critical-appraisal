import os
import sys
import csv
import argparse

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from appraisal.llm_client import ask_llm
from appraisal.llm_evaluator import traverse_tree
from appraisal.tree_data import (
    decision_tree_1, decision_tree_2, decision_tree_3, 
    decision_tree_4, decision_tree_5, decision_tree_6, decision_tree_7
)

TREES = {
    "1": decision_tree_1,
    "2": decision_tree_2,
    "3": decision_tree_3,
    "4": decision_tree_4,
    "5": decision_tree_5,
    "6": decision_tree_6,
    "7": decision_tree_7
}

def load_paper_text(processed_dir, filename):
    filepath = os.path.join(processed_dir, filename)

    # Try exact match, .txt appended, and .pdf.txt appended (common from preprocessing)
    candidates = [filepath, filepath + ".txt", filepath + ".pdf.txt"]

    for candidate in candidates:
        if os.path.exists(candidate):
            with open(candidate, "r", encoding="utf-8") as f:
                return f.read()

    return None

def run_benchmark(benchmark_csv, processed_dir, verbose=True):
    if verbose:
        print(f"--- Running Benchmark from {benchmark_csv} ---")
    
    correct_count = 0
    total_count = 0
    failures = []
    
    with open(benchmark_csv, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            filename = row["filename"]
            tree_idx = row["tree_index"]
            expected = row["expected_answer"].lower()
            
            paper_text = load_paper_text(processed_dir, filename)
            if not paper_text:
                if verbose:
                    print(f"Skipping {filename}: File not found.")
                continue
                
            tree = TREES.get(str(tree_idx))
            if not tree:
                if verbose:
                    print(f"Skipping {filename}: Invalid Tree {tree_idx}")
                continue

            if verbose:
                print(f"\nTesting {filename} | Tree {tree_idx} (Full Traversal)")
            
            # Run the Full Tree Traversal
            actual = traverse_tree(tree, paper_text, verbose=verbose).lower()
            
            # Basic normalization for comparison
            is_correct = expected in actual
            
            status = "PASS" if is_correct else "FAIL"
            if verbose:
                print(f"  [{status}] Expected: '{expected}' | Actual: '{actual}'")
            
            if is_correct:
                correct_count += 1
            else:
                failures.append(f"Expected: {expected} | Actual: {actual}")
            total_count += 1

    accuracy = 0.0
    if total_count > 0:
        accuracy = correct_count / total_count
        if verbose:
            print(f"\n--- Benchmark Complete ---")
            print(f"Accuracy: {correct_count}/{total_count} ({accuracy:.2%})")
    elif verbose:
        print("No valid benchmark entries found.")
        
    return accuracy, failures

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run benchmark tests against the LLM decision tree pipeline."
    )
    parser.add_argument(
        "benchmark_csv",
        type=str,
        nargs="?",
        default="data/benchmark.csv",
        help="Path to the benchmark CSV file. Defaults to 'data/benchmark.csv'."
    )
    parser.add_argument(
        "--processed_dir",
        type=str,
        default="data/processed_text",
        help="Directory containing the processed .txt paper files."
    )
    args = parser.parse_args()
    run_benchmark(args.benchmark_csv, args.processed_dir)