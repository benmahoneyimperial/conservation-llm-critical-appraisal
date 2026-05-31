import os
import glob
import json
import re
import requests
import datetime
from dotenv import load_dotenv

load_dotenv()

def load_domain_guidance(guidance_dir: str) -> dict:
    """
    Reads all domain guidance markdown files from the specified directory.
    
    Args:
        guidance_dir (str): Path to the directory containing domain guidance files.
        
    Returns:
        dict: A dictionary where keys are the domain names (derived from filenames)
              and values are the markdown text of the guidance.
    """
    domain_guidance = {}
    
    if not os.path.exists(guidance_dir):
        raise FileNotFoundError(f"Guidance directory not found: {guidance_dir}")
                
    files = glob.glob(os.path.join(guidance_dir, "*.md"))
    
        
    for file_path in files:
        filename = os.path.basename(file_path)
        domain_name = os.path.splitext(filename)[0]  # e.g., 'domain_1'
        
        with open(file_path, "r", encoding="utf-8") as f:
            domain_guidance[domain_name] = f.read()
            
    return dict(sorted(domain_guidance.items()))


def evaluate_domain_with_llm(domain_name: str, domain_text: str, paper_text: str, intro_text: str, model: str = "meta-llama/llama-3.3-70b-instruct") -> dict:
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "Content-Type": "application/json"
    }

    system_prompt = f"""
    You are an expert human systematic reviewer performing structured risk-of-bias assessment for the domain: {domain_name}.

    You must follow the domain guidance strictly and base all judgments ONLY on evidence explicitly found in the provided paper.

    You are NOT allowed to use external knowledge or assumptions.

    ---

    ## TASK OVERVIEW

    Your job is to:
    1. Carefully read the provided domain guidance and checklist.
    2. Analyze the provided research paper for relevant information.
    3. Extract relevant evidence from the paper.
    4. Map the evidence to the checklist questions and answer options.
    5. Follow the provided decision tree logic to determine the final risk of bias for this domain.
    ---

    ## CRITICAL RULES

    - Only use information explicitly stated in the paper.
    - Follow conditional logic exactly as written in the checklist.
    - Do NOT skip steps.
    - Do NOT provide narrative summaries outside the required JSON.

    ---

    ## OUTPUT FORMAT (STRICT JSON ONLY)

    Return ONLY a valid JSON object with these keys:

    {{
    "evidence": [
        "verbatim excerpt 1",
        "verbatim excerpt 2"
    ],
    "checklist_answers": {{
        "<Question ID>": "Yes/Seemingly yes/Seemingly no/No/Unclear",
        "<Next Question ID>": "..."
    }},
    "mapping_reasoning": [
        "Brief explanation of how evidence maps to each answer (no long reasoning)"
    ],
    "decision_path": [
        "<Question ID> → <Answer>",
        "<Next Question ID> → <Answer>",
        "<Final Risk>"
    ]
    }}

    ---

    ## IMPORTANT
    - The decision_path must explicitly reflect the tree traversal.
    """

    user_prompt = f"\n{intro_text}\n\n--- GUIDANCE FOR {domain_name} ---\n{domain_text}\n\n--- RESEARCH PAPER ---\n{paper_text}\n\nPlease evaluate the paper for {domain_name} and return the JSON."

    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
    response.raise_for_status()
    content = response.json()["choices"][0]["message"]["content"].strip()
    
    match = re.search(r'```(?:json)?(.*?)```', content, re.DOTALL | re.IGNORECASE)
    json_str = match.group(1).strip() if match else content.strip()
    
    qa_log_file = os.getenv("QA_LOG_FILE")
    if qa_log_file:
        os.makedirs(os.path.dirname(os.path.abspath(qa_log_file)), exist_ok=True)
        with open(qa_log_file, "a", encoding="utf-8") as f:
            f.write(f"\n[{datetime.datetime.now().isoformat()}] Model: {model} | Domain: {domain_name}\n")
            f.write(f"Response: {content}\n{'-' * 50}\n")
            
    try:
        return {"parsed_response": json.loads(json_str)}
    except json.JSONDecodeError:
        return {"error": "Invalid JSON returned", "full_response": content}

def calculate_overall_risk(domain_results: dict) -> str:
    high_count = sum(1 for d in domain_results.values() if "high" in d.get("parsed_response", {}).get("risk", "").lower())
    medium_count = sum(1 for d in domain_results.values() if "medium" in d.get("parsed_response", {}).get("risk", "").lower())
    
    if high_count > 0:
        return "High Risk"
    elif medium_count >= 2:
        return "Medium Risk"
    elif medium_count == 1:
        return "Low Risk (with 1 Medium)"
    return "Low Risk"

def evaluate_single(guidance_dict: dict, paper_path: str, intro_text: str, model: str = "meta-llama/llama-3.3-70b-instruct"):
    paper_name = os.path.basename(paper_path)
    print(f"\n--- Evaluating Paper: {paper_name} ---")
    print(f"Loaded {len(guidance_dict)} domains for evaluation.")
    
    with open(paper_path, "r", encoding="utf-8") as f:
        paper_text = f.read()

    final_results = {}
    for domain_name, domain_text in guidance_dict.items():
        print(f"  -> Assessing {domain_name}...")
        response = evaluate_domain_with_llm(domain_name, domain_text, paper_text, intro_text, model)
        final_results[domain_name] = response
        
    overall_risk = calculate_overall_risk(final_results)
    final_results["overall_risk"] = overall_risk
    
    print(f"\nFinal Result for {paper_name}")
    print(f"Overall Risk: {overall_risk}")
    return final_results


def evaluate_all(guidance_dict: dict, papers_dir: str, intro_text: str, model: str = "meta-llama/llama-3.3-70b-instruct"):
    print(f"\n--- Starting Batch Domain-Shot Evaluation on: {papers_dir} ---")
    valid_extensions = (".md", ".txt")
    files = [f for f in os.listdir(papers_dir) if f.lower().endswith(valid_extensions)]
    
    all_results = {}
    for filename in sorted(files):
        file_path = os.path.join(papers_dir, filename)
        res = evaluate_single(guidance_dict, file_path, intro_text, model)
        all_results[filename] = res
        
    return all_results