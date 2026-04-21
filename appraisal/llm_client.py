import requests
import os
import re
from json import JSONDecodeError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
if not API_KEY:
    raise ValueError("OPENROUTER_API_KEY is not set. Please ensure you have a .env file with this key.")

MODEL = "openai/gpt-5.2"

# Create a session object to reuse TCP connections (Keep-Alive)
_session = requests.Session()

DEFAULT_INSTRUCTIONS = (
    "Instructions for Evaluation:\n"
    "1. Evidence Extraction: First, locate and quote the exact, relevant passages from the paper.\n"
    "2. Reasoning: Explain step-by-step how the quoted evidence answers the specific question. "
    "Do not assume or guess; if the information is missing, note that it is missing.\n"
    "3. Final Judgment: Based strictly on the reasoning, select the most appropriate option.\n\n"

    "You MUST provide ALL THREE sections above.\n"
    "Do NOT omit reasoning.\n\n"

    "Definitions for ALL Valid Options (not all of the below answers will be valid for all questions. Please be aware of this):\n"
    "- 'Yes' / 'No': The paper explicitly states information confirming the answer.\n"
    "- 'Seemingly Yes' / 'Seemingly No': The paper strongly implies the answer, but does not explicitly state it.\n"
    "- 'Unclear': The paper does not provide enough details to make a judgment.\n\n"

    "You MUST conclude your response with the final selection in double brackets.\n"
    "Example format: [[Seemingly Yes]]"
)

INSTRUCTIONS = DEFAULT_INSTRUCTIONS

def set_instructions(new_instructions: str):
    """Update the instructions used in the prompt."""
    global INSTRUCTIONS
    INSTRUCTIONS = new_instructions

def ask_llm(
    prompt: str,
    context: str,
    prior_context: str | None = None,
    valid_answers: list = None,
    model: str = MODEL,
) -> dict:
    """Send prompt to OpenRouter and return both full response and extracted final answer."""
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    if valid_answers:
        options_str = ", ".join([f"'{ans}'" for ans in valid_answers])
    else:
        options_str = "the valid options defined in the system instructions"

    user_prompt_parts = []
    if prior_context:
        user_prompt_parts.append(
            "Previous appraisal context is provided for continuity. "
            "Use it only as local context, and judge the current question from the paper text."
        )
        user_prompt_parts.append(prior_context)
    user_prompt_parts.append(f"Question: {prompt}")
    user_prompt_parts.append(
        f"Important: Your final response MUST be exactly one of the following valid options: {options_str}.\n"
        "You MUST conclude your response with the final selection enclosed in double brackets, e.g., [[Yes]]."
    )
    user_prompt = "\n\n".join(user_prompt_parts)

    system_prompt = (
        "You are an expert scientific systematic reviewer specializing in the critical appraisal of academic literature for risk of bias.\n"
        "Your task is to evaluate the provided study objectively and rigorously.\n"
        "Please answer the evaluation question based STRICTLY on the text of the paper provided below. Do not use outside knowledge.\n\n"
        f"{INSTRUCTIONS}\n\n"
        f"--- PAPER TEXT ---\n{context}\n------------------"
    )
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    data = {
        "model": model,
        "messages": messages
    }
    
    try:
        response = _session.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=120,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        status_code = getattr(exc.response, "status_code", "unknown")
        body = ""
        if exc.response is not None:
            body = exc.response.text.strip()[:500]
        return {
            "full_response": None,
            "final_answer": None,
            "error": f"Request failed (status {status_code}): {exc}. Response body: {body}"
        }

    try:
        result = response.json()
    except (requests.exceptions.JSONDecodeError, JSONDecodeError):
        return {
            "full_response": response.text[:1000],
            "final_answer": None,
            "error": (
                f"Non-JSON response from API (status {response.status_code}). "
                f"Response body: {response.text[:500]}"
            )
        }

    if "error" in result:
        error_message = result["error"].get("message", str(result["error"]))
        return {
            "full_response": None,
            "final_answer": None,
            "error": error_message
        }
    
    content = result["choices"][0]["message"]["content"].strip()
    
    # Extract final answer inside [[...]]
    match = re.search(r"\[\[(.*?)\]\]", content, re.DOTALL)
    
    return {
        "full_response": content,
        "final_answer": match.group(1).strip() if match else None
    }
