import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DEFAULT_GUIDANCE_INTRO_PATH = os.path.join(PROJECT_ROOT, "data", "guidance_intro_md", "guidance_intro.md")
DEFAULT_DOMAIN_QUESTIONS_DIR = os.path.join(PROJECT_ROOT, "data", "domain_questions_md")
DEFAULT_PAPERS_DIR = os.path.join(PROJECT_ROOT, "data", "sample_papers", "sample_papers_md")

SYSTEM_PROMPT_INSTRUCTIONS = """You are an expert human systematic reviewer performing structured risk-of-bias assessment.

You must follow the guidance strictly and base all judgments only on evidence explicitly found in the target paper.
You are not allowed to use external knowledge or assumptions.
Answer all domain questions and provide a numeric risk score from 0 to 10.

Return valid JSON only with this structure:
{
    "question_answers": {
        "<question_id_or_question_text>": "Yes/Seemingly yes/Seemingly no/No/Unclear/Not applicable"
    },
    "risk_of_bias_score_0_to_10": 0,
    "short_rationale": "1-3 sentences grounded in target paper evidence"
}

Score scale (integer 0-10 only):
0 = no identifiable risk of bias.
1-2 = very low risk (minor concerns only).
3-4 = low risk (some concerns, unlikely to change conclusions).
5-6 = moderate risk (meaningful concerns that may affect conclusions).
7-8 = high risk (serious concerns likely affecting conclusions).
9-10 = extreme risk (major validity concerns; conclusions highly unreliable).

Scoring rules:
Use the full 0-10 range.
More severe adverse answers (No, Seemingly no, Unclear) must not produce a lower score.
Base the score only on evidence in the target paper and keep it consistent with the question-level answers.
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


def build_prompt(
    domain_name: str,
    intro_text: str,
    domain_questions_text: str,
    paper_text: str,
) -> str:
    """Join prompt parts into a single prompt string in the intended order."""
    guidance_intro = intro_text or ""
    domain_questions = domain_questions_text or ""
    paper = paper_text or ""

    sections = [
        f"--- GUIDANCE INTRO ---\n{guidance_intro}",
        f"--- DOMAIN QUESTIONS ({domain_name}) ---\n{domain_questions}",
        (
            "--- TARGET PAPER ---\n"
            f"{paper}\n\n"
            "How to use these sections:\n"
            "1. Use GUIDANCE INTRO as helpful background context for interpreting bias concepts.\n"
            "2. Read the TARGET PAPER and answer all DOMAIN QUESTIONS first (exactly once each, using allowed labels only).\n"
            "3. Then assign risk_of_bias_score_0_to_10 using those question-level answers, with higher concern answers leading to higher scores.\n"
            "4. Return JSON only, following the required schema from the system message."
        ),
    ]

    return "\n\n".join(sections)


def build_prompt_messages(
    domain_name: str,
    intro_text: str,
    domain_questions_text: str,
    paper_text: str,
) -> list:
    """Build the system and user message content for the LLM."""
    prompt_text = build_prompt(
        domain_name=domain_name,
        intro_text=intro_text,
        domain_questions_text=domain_questions_text,
        paper_text=paper_text,
    )

    return [
        {
            "role": "system",
            "content": SYSTEM_PROMPT_INSTRUCTIONS,
        },
        {"role": "user", "content": prompt_text},
    ]

