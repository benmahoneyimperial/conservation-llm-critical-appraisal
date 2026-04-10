import os
import sys
import argparse
import requests
import json
import re
import csv
from dotenv import load_dotenv

# Add the project root to the python path to import project modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from paper_processing.pdf_processor import extract_text_from_pdf

load_dotenv()

def evaluate_with_llm(guidance_text: str, paper_text: str) -> dict:
    """
    Sends the combined guidance and paper to the LLM via OpenRouter.
    """
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        return {"error": "OPENROUTER_API_KEY is not set. Please ensure you have a .env file with this key."}

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    system_prompt = (
        """You are an expert systematic reviewer performing structured risk-of-bias assessment.

        You MUST follow this exact process:

        1. Identify all bias domains defined in the guidance document.
        2. For EACH domain:
        a. Locate and quote the exact relevant evidence from the paper.
        b. Compare the evidence directly to the criteria in the guidance.
        c. Assign a risk judgment strictly based on the guidance definitions.

        Output rules: Your final output should primarily be a JSON object.
        - The JSON must be valid and contain the final judgments.
        - Use keys: domain_1, domain_2, ..., overall.
        - Values must be one of: "Low Risk", "Medium Risk", "High Risk", "Unclear".
        - You may include brief explanations or reasoning *before* or *after* the JSON block.
        
        You may reason step-by-step internally, but you must NOT output your reasoning."""
        )

    user_prompt = f"""You will evaluate a research paper using the provided guidance document.
--- GUIDANCE DOCUMENT ---
{guidance_text}

--- RESEARCH PAPER TO EVALUATE ---
{paper_text}

TASK:
Using ONLY the guidance document:

1. Identify each bias domain defined in the guidance.
2. For each domain:
- Apply the criteria strictly
- Base your judgment ONLY on explicit evidence in the paper

3. Then determine an overall risk of bias:
- If ANY domain is High Risk → overall = High Risk
- If multiple domains are Medium Risk → overall = Medium Risk
- Otherwise → Low Risk

OUTPUT FORMAT (Please provide your final judgments in JSON, optionally wrapped in a markdown code block):

{{
"domain_1": "...",
"domain_2": "...",
"domain_3": "...",
"domain_4": "...",
"domain_5": "...",
"domain_6": "...",
"domain_7": "...",
"overall": "..."
}}"""

    data = {
        "model": "meta-llama/llama-3.3-70b-instruct",  # Change this to your preferred model
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
        
        # Extract JSON block if surrounded by markdown backticks
        match = re.search(r'```(?:json)?(.*?)```', content, re.DOTALL | re.IGNORECASE)
        json_str = match.group(1).strip() if match else content.strip()
        
        try:
            parsed_json = json.loads(json_str)
            return {"parsed_response": parsed_json, "full_response": content}
        except json.JSONDecodeError:
            return {"error": "LLM did not return valid JSON.", "full_response": content}
            
    except Exception as e:
        return {"error": str(e)}

def print_results_table(results_dict: dict):
    """
    Prints a formatted table of the evaluation results.
    """
    # Find all unique keys across all successful results
    all_keys = set()
    for res in results_dict.values():
        if isinstance(res, dict) and "error" not in res:
            all_keys.update(res.keys())
            
    # Filter and sort domain keys
    domain_keys = sorted([k for k in all_keys if k.lower().startswith("domain")])
    if not domain_keys:
        domain_keys = [f"domain_{i}" for i in range(1, 8)]
        
    overall_key = next((k for k in all_keys if k.lower() == "overall"), "overall")
    
    # Determine column widths
    col_width_paper = max(20, max([len(p) for p in results_dict.keys()] + [10]))
    col_width_domain = 14
    
    header_format = f"{{:<{col_width_paper}}} | " + " | ".join([f"{{:<{col_width_domain}}}"] * len(domain_keys)) + f" | {{:<{col_width_domain}}}"
    
    sep_line = "-" * (col_width_paper + 3 + (col_width_domain+3)*(len(domain_keys)+1))
    
    print("\n" + "=" * len(sep_line))
    print("=== EVALUATION RESULTS ===")
    print("=" * len(sep_line))
    
    headers = ["Paper Name"] + [k.replace('_', ' ').title() for k in domain_keys] + ["Overall"]
    print(header_format.format(*headers))
    print(sep_line)
    
    for paper, result in results_dict.items():
        if isinstance(result, dict) and "error" not in result:
            row = [paper]
            for k in domain_keys:
                row.append(str(result.get(k, "N/A"))[:col_width_domain])
            row.append(str(result.get(overall_key, "N/A"))[:col_width_domain])
            print(header_format.format(*row))
        else:
            err_msg = str(result.get("error", result)) if isinstance(result, dict) else str(result)
            row = [paper] + ["Error"] * len(domain_keys) + [err_msg[:col_width_domain]]
            print(header_format.format(*row))
    print("=" * len(sep_line) + "\n")

def save_results_csv(results_dict: dict, csv_path: str):
    """
    Saves the evaluation results to a CSV file.
    """
    # Find all unique keys across all successful results
    all_keys = set()
    for res in results_dict.values():
        if isinstance(res, dict) and "error" not in res:
            all_keys.update(res.keys())
            
    # Filter and sort domain keys
    domain_keys = sorted([k for k in all_keys if k.lower().startswith("domain")])
    if not domain_keys:
        domain_keys = [f"domain_{i}" for i in range(1, 8)]
        
    overall_key = next((k for k in all_keys if k.lower() == "overall"), "overall")
    
    headers = ["Paper Name"] + [k.replace('_', ' ').title() for k in domain_keys] + ["Overall"]
    
    try:
        with open(csv_path, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            
            for paper, result in results_dict.items():
                if isinstance(result, dict) and "error" not in result:
                    row = [paper]
                    for k in domain_keys:
                        row.append(str(result.get(k, "N/A")))
                    row.append(str(result.get(overall_key, "N/A")))
                    writer.writerow(row)
                else:
                    err_msg = str(result.get("error", result)) if isinstance(result, dict) else str(result)
                    row = [paper] + ["Error"] * len(domain_keys) + [err_msg]
                    writer.writerow(row)
        print(f"\nResults successfully saved to '{csv_path}'")
    except Exception as e:
        print(f"\nError saving to CSV: {e}")

def simple_evaluate(guidance_pdf_path: str, paper_pdf_path: str, output_csv: str = None):
    """
    Performs a simple evaluation of a paper against a guidance document.
    """
    # 1. Validate file paths
    if not os.path.exists(guidance_pdf_path):
        print(f"Error: Guidance PDF not found at '{guidance_pdf_path}'")
        return
    if not os.path.exists(paper_pdf_path):
        print(f"Error: Paper PDF not found at '{paper_pdf_path}'")
        return

    print("--- Starting Single-Shot Evaluation ---")
    
    # 2. Extract text from both PDFs
    print(f"Reading guidance document: {os.path.basename(guidance_pdf_path)}...")
    try:
        guidance_text = extract_text_from_pdf(guidance_pdf_path)
    except Exception as e:
        print(f"Error reading guidance PDF: {e}")
        return

    print(f"Reading paper: {os.path.basename(paper_pdf_path)}...")
    try:
        paper_text = extract_text_from_pdf(paper_pdf_path)
    except Exception as e:
        print(f"Error reading paper PDF: {e}")
        return

    # 3. Call the LLM directly
    print("\nSending request to LLM... (This may take a moment)")
    response = evaluate_with_llm(guidance_text, paper_text)

    # 4. Print the results
    paper_name = os.path.basename(paper_pdf_path)
    
    if response.get("error"):
        print(f"\nAn error occurred: {response['error']}")
        if "full_response" in response:
            print("\nFull Response:\n", response["full_response"])
        results_dict = {paper_name: {"error": response["error"]}}
    elif response.get("parsed_response"):
        results_dict = {paper_name: response["parsed_response"]}
        print_results_table(results_dict)
    else:
        print("\nNo response was received from the LLM.")
        results_dict = {paper_name: {"error": "No response"}}

    if output_csv:
        save_results_csv(results_dict, output_csv)

def evaluate_all(guidance_pdf_path: str, papers_dir: str, output_csv: str = None):
    """
    Evaluates all PDF papers in a directory against a guidance document.
    """
    if not os.path.exists(guidance_pdf_path):
        print(f"Error: Guidance PDF not found at '{guidance_pdf_path}'")
        return
    if not os.path.isdir(papers_dir):
        print(f"Error: Papers directory not found at '{papers_dir}'")
        return

    print(f"--- Starting Batch Evaluation on directory: {papers_dir} ---")
    
    print(f"Reading guidance document: {os.path.basename(guidance_pdf_path)}...")
    try:
        guidance_text = extract_text_from_pdf(guidance_pdf_path)
    except Exception as e:
        print(f"Error reading guidance PDF: {e}")
        return

    pdf_files = [f for f in os.listdir(papers_dir) if f.lower().endswith('.pdf')]
    if not pdf_files:
        print(f"No PDF files found in '{papers_dir}'.")
        return

    results = {}
    for pdf_file in pdf_files:
        paper_pdf_path = os.path.join(papers_dir, pdf_file)
        print(f"\nEvaluating paper: {pdf_file}...")
        
        try:
            paper_text = extract_text_from_pdf(paper_pdf_path)
        except Exception as e:
            print(f"  Error reading paper PDF: {e}")
            results[pdf_file] = f"Error: {e}"
            continue

        print("  Sending request to LLM...")
        response = evaluate_with_llm(guidance_text, paper_text)
        
        if response.get("error"):
            print(f"  An error occurred: {response['error']}")
            results[pdf_file] = {"error": response['error']}
        elif response.get("parsed_response"):
            print(f"  Evaluation complete.")
            results[pdf_file] = response["parsed_response"]
        else:
            print("  No response was received from the LLM.")
            results[pdf_file] = {"error": "No response"}

    print_results_table(results)

    if output_csv:
        save_results_csv(results, output_csv)
        
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Evaluate a paper (or a directory of papers) for bias against a guidance document in a single prompt."
    )
    parser.add_argument("guidance_pdf", type=str, help="The path to the guidance PDF file.")
    parser.add_argument("target", type=str, help="The path to a single research paper PDF file OR a directory of PDF files.")
    parser.add_argument("--output_csv", type=str, default=None, help="Optional path to save the results as a CSV file.")
    args = parser.parse_args()
    
    if os.path.isdir(args.target):
        evaluate_all(args.guidance_pdf, args.target, args.output_csv)
    else:
        simple_evaluate(args.guidance_pdf, args.target, args.output_csv)