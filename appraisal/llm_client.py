import requests
import os
import re
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
if not API_KEY:
    raise ValueError("OPENROUTER_API_KEY is not set. Please ensure you have a .env file with this key.")
MODEL = "openai/gpt-5.4"

# Create a session object to reuse TCP connections (Keep-Alive)
_session = requests.Session()

DEFAULT_INSTRUCTIONS = (
    "Instructions for Evaluation:\n"
    "1. Evidence Extraction: First, locate and quote the exact, relevant passages from the paper.\n"
    "2. Reasoning: Explain step-by-step how the quoted evidence answers the specific question. Do not assume or guess; if the information is missing, note that it is missing.\n"
    "3. Final Judgment: Based strictly on the reasoning, select the most appropriate option.\n\n"
    "Definitions for Valid Options:\n"
    "- 'Yes' / 'No': The paper explicitly states information confirming the answer.\n"
    "- 'Seemingly Yes' / 'Seemingly No': The paper strongly implies the answer, but does not explicitly state it.\n"
    "- 'Unclear': The paper does not provide enough details to make a judgment.\n"
    "- 'Not Applicable': The question fundamentally does not apply to this study.\n\n"
    "You MUST conclude your response by enclosing ONLY your final selection in double brackets.\n"
    "Example format: [[Seemingly Yes]]"
)

_CONFIG = {"instructions": DEFAULT_INSTRUCTIONS}

def set_instructions(new_instructions: str):
    """Update the instructions used in the prompt."""
    _CONFIG["instructions"] = new_instructions

def ask_llm(prompt: str, context: str, model: str = MODEL) -> str:
    """Send prompt to OpenRouter and return the response."""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    full_prompt = (
        f"{prompt}\n\n" + _CONFIG["instructions"]
    )
    
    system_prompt = (
        "You are an expert scientific systematic reviewer specializing in the critical appraisal of academic literature for risk of bias.\n"
        "Your task is to evaluate the provided study objectively and rigorously.\n"
        "Please answer the evaluation question based STRICTLY on the text of the paper provided below. Do not use outside knowledge.\n\n"
        f"--- PAPER TEXT ---\n{context}\n------------------"
    )
    
    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": full_prompt}
        ]
    }
    
    response = _session.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=data
    )
    
    result = response.json()
    
    if "error" in result:
        return f"Error: {result['error']['message']}"
    else:
        content = result["choices"][0]["message"]["content"].strip()
        # Use regex to find the answer inside brackets [[Answer]]
        match = re.search(r"\[\[(.*?)\]\]", content)
        if match:
            return match.group(1).strip()
        else:
            return content