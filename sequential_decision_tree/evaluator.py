import os
import json
import datetime
from .trees import TREES
from .llm_client import ask_llm


def _default_checkpoint_path(processed_dir: str) -> str:
    return os.path.join(processed_dir, ".sequential_decision_tree_checkpoint.json")


def _load_checkpoint(checkpoint_path: str) -> dict:
    with open(checkpoint_path, "r", encoding="utf-8") as f:
        payload = json.load(f)

    # Backward compatible: support plain {paper_name: result} checkpoint format.
    if isinstance(payload, dict) and "results" in payload and isinstance(payload["results"], dict):
        return payload["results"]
    if isinstance(payload, dict):
        return payload
    raise ValueError("Checkpoint file format is invalid.")


def _save_checkpoint(checkpoint_path: str, results: dict, processed_dir: str, guidance_path: str | None):
    os.makedirs(os.path.dirname(checkpoint_path) or ".", exist_ok=True)
    payload = {
        "saved_at": datetime.datetime.now().isoformat(),
        "processed_dir": processed_dir,
        "guidance_path": guidance_path,
        "completed_papers": len(results),
        "results": results,
    }

    temp_path = f"{checkpoint_path}.tmp"
    with open(temp_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    os.replace(temp_path, checkpoint_path)


def _is_complete_result(result: object) -> bool:
    """Return whether a checkpoint record is a complete, non-error appraisal."""
    if not isinstance(result, dict) or str(result.get("overall", "")).startswith("ERROR:"):
        return False

    for tree_id in TREES:
        tree_result = result.get(tree_id)
        if not isinstance(tree_result, dict) or tree_result.get("error") or tree_result.get("failed_node"):
            return False

    return True

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


def traverse_tree(tree, paper_text, start_node = "q_1_1", guidance_text = None, verbose = True, ask = None):
    node_id = start_node
    path = []
    ask_fn = ask or ask_llm

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
        response = ask_fn(
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


def analyse_all_papers(
    processed_dir: str,
    guidance_path: str = None,
    verbose: bool = True,
    checkpoint_path: str | None = None,
    resume: bool = True,
):
    """
    Reads all .txt, .md, or .json files from a directory, runs analysis on each, and returns
    a dictionary of results. For JSON files, extracts the full content as text.

    Checkpoint behavior:
    - Saves progress after each paper.
    - Can resume from an existing checkpoint file.
    """
    print(f"--- Starting Analysis on All Papers in '{processed_dir}' ---")

    if checkpoint_path is None:
        checkpoint_path = _default_checkpoint_path(processed_dir)
    
    guidance_text = None
    if guidance_path and os.path.exists(guidance_path):
        with open(guidance_path, "r", encoding="utf-8") as gf:
            guidance_text = gf.read()
        print(f"  -> Loaded CEECAT guidance from {guidance_path}")

    all_results = {}
    if resume and os.path.exists(checkpoint_path):
        try:
            all_results = _load_checkpoint(checkpoint_path)
            print(
                f"  -> Resuming from checkpoint: {checkpoint_path} "
                f"({len(all_results)} papers already completed)"
            )
        except Exception as exc:
            print(f"  - Warning: Could not load checkpoint '{checkpoint_path}': {exc}")
            print("  - Starting with a fresh run.")
            all_results = {}

    checkpoint_name = os.path.basename(checkpoint_path)
    all_files = sorted(
        f
        for f in os.listdir(processed_dir)
        if f.endswith((".txt", ".md", ".json"))
        and not f.startswith(".")
        and f != checkpoint_name
    )

    if not all_files:
        print("No processed text, markdown, or JSON files found in the specified directory.")
        return all_results

    for file_name in all_files:
        paper_name = os.path.splitext(file_name)[0]

        if resume and _is_complete_result(all_results.get(paper_name)):
            print(f"\n--- Skipping already completed: {paper_name} ---")
            continue

        print(f"\n--- Analyzing: {paper_name} ---")
        
        file_path = os.path.join(processed_dir, file_name)
        
        # Load content based on file type
        if file_name.endswith(".json"):
            with open(file_path, "r", encoding="utf-8") as f:
                json_data = json.load(f)
                # Convert JSON to formatted string
                paper_text = json.dumps(json_data, indent=2, ensure_ascii=False)
        else:
            # Handle .txt and .md files
            with open(file_path, "r", encoding="utf-8") as f:
                paper_text = f.read()

        if not paper_text.strip():
            print("  - Warning: Text file is empty, skipping.")
            all_results[paper_name] = "Skipped (empty file)"
            continue

        all_results[paper_name] = run_all_trees(paper_text, guidance_text=guidance_text, verbose=verbose)

        # Save checkpoint after each paper so long runs can be resumed safely.
        _save_checkpoint(
            checkpoint_path=checkpoint_path,
            results=all_results,
            processed_dir=processed_dir,
            guidance_path=guidance_path,
        )

    print(f"\n--- Checkpoint saved at: {checkpoint_path} ---")

    return all_results
