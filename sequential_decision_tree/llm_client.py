import requests
import os
import re
from json import JSONDecodeError
from dotenv import load_dotenv
import datetime

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
if not API_KEY:
    raise ValueError("OPENROUTER_API_KEY is not set. Please ensure you have a .env file with this key.")

MODEL = "openai/gpt-4.1-nano"

# Create a session object to reuse TCP connections (Keep-Alive)
_session = requests.Session()

DEFAULT_INSTRUCTIONS = (
    "Instructions for Evaluation:\n"
    "1. Evidence Extraction: First, locate and quote the exact, relevant passages from the paper.\n"
    "2. Reasoning: Explain step-by-step how the quoted evidence answers the specific question.\n"
    "Use expert scientific judgment. If a standard methodological practice is strongly implied by the context, you should acknowledge it rather than strictly penalizing the paper for exact phrasing.\n"
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


def _normalize_to_valid_answer(candidate: str, valid_answers: list | None) -> str | None:
    """Normalize a parsed candidate to one of the valid answers when possible."""
    cleaned = candidate.strip().strip("[](){}<> ").strip(".:;,*_`\"")
    if not cleaned:
        return None

    if not valid_answers:
        return cleaned

    valid_map = {ans.lower(): ans for ans in valid_answers}
    normalized = cleaned.lower()
    return valid_map.get(normalized)


def _extract_final_answer(content: str, valid_answers: list | None = None) -> str | None:
    """Extract final answer from LLM output with bracket-first, answer-line fallback."""
    # Preferred format: [[Answer]]
    match = re.search(r"\[\[(.*?)\]\]", content, re.DOTALL)
    if match:
        parsed = _normalize_to_valid_answer(match.group(1), valid_answers)
        if parsed:
            return parsed

    # Fallback format: "Answer: X" (including markdown bold variants)
    answer_line_matches = list(
        re.finditer(r"(?im)^\s*(?:\*\*)?answer(?:\*\*)?\s*:\s*(.+?)\s*$", content)
    )
    for m in reversed(answer_line_matches):
        parsed = _normalize_to_valid_answer(m.group(1), valid_answers)
        if parsed:
            return parsed

    # Last-line fallback for outputs that end with just the label.
    if valid_answers:
        valid_map = {ans.lower(): ans for ans in valid_answers}
        lines = [line.strip().strip("*_`") for line in content.splitlines() if line.strip()]
        for line in reversed(lines):
            normalized = line.strip(".:;,*_`\"").lower()
            if normalized in valid_map:
                return valid_map[normalized]

    return None

def set_instructions(new_instructions: str):
    """Update the instructions used in the prompt."""
    global INSTRUCTIONS
    INSTRUCTIONS = new_instructions

def ask_llm(
    prompt: str,
    context: str,
    prior_context: str | None = None,
    guidance_text: str | None = None,
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

    system_prompt_parts = [
        "You are an expert scientific systematic reviewer specializing in the critical appraisal of academic literature for risk of bias.",
        "Your task is to evaluate the provided study objectively and rigorously.",
        "Please answer the evaluation question based STRICTLY on the text of the paper provided below. Do not use outside knowledge.\n",
        INSTRUCTIONS
    ]
    
    if guidance_text:
        system_prompt_parts.append("\n--- CEECAT GUIDANCE ---")
        system_prompt_parts.append(guidance_text)
        system_prompt_parts.append("Use the above guidance as helpful background information to better understand the context of the biases being evaluated. It provides general information rather than strict rules.\n-----------------------\n")
        
    system_prompt_parts.append(f"--- PAPER TEXT ---\n{context}\n------------------")
    system_prompt = "\n".join(system_prompt_parts)

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
    
    # Extract final answer (preferred [[...]] format, with one-call fallback parsing)
    final_answer = _extract_final_answer(content, valid_answers=valid_answers)
    
    qa_log_file = os.getenv("QA_LOG_FILE")
    if qa_log_file:
        try:
            os.makedirs(os.path.dirname(os.path.abspath(qa_log_file)), exist_ok=True)
            with open(qa_log_file, "a", encoding="utf-8") as f:
                timestamp = datetime.datetime.now().isoformat()
                f.write(f"\n[{timestamp}] Model: {model}\n")
                f.write("=== SYSTEM PROMPT ===\n" + system_prompt + "\n")
                f.write("=== USER PROMPT ===\n" + user_prompt + "\n")
                f.write("=== RAW RESPONSE ===\n" + content + "\n")
                f.write("=== PARSED OUTPUT ===\n" + str(final_answer) + "\n")
                f.write("-" * 50 + "\n")
        except Exception as e:
            print(f"Warning: Failed to write QA log to {qa_log_file}: {e}")
    
    return {
        "full_response": content,
        "final_answer": final_answer
    }
