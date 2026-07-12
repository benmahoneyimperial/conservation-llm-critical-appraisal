import os
from .trees import TREES
from .llm_client import ask_llm

def build_prior_context(path, max_steps: int = 2):
    """Summarise the most recent node decisions for the next question."""
    if not path:
        return None

    recent_steps = path[-max_steps:]
    lines = ["Previous node decisions:"]
    for step in recent_steps:
        lines.append(f"- {step['node']}: {step['question']}")
        lines.append(f"  Answer: {step['answer']}")
    return "\n".join(lines)


def traverse_tree(tree, paper_text, start_node = "q_1_1", guidance_text = None, verbose = True):
    node_id = start_node
    path = []

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
        prior_context = build_prior_context(path)
        response = ask_llm(
            node["question"],
            paper_text,
            prior_context=prior_context,
            guidance_text=guidance_text,
            valid_answers=node.get("valid_answers"),
        )
        if response.get("error"):
            error_message = response["error"]
            if verbose:
                print(f"\nNode: {node_id}")
                print(f"Error: {error_message}")
            return {
                "result": f"ERROR: {error_message}",
                "path": path,
                "error": error_message,
                "failed_node": node_id,
            }

        answer = response.get("final_answer")
        if not answer:
            error_message = "LLM response did not include a final answer in [[...]] format."
            if verbose:
                print(f"\nNode: {node_id}")
                print(f"Error: {error_message}")
                print(f"LLM Full Response:\n{response.get('full_response')}\n")
            return {
                "result": f"ERROR: {error_message}",
                "path": path,
                "error": error_message,
                "failed_node": node_id,
            }

        answer = answer.strip().lower()

        # Validate answer
        if answer not in node["valid_answers"]:
            if verbose:
                print(f"Invalid answer '{answer}' → forcing 'unclear'")
            answer = "unclear" if "unclear" in node["valid_answers"] else node["valid_answers"][0]

        if verbose:
            print(f"\nNode: {node_id}")
            print(f"Answer: {answer}")
            # print(f"Full response: {response['full_response']}")

        # Store trace
        path.append({
            "node": node_id,
            "question": node["question"],
            "answer": answer,
            "full_response": response["full_response"]
        })

        # Move to next node
        node_id = node["mapping"][answer]


def run_all_trees(paper_text, guidance_text=None, verbose=True):
    results = {}

    for tree_id, tree in TREES.items():
        if verbose:
            print(f"\n--- Running Tree {tree_id} ---")

        start_node = "start" if "start" in tree else f"q_{tree_id}_1"
        output = traverse_tree(tree, paper_text, start_node=start_node, guidance_text=guidance_text, verbose=verbose)

        results[tree_id] = {
            "result": output["result"],
            "path": output["path"]
        }
        if output.get("error"):
            results[tree_id]["error"] = output["error"]
            results[tree_id]["failed_node"] = output.get("failed_node")
            results["overall"] = f"ERROR: Tree {tree_id} failed at {output.get('failed_node')}"
            if verbose:
                print(f"\n--- Stopping early: Tree {tree_id} failed at {output.get('failed_node')} ---")
            return results

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


def analyse_all_papers(processed_dir: str, guidance_path: str = None, verbose: bool = True):
    """
    Reads all .txt files from a directory, runs analysis on each, and returns
    a dictionary of results.
    """
    print(f"--- Starting Analysis on All Papers in '{processed_dir}' ---")
    
    guidance_text = None
    if guidance_path and os.path.exists(guidance_path):
        with open(guidance_path, "r", encoding="utf-8") as gf:
            guidance_text = gf.read()
        print(f"  -> Loaded CEECAT guidance from {guidance_path}")

    all_results = {}
    
    text_files = [f for f in os.listdir(processed_dir) if f.endswith(".txt") or f.endswith(".md")]

    if not text_files:
        print("No processed text or markdown files found in the specified directory.")
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

        all_results[paper_name] = run_all_trees(paper_text, guidance_text=guidance_text, verbose=verbose)

    return all_results
