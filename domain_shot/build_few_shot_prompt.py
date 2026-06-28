import glob
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DEFAULT_DOMAIN_GUIDANCE_DIR = os.path.join(PROJECT_ROOT, "data", "guidance_by_domain_md")
DEFAULT_GUIDANCE_INTRO_PATH = os.path.join(PROJECT_ROOT, "data", "guidance_intro_md", "guidance_intro.md")
DEFAULT_DOMAIN_QUESTIONS_DIR = os.path.join(PROJECT_ROOT, "data", "domain_questions_md")
DEFAULT_EXAMPLES_DIR = os.path.join(PROJECT_ROOT, "examples")
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
    "final_risk_judgement": "Low Risk/Medium Risk/High Risk/Unclear",
    "short_rationale": "1-3 sentences grounded in target paper evidence"
}
"""


def read_text_file(path: str) -> str:
    """Load text content from a file path."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")

    with open(path, "r", encoding="utf-8") as handle:
        return handle.read()


def load_domain_guidance(guidance_dir: str) -> dict:
    """Read all domain guidance markdown files from a directory."""
    if not os.path.exists(guidance_dir):
        raise FileNotFoundError(f"Guidance directory not found: {guidance_dir}")

    files = glob.glob(os.path.join(guidance_dir, "*.md"))
    domain_guidance = {}

    for file_path in files:
        filename = os.path.basename(file_path)
        domain_name = os.path.splitext(filename)[0]
        with open(file_path, "r", encoding="utf-8") as handle:
            domain_guidance[domain_name] = handle.read()

    return dict(sorted(domain_guidance.items()))


def load_default_domain_guidance() -> dict:
    """Load all domain guidance files from the default project directory."""
    return load_domain_guidance(DEFAULT_DOMAIN_GUIDANCE_DIR)


def load_default_guidance_intro() -> str:
    """Load the shared guidance intro from the default project file."""
    return read_text_file(DEFAULT_GUIDANCE_INTRO_PATH)


def _load_domain_markdown_with_fallback(
    domain_name: str,
    base_dir: str,
    preferred_suffix: str,
    placeholder_label: str,
) -> str:
    """Load domain markdown using common naming conventions, else return a placeholder."""
    candidates = [
        os.path.join(base_dir, f"{domain_name}{preferred_suffix}.md"),
        os.path.join(base_dir, f"{domain_name}.md"),
    ]

    for path in candidates:
        if os.path.exists(path):
            return read_text_file(path)

    return (
        f"[PLACEHOLDER] No {placeholder_label} found for {domain_name}. "
        f"Expected one of: {', '.join(candidates)}"
    )


def load_domain_questions(domain_name: str, questions_dir: str = DEFAULT_DOMAIN_QUESTIONS_DIR) -> str:
    """Load domain questions markdown for one domain."""
    return _load_domain_markdown_with_fallback(
        domain_name=domain_name,
        base_dir=questions_dir,
        preferred_suffix="_questions",
        placeholder_label="domain questions file",
    )


def load_domain_examples(domain_name: str, examples_dir: str = DEFAULT_EXAMPLES_DIR) -> str:
    """Load worked examples markdown for one domain."""
    return _load_domain_markdown_with_fallback(
        domain_name=domain_name,
        base_dir=examples_dir,
        preferred_suffix="_examples",
        placeholder_label="worked examples file",
    )


def build_prompt(
    domain_name: str,
    domain_guidance_text: str,
    domain_questions_text: str,
    worked_examples_text: str,
    paper_text: str,
    intro_text: str,
) -> str:
    """Join the few-shot prompt parts into a single prompt string in the intended order."""
    guidance_intro = intro_text or ""
    domain_guidance = domain_guidance_text or ""
    domain_questions = domain_questions_text or ""
    worked_examples = worked_examples_text or ""
    paper = paper_text or ""

    sections = []
    if guidance_intro:
        sections.append(f"--- GUIDANCE INTRO ---\n{guidance_intro}")
    if domain_guidance:
        sections.append(f"--- DOMAIN GUIDANCE ({domain_name}) ---\n{domain_guidance}")
    if domain_questions:
        sections.append(f"--- DOMAIN QUESTIONS ({domain_name}) ---\n{domain_questions}")
    if worked_examples:
        sections.append(f"--- WORKED EXAMPLES ({domain_name}) ---\n{worked_examples}")
    if paper:
        sections.append(
            "--- TARGET PAPER ---\n"
            f"{paper}\n\n"
            "Using the same style as the worked examples, answer all domain questions and "
            "provide a final domain risk judgement in the required JSON format."
        )

    return "\n\n".join(sections)


def build_prompt_messages(
    domain_name: str,
    domain_guidance_text: str,
    domain_questions_text: str,
    worked_examples_text: str,
    paper_text: str,
    intro_text: str,
) -> list:
    """Build the system and user message content for the LLM."""
    prompt_text = build_prompt(
        domain_name=domain_name,
        domain_guidance_text=domain_guidance_text,
        domain_questions_text=domain_questions_text,
        worked_examples_text=worked_examples_text,
        paper_text=paper_text,
        intro_text=intro_text,
    )

    return [
        {
            "role": "system",
            "content": SYSTEM_PROMPT_INSTRUCTIONS,
        },
        {"role": "user", "content": prompt_text},
    ]

