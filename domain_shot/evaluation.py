import json
import os
import re

import requests
from dotenv import load_dotenv

from .build_tree_guided_prompt import (
    DEFAULT_PAPERS_DIR,
    load_default_guidance_intro,
    read_text_file,
    build_prompt_messages as build_tree_guided_prompt_messages,
    load_default_domain_prompt_parts,
)

load_dotenv()

DEFAULT_MODEL = "anthropic/claude-sonnet-5"


def _load_domain_guidance_module():
    """Import domain-guidance prompt builder lazily so other modes still work when absent."""
    try:
        from .build_domain_shot_prompt import (  # pylint: disable=import-outside-toplevel
            build_prompt_messages as build_domain_shot_prompt_messages,
            load_default_domain_guidance,
        )
    except ModuleNotFoundError as exc:
        raise ModuleNotFoundError(
            "domain_guidance mode is unavailable because 'domain_shot.build_domain_shot_prompt' is missing."
        ) from exc

    return build_domain_shot_prompt_messages, load_default_domain_guidance


def _load_default_guidance_by_mode(prompt_mode: str) -> dict:
    """Load default per-domain prompt content based on prompt mode."""
    if prompt_mode == "domain_guidance":
        _, load_default_domain_guidance = _load_domain_guidance_module()
        return load_default_domain_guidance()
    if prompt_mode == "tree_questions":
        return load_default_domain_prompt_parts()

    raise ValueError(
        f"Unsupported prompt_mode '{prompt_mode}'. Expected 'domain_guidance' or 'tree_questions'."
    )


def call_llm_and_process(domain_name: str, messages: list, model: str) -> dict:
    """Call the LLM API and process the response."""
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "Content-Type": "application/json",
    }

    data = {
        "model": model,
        "messages": messages,
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=data,
        timeout=120,
    )
    response.raise_for_status()
    content = response.json()["choices"][0]["message"]["content"].strip()

    match = re.search(r"```(?:json)?(.*?)```", content, re.DOTALL | re.IGNORECASE)
    json_str = match.group(1).strip() if match else content.strip()

    parsed_json = json.loads(json_str)

    return {"parsed_response": parsed_json}


def evaluate_domain_with_llm(
    domain_name: str,
    domain_text: str,
    paper_text: str,
    intro_text: str,
    model: str = DEFAULT_MODEL,
) -> dict:
    """Build the prompt, call the LLM, and return the processed response."""
    build_domain_shot_prompt_messages, _ = _load_domain_guidance_module()
    messages = build_domain_shot_prompt_messages(
        domain_name=domain_name,
        domain_text=domain_text,
        paper_text=paper_text,
        intro_text=intro_text,
    )
    return call_llm_and_process(domain_name, messages, model)


def evaluate_domain_with_llm_tree_questions(
    domain_name: str,
    decision_tree_text: str,
    domain_questions_text: str,
    paper_text: str,
    intro_text: str,
    model: str = DEFAULT_MODEL,
) -> dict:
    """Build a tree+questions prompt, call the LLM, and return the processed response."""
    messages = build_tree_guided_prompt_messages(
        domain_name=domain_name,
        intro_text=intro_text,
        decision_tree_text=decision_tree_text,
        domain_questions_text=domain_questions_text,
        paper_text=paper_text,
    )
    return call_llm_and_process(domain_name, messages, model)


def evaluate_single(
    paper_path: str,
    intro_text: str,
    model: str = DEFAULT_MODEL,
    guidance_dict: dict | None = None,
    prompt_mode: str = "domain_guidance",
):
    if guidance_dict is None:
        guidance_dict = _load_default_guidance_by_mode(prompt_mode)

    paper_name = os.path.basename(paper_path)
    print(f"\n--- Evaluating Paper: {paper_name} ---")
    print(f"Loaded {len(guidance_dict)} domains for evaluation using mode '{prompt_mode}'.")

    paper_text = read_text_file(paper_path)

    final_results = {}
    for domain_name, domain_payload in guidance_dict.items():
        print(f"  -> Assessing {domain_name}...")
        if prompt_mode == "domain_guidance":
            response = evaluate_domain_with_llm(
                domain_name,
                domain_payload,
                paper_text,
                intro_text,
                model,
            )
        elif prompt_mode == "tree_questions":
            if not isinstance(domain_payload, dict):
                raise ValueError(
                    "guidance_dict values must be dict payloads in tree_questions mode."
                )

            response = evaluate_domain_with_llm_tree_questions(
                domain_name=domain_name,
                decision_tree_text=domain_payload["decision_tree_text"],
                domain_questions_text=domain_payload["domain_questions_text"],
                paper_text=paper_text,
                intro_text=intro_text,
                model=model,
            )
        else:
            raise ValueError(
                f"Unsupported prompt_mode '{prompt_mode}'. Expected 'domain_guidance' or 'tree_questions'."
            )

        final_results[domain_name] = response

    return final_results


def evaluate_all(
    papers_dir: str = DEFAULT_PAPERS_DIR,
    model: str = DEFAULT_MODEL,
    guidance_dict: dict | None = None,
    intro_text: str | None = None,
    prompt_mode: str = "domain_guidance",
):
    if guidance_dict is None:
        guidance_dict = _load_default_guidance_by_mode(prompt_mode)
    if intro_text is None:
        intro_text = load_default_guidance_intro()

    print(
        f"\n--- Starting Batch Domain-Shot Evaluation on: {papers_dir} (mode={prompt_mode}) ---"
    )
    valid_extensions = (".md",)
    files = [f for f in os.listdir(papers_dir) if f.lower().endswith(valid_extensions)]

    all_results = {}
    for filename in sorted(files):
        file_path = os.path.join(papers_dir, filename)
        res = evaluate_single(
            paper_path=file_path,
            intro_text=intro_text,
            model=model,
            guidance_dict=guidance_dict,
            prompt_mode=prompt_mode,
        )
        all_results[filename] = res

    return all_results


def evaluate_single_by_filename(
    paper_filename: str,
    papers_dir: str = DEFAULT_PAPERS_DIR,
    model: str = DEFAULT_MODEL,
    prompt_mode: str = "domain_guidance",
):
    """Convenience helper for evaluating one markdown paper from the default papers directory."""
    guidance_dict = _load_default_guidance_by_mode(prompt_mode)
    intro_text = load_default_guidance_intro()
    paper_path = os.path.join(papers_dir, paper_filename)

    return evaluate_single(
        paper_path=paper_path,
        intro_text=intro_text,
        model=model,
        guidance_dict=guidance_dict,
        prompt_mode=prompt_mode,
    )