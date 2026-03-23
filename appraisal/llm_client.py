import requests
import os
import re
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
if not API_KEY:
    raise ValueError("OPENROUTER_API_KEY is not set. Please ensure you have a .env file with this key.")
MODEL = "meta-llama/llama-3.3-70b-instruct:free"

# Create a session object to reuse TCP connections (Keep-Alive)
_session = requests.Session()

DEFAULT_INSTRUCTIONS = (
    "Instructions:\n"
    "1. Think step-by-step based strictly on the paper text provided.\n"
    "2. Conclude your answer by enclosing the final selection in double brackets, e.g., [[Yes]] or [[Seemingly No]].\n"
    "3. Valid options are: 'Yes', 'Seemingly Yes', 'Unclear', 'Seemingly No', 'No', 'Not Applicable'."
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
    
    system_prompt = f"You are a critical appraisal assistant. Please answer the following question based strictly on the text of the paper provided below.\n\n--- PAPER TEXT ---\n{context}\n------------------"
    
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