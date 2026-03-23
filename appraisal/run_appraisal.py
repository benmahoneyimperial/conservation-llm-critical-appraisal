import os
import sys
import argparse

# Add the project root to the python path so we can import the appraisal package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from appraisal.llm_evaluator import analyse_all_papers

def main():
    parser = argparse.ArgumentParser(description="Run the full critical appraisal pipeline on processed text files.")
    parser.add_argument(
        "--processed_dir", 
        default="data/processed_text", 
        help="Directory containing the processed .txt paper files."
    )
    args = parser.parse_args()

    final_results = analyse_all_papers(args.processed_dir)
    
    print("\n\n" + "="*30)
    print("=== FINAL CONSOLIDATED RESULTS ===")
    print("="*30)
    
    if final_results:
        for paper, results in final_results.items():
            print(f"\nPaper: {paper}")
            if isinstance(results, dict):
                for tree, result in results.items():
                    print(f"  - {tree}: {result}")
            else:
                print(f"  - {results}")
    else:
        print("No analysis was run.")

if __name__ == "__main__":
    main()