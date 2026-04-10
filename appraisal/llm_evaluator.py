import os
from .tree_data import TREES
from .llm_client import ask_llm

def traverse_tree(tree, paper_text, start_node = "q_1_1", verbose = True):
    node_id = start_node
    path = []
    chat_history = []

    while True:
        node = tree[node_id]

        # If leaf node then return result
        if isinstance(node, str):
            if verbose:
                print(f"\nFinal Result: {node}")
            return {
                "result": node,
                "path": path
            }

        # Ask LLM
        response = ask_llm(node["question"], paper_text, chat_history=chat_history, valid_answers=node.get("valid_answers"))
        answer = response["final_answer"]

        answer = answer.strip().lower()

        # Validate answer DO I WANT TO FORCE A 'no' if answer is invalid? PROS: keeps us on the tree, CONS: may bias towards 'no' if LLM is confused. Maybe better to return an error and mark this question as failed?
        if answer not in node["valid_answers"]:
            if verbose:
                print(f"Invalid answer '{answer}' → forcing 'no'")
            answer = "no"

        if verbose:
            print(f"\nNode: {node_id}")
            print(f"Answer: {answer}")
            # print(f"Full response: {response['full_response']}")

        # Store trace
        path.append({
            "node": node_id,
            "answer": answer,
            "full_response": response["full_response"]
        })

        # Update chat history for the next node
        chat_history.append({"role": "user", "content": node["question"]})
        if response["full_response"]:
            chat_history.append({"role": "assistant", "content": response["full_response"]})

        # Move to next node
        node_id = node["mapping"][answer]


def run_all_trees(paper_text, verbose=True):
    results = {}

    for tree_id, tree in TREES.items():
        if verbose:
            print(f"\n--- Running Tree {tree_id} ---")

        start_node = "start" if "start" in tree else f"q_{tree_id}_1"
        output = traverse_tree(tree, paper_text, start_node=start_node, verbose=verbose)

        results[tree_id] = {
            "result": output["result"],
            "path": output["path"]
        }

    # Calculate overall bias risk
    overall_risk = "LOW RISK"
    has_medium = False
    for tree_id, tree_data in results.items():
        res_str = str(tree_data["result"]).lower()
        if "high" in res_str:
            overall_risk = "HIGH RISK"
            break
        elif "med" in res_str:
            has_medium = True
            
    if overall_risk != "HIGH RISK" and has_medium:
        overall_risk = "MEDIUM RISK"
        
    results["overall"] = overall_risk

    if verbose:
        print(f"\n--- Overall Bias Risk: {overall_risk} ---")

    return results


def analyse_all_papers(processed_dir: str, verbose: bool = True):
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

        all_results[paper_name] = run_all_trees(paper_text, verbose=verbose)

    return all_results
