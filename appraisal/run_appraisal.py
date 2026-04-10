import os
import sys
import argparse
import csv

# Add the project root to the python path so we can import the appraisal package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from appraisal.llm_evaluator import analyse_all_papers, run_all_trees

def main():
    parser = argparse.ArgumentParser(description="Run the full critical appraisal pipeline on a single text file or a directory of processed text files.")
    parser.add_argument(
        "target",
        nargs="?",
        default="data/processed_text", 
        help="Path to a single .txt file or a directory containing processed .txt files."
    )
    parser.add_argument("--output_csv", type=str, default=None, help="Optional path to save the results as a CSV file.")
    parser.add_argument("--quiet", action="store_true", help="Suppress detailed step-by-step reasoning logs.")
    args = parser.parse_args()

    final_results = {}
    if os.path.isfile(args.target):
        paper_name = os.path.basename(args.target)
        print(f"\n--- Analyzing single file: {paper_name} ---")
        with open(args.target, "r", encoding="utf-8") as f:
            paper_text = f.read()
        if paper_text.strip():
            final_results[paper_name] = run_all_trees(paper_text, verbose=not args.quiet)
        else:
            print("  - Warning: Text file is empty, skipping.")
    elif os.path.isdir(args.target):
        final_results = analyse_all_papers(args.target, verbose=not args.quiet)
    else:
        print(f"Error: Target '{args.target}' is not a valid file or directory.")
        return
    
    if not final_results:
        print("No analysis was run.")
        return

    # Determine column widths
    col_width_paper = max(20, max([len(p) for p in final_results.keys()] + [10]))
    col_width_domain = 15
    
    trees = [str(i) for i in range(1, 8)]
    domain_headers = [f"Domain {i}" for i in trees]
    headers = ["Paper Name"] + domain_headers + ["Overall"]
    
    header_format = f"{{:<{col_width_paper}}} | " + " | ".join([f"{{:<{col_width_domain}}}"] * len(domain_headers)) + f" | {{:<{col_width_domain}}}"
    sep_line = "-" * len(header_format.format(*([""] * len(headers))))
    
    print("\n\n" + "=" * len(sep_line))
    print("=== FINAL CONSOLIDATED RESULTS ===")
    print("=" * len(sep_line))
    print(header_format.format(*headers))
    print(sep_line)
    
    for paper, results in final_results.items():
        if isinstance(results, dict):
            row = [paper]
            for t in trees:
                tree_data = results.get(t, {})
                val = tree_data.get("result", "N/A") if isinstance(tree_data, dict) else "N/A"
                # Extract just the main risk category (e.g., "LOW RISK" instead of "LOW RISK: explanation...")
                val_str = str(val).split(':')[0].strip() if ':' in str(val) else str(val)
                row.append(val_str[:col_width_domain])
            
            overall = results.get("overall", "N/A")
            row.append(str(overall)[:col_width_domain])
            print(header_format.format(*row))
        else:
            row = [paper] + ["Error"] * len(trees) + [str(results)[:col_width_domain]]
            print(header_format.format(*row))
    print("=" * len(sep_line) + "\n")

    if args.output_csv:
        try:
            with open(args.output_csv, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                
                for paper, results in final_results.items():
                    if isinstance(results, dict):
                        row = [paper]
                        for t in trees:
                            tree_data = results.get(t, {})
                            val = tree_data.get("result", "N/A") if isinstance(tree_data, dict) else "N/A"
                            val_str = str(val).split(':')[0].strip() if ':' in str(val) else str(val)
                            row.append(val_str)
                        row.append(str(results.get("overall", "N/A")))
                        writer.writerow(row)
                    else:
                        writer.writerow([paper] + ["Error"] * len(trees) + [str(results)])
            print(f"Results successfully saved to '{args.output_csv}'\n")
        except Exception as e:
            print(f"Error saving to CSV: {e}\n")

if __name__ == "__main__":
    main()