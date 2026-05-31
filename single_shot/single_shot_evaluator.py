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
        
    # Look for .md files first, fallback to .txt if necessary
    files = glob.glob(os.path.join(guidance_dir, "*.md"))
    if not files:
        files = glob.glob(os.path.join(guidance_dir, "*.txt"))
        
    for file_path in files:
        filename = os.path.basename(file_path)
        domain_name = os.path.splitext(filename)[0]  # e.g., 'domain_1'
        
        with open(file_path, "r", encoding="utf-8") as f:
            domain_guidance[domain_name] = f.read()
            
    # Sort the dictionary by keys so they process in order (domain_1, domain_2, etc.)
    return dict(sorted(domain_guidance.items()))


def evaluate_domain_with_llm(domain_name: str, domain_text: str, paper_text: str) -> dict:
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        return {"error": "OPENROUTER_API_KEY is not set. Please ensure you have a .env file with this key."}

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    system_prompt = (
        f"You are an expert systematic reviewer performing structured risk-of-bias assessment for a specific domain: {domain_name}.\n\n"
        "You MUST follow this exact process:\n"
        "1. Read the provided research paper.\n"
        "2. Read the appraisal guidance for this specific domain.\n"
        "3. Locate and extract exact quotes from the paper as evidence.\n"
        "4. Provide step-by-step reasoning based on the evidence.\n"
        "5. Assign a final risk judgment strictly based on the guidance definitions.\n\n"
        "Output rules: Your final output MUST be a valid JSON object. Do not output anything outside of the JSON block.\n"
        "The JSON must have the following keys:\n"
        '  "evidence": "Exact quotes from the paper",\n'
        '  "reasoning": "Your step-by-step reasoning",\n'
        '  "risk": "The final judgment (e.g., Low Risk, Medium Risk, High Risk, or Unclear)"\n'
    )

    user_prompt = f"--- GUIDANCE FOR {domain_name} ---\n{domain_text}\n\n--- RESEARCH PAPER ---\n{paper_text}\n\nPlease evaluate the paper for {domain_name} and return the JSON."

    data = {
        "model": "meta-llama/llama-3.3-70b-instruct",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        if "error" in result:
            return {"error": result["error"]["message"]}
            
        content = result["choices"][0]["message"]["content"].strip()
        
        # Extract JSON block
        match = re.search(r'```(?:json)?(.*?)```', content, re.DOTALL | re.IGNORECASE)
        json_str = match.group(1).strip() if match else content.strip()
        
        parsed_json = None
        error_msg = None
        try:
            parsed_json = json.loads(json_str)
        except json.JSONDecodeError:
            error_msg = "LLM did not return valid JSON."
            
        qa_log_file = os.getenv("QA_LOG_FILE")
        if qa_log_file:
            try:
                os.makedirs(os.path.dirname(os.path.abspath(qa_log_file)), exist_ok=True)
                with open(qa_log_file, "a", encoding="utf-8") as f:
                    timestamp = datetime.datetime.now().isoformat()
                    f.write(f"\n[{timestamp}] Model: meta-llama/llama-3.3-70b-instruct | Domain: {domain_name}\n")
                    f.write("=== SYSTEM PROMPT ===\n" + system_prompt + "\n")
                    f.write("=== USER PROMPT ===\n" + user_prompt + "\n")
                    f.write("=== RAW RESPONSE ===\n" + content + "\n")
                    f.write("=== PARSED OUTPUT ===\n" + str(parsed_json if parsed_json else error_msg) + "\n")
                    f.write("-" * 50 + "\n")
            except Exception as e:
                print(f"Warning: Failed to write QA log to {qa_log_file}: {e}")
                
        if error_msg:
            return {"error": error_msg, "full_response": content}
        return {"parsed_response": parsed_json}
        
    except Exception as e:
        return {"error": str(e)}

def calculate_overall_risk(domain_results: dict) -> str:
    """
    Calculate overall risk deterministically based on CEECAT logic.
    """
    high_count = 0
    medium_count = 0
    
    for domain, data in domain_results.items():
        if "error" in data:
            continue
        # Safely extract risk value
        risk = data.get("parsed_response", {}).get("risk", "").lower() if data.get("parsed_response") else ""
        if "high" in risk:
            high_count += 1
        elif "medium" in risk or "moderate" in risk:
            medium_count += 1
            
    if high_count > 0:
        return "High Risk"
    elif medium_count >= 2:
        return "Medium Risk"
    elif medium_count == 1:
        return "Low Risk (with 1 Medium)"
    else:
        return "Low Risk"

def evaluate_single(guidance_dict: dict, paper_path: str):
    """
    Evaluates a single paper across all loaded domains.
    """
    paper_name = os.path.basename(paper_path)
    print(f"\n--- Evaluating Paper: {paper_name} ---")
    print(f"Loaded {len(guidance_dict)} domains for evaluation.")
    
    try:
        with open(paper_path, "r", encoding="utf-8") as f:
            paper_text = f.read()
    except Exception as e:
        print(f"Error reading {paper_path}: {e}")
        return None

    final_results = {}
    for domain_name, domain_text in guidance_dict.items():
        print(f"  -> Assessing {domain_name}...")
        response = evaluate_domain_with_llm(domain_name, domain_text, paper_text)
        final_results[domain_name] = response
        
    overall_risk = calculate_overall_risk(final_results)
    final_results["overall_risk"] = overall_risk
    
    print(f"\nFinal Result for {paper_name}")
    print(f"Overall Risk: {overall_risk}")
    return final_results


def evaluate_all(guidance_dict: dict, papers_dir: str):
    """
    Batch evaluates all papers in a directory.
    """
    print(f"\n--- Starting Batch Domain-Shot Evaluation on: {papers_dir} ---")
    valid_extensions = (".md", ".txt")
    files = [f for f in os.listdir(papers_dir) if f.lower().endswith(valid_extensions)]
    
    if not files:
        print(f"No valid text/markdown files found in '{papers_dir}'.")
        return {}

    all_results = {}
    for filename in sorted(files):
        file_path = os.path.join(papers_dir, filename)
        res = evaluate_single(guidance_dict, file_path)
        all_results[filename] = res
        
    return all_results