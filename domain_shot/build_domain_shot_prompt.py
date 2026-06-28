import glob
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DEFAULT_DOMAIN_GUIDANCE_DIR = os.path.join(PROJECT_ROOT, "data", "guidance_by_domain_md")
DEFAULT_GUIDANCE_INTRO_PATH = os.path.join(PROJECT_ROOT, "data", "guidance_intro_md", "guidance_intro.md")
DEFAULT_PAPERS_DIR = os.path.join(PROJECT_ROOT, "data", "sample_papers", "sample_papers_md")

SYSTEM_PROMPT_INSTRUCTIONS = """You are an expert human systematic reviewer performing structured risk-of-bias assessment.

You must follow the domain guidance strictly and base all judgments only on evidence explicitly found in the provided paper.
You are not allowed to use external knowledge or assumptions.

Please return your evaluation as valid JSON.
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


def build_prompt(
    domain_name: str,
    domain_guidance_text: str,
    paper_text: str,
    intro_text: str,
) -> str:
    """Join the prompt parts into a single prompt string in the intended order."""
    guidance_intro = intro_text or ""
    domain_guidance = domain_guidance_text or ""
    paper = paper_text or ""

    sections = []
    if guidance_intro:
        sections.append(f"--- GUIDANCE INTRO ---\n{guidance_intro}")
    if domain_guidance:
        sections.append(f"--- GUIDANCE FOR {domain_name} ---\n{domain_guidance}")
    if paper:
        sections.append(f"--- RESEARCH PAPER ---\n{paper}")

    return "\n\n".join(sections)


def build_prompt_messages(
    domain_name: str,
    domain_text: str,
    paper_text: str,
    intro_text: str,
) -> list:
    """Build the system and user message content for the LLM."""
    prompt_text = build_prompt(
        domain_name=domain_name,
        domain_guidance_text=domain_text,
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

