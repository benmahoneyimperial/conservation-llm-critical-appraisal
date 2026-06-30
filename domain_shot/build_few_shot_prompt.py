import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DEFAULT_GUIDANCE_INTRO_PATH = os.path.join(PROJECT_ROOT, "data", "guidance_intro_md", "guidance_intro.md")
DEFAULT_DOMAIN_QUESTIONS_DIR = os.path.join(PROJECT_ROOT, "data", "domain_questions_md")
DEFAULT_EXAMPLES_DIR = os.path.join(PROJECT_ROOT, "data", "examples")
DEFAULT_PAPERS_DIR = os.path.join(PROJECT_ROOT, "data", "sample_papers", "sample_papers_md")

SYSTEM_PROMPT_INSTRUCTIONS = """You are an expert human systematic reviewer performing structured risk-of-bias assessment using example-guided appraisal.

You must follow the guidance strictly and base all judgments only on evidence explicitly found in the target paper.
You are not allowed to use external knowledge or assumptions.
Use worked examples only as calibration references, not as evidence for the target paper.

Return valid JSON only with this structure:
{
    "question_answers": {
        "<question_id_or_question_text>": "Yes/Seemingly yes/Seemingly no/No/Unclear"
    },
    "final_risk_judgement": "Low Risk/Medium Risk/High Risk/Unclear/Not Applicable",
    "short_rationale": "1-3 sentences grounded in target paper evidence"
}
"""


def read_text_file(path: str) -> str:
    """Load text content from a file path."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")

    with open(path, "r", encoding="utf-8") as handle:
        return handle.read()


def load_default_guidance_intro() -> str:
    """Load the shared guidance intro from the default project file."""
    return read_text_file(DEFAULT_GUIDANCE_INTRO_PATH)


def _resolve_domain_markdown_path(
    domain_name: str,
    base_dir: str,
    preferred_suffix: str,
    file_label: str,
) -> str:
    """Resolve a required domain markdown path or raise FileNotFoundError."""
    candidates = [
        os.path.join(base_dir, f"{domain_name}{preferred_suffix}.md"),
        os.path.join(base_dir, f"{domain_name}.md"),
    ]

    for path in candidates:
        if os.path.exists(path):
            return path

    raise FileNotFoundError(
        f"Missing {file_label} for domain '{domain_name}'. Expected one of: {', '.join(candidates)}"
    )


def load_domain_questions(domain_name: str, questions_dir: str = DEFAULT_DOMAIN_QUESTIONS_DIR) -> str:
    """Load domain questions markdown for one domain."""
    path = _resolve_domain_markdown_path(
        domain_name=domain_name,
        base_dir=questions_dir,
        preferred_suffix="_questions",
        file_label="domain questions file",
    )
    return read_text_file(path)


def load_domain_examples(domain_name: str, examples_dir: str = DEFAULT_EXAMPLES_DIR) -> str:
    """Load worked examples markdown for one domain."""
    path = _resolve_domain_markdown_path(
        domain_name=domain_name,
        base_dir=examples_dir,
        preferred_suffix="_examples",
        file_label="worked examples file",
    )
    return read_text_file(path)


def build_prompt(
    domain_name: str,
    intro_text: str,
    domain_questions_text: str,
    worked_examples_text: str,
    paper_text: str,
) -> str:
    """Join the few-shot prompt parts into a single prompt string in the intended order."""
    guidance_intro = intro_text or ""
    domain_questions = domain_questions_text or ""
    worked_examples = worked_examples_text or ""
    paper = paper_text or ""

    sections = [
        f"--- GUIDANCE INTRO ---\n{guidance_intro}",
        f"--- DOMAIN QUESTIONS ({domain_name}) ---\n{domain_questions}",
        f"--- WORKED EXAMPLES ({domain_name}) ---\n{worked_examples}",
        (
            "--- TARGET PAPER ---\n"
            f"{paper}\n\n"
            "Using the same style as the worked examples, answer all domain questions and "
            "provide a final domain risk judgement in the required JSON format."
        ),
    ]

    return "\n\n".join(sections)


def build_prompt_messages(
    domain_name: str,
    intro_text: str,
    domain_questions_text: str,
    worked_examples_text: str,
    paper_text: str,
) -> list:
    """Build the system and user message content for the LLM."""
    prompt_text = build_prompt(
        domain_name=domain_name,
        intro_text=intro_text,
        domain_questions_text=domain_questions_text,
        worked_examples_text=worked_examples_text,
        paper_text=paper_text,
    )

    return [
        {
            "role": "system",
            "content": SYSTEM_PROMPT_INSTRUCTIONS,
        },
        {"role": "user", "content": prompt_text},
    ]
