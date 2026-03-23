import os
from .tree_data import decision_tree_1, decision_tree_2, decision_tree_3, decision_tree_4, decision_tree_5, decision_tree_6, decision_tree_7
from .llm_client import ask_llm

def traverse_tree(tree, paper_text, node_id="start", verbose=True):
    """Traverse the decision tree asking questions and following paths."""
    node = tree[node_id]
    
    if isinstance(node, str):
        return node
    
    # For batch processing, we'll just print the question.
    # The actual ask_llm call is now the main part of the logic.
    if verbose:
        print(f"  - Asking: {node['question'][:100]}...")
    answer = ask_llm(node["question"], paper_text)
    if verbose:
        print(f"    > Answer: {answer}")
    
    # Simplified logic for demonstration
    if "yes" in answer.lower():
        return traverse_tree(tree, paper_text, node["yes"], verbose=verbose)
    else:
        return traverse_tree(tree, paper_text, node["no"], verbose=verbose)


def run_all_trees(paper_text):
    """Run all configured decision trees on a single paper's text."""
    results = {}
    trees = {
        "Tree 1 (Confounding)": decision_tree_1,
        "Tree 2 (Selection)": decision_tree_2,
        "Tree 3 (Intervention)": decision_tree_3,
        "Tree 4 (Performance)": decision_tree_4,
        "Tree 5 (Detection)": decision_tree_5,
        "Tree 6 (Reporting)": decision_tree_6,
        "Tree 7 (Analysis)": decision_tree_7
    }
    
    for name, tree in trees.items():
        results[name] = traverse_tree(tree, paper_text)
        
    return results


def analyse_all_papers(processed_dir: str):
    """
    Reads all .txt files from a directory, runs analysis on each, and returns
    a dictionary of results.
    """
    print(f"--- Starting Analysis on All Papers in '{processed_dir}' ---")
    all_results = {}
    
    text_files = [f for f in os.listdir(processed_dir) if f.endswith(".txt")]

    if not text_files:
        print("No processed text files found. Did you run the 'preprocess_pdfs.py' script?")
        return

    for text_file in text_files:
        paper_name = os.path.splitext(text_file)[0]
        print(f"\n--- Analyzing: {paper_name} ---")
        
        file_path = os.path.join(processed_dir, text_file)
        with open(file_path, "r", encoding="utf-8") as f:
            paper_text = f.read()

        if not paper_text.strip():
            print("  - Warning: Text file is empty, skipping.")
            all_results[paper_name] = "Skipped (empty file)"
            continue

        all_results[paper_name] = run_all_trees(paper_text)

    return all_results
