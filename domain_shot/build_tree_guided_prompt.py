import glob
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DEFAULT_GUIDANCE_INTRO_PATH = os.path.join(PROJECT_ROOT, "data", "guidance_intro_md", "guidance_intro.md")
DEFAULT_DECISION_TREES_DIR = os.path.join(PROJECT_ROOT, "data", "decision_trees_only_md")
DEFAULT_DOMAIN_QUESTIONS_DIR = os.path.join(PROJECT_ROOT, "data", "domain_questions_md")
DEFAULT_PAPERS_DIR = os.path.join(PROJECT_ROOT, "data", "sample_papers", "sample_papers_md")

SYSTEM_PROMPT_INSTRUCTIONS = """You are an expert human systematic reviewer performing structured risk-of-bias assessment using domain decision trees and checklist questions.

You must follow the decision tree and domain questions strictly and base all judgments only on evidence explicitly found in the target paper.
You are not allowed to use external knowledge or assumptions.

Return JSON only (no markdown, no prose outside JSON) with this exact structure:
{
    "question_answers": {
        "<question_id>": "Yes|Seemingly yes|Seemingly no|No|Unclear|Not applicable"
    },
    "decision_path": [
        "<question_id> -> <answer>",
        "<question_id> -> <answer>",
        "<final_judgement>"
    ],
    "final_risk_judgement": "Low Risk|Medium Risk|High Risk|Unclear|Not Applicable",
    "short_rationale": "1-3 sentences grounded in paper evidence"
}

Critical output rules:
- Answer every domain question exactly once in question_answers.
- Allowed answers for each question are only: Yes, Seemingly yes, Seemingly no, No, Unclear, Not applicable.
- Follow conditional logic from the domain questions and use Not applicable when conditions are not met.
- decision_path must reflect the tree traversal used to reach final_risk_judgement.
- If the decision tree and checklist text appear to conflict, prioritize the decision tree and explain briefly in short_rationale.
- If evidence is insufficient, use Unclear rather than guessing.
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
    preferred_suffixes: list[str],
    file_label: str,
) -> str:
    """Resolve a required domain markdown path or raise FileNotFoundError."""
    candidates = []
    for suffix in preferred_suffixes:
        candidates.append(os.path.join(base_dir, f"{domain_name}{suffix}.md"))
    candidates.append(os.path.join(base_dir, f"{domain_name}.md"))

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
        preferred_suffixes=["_questions"],
        file_label="domain questions file",
    )
    return read_text_file(path)


def load_domain_decision_tree(domain_name: str, decision_trees_dir: str = DEFAULT_DECISION_TREES_DIR) -> str:
    """Load decision-tree markdown for one domain."""
    path = _resolve_domain_markdown_path(
        domain_name=domain_name,
        base_dir=decision_trees_dir,
        preferred_suffixes=["_decision_tree"],
        file_label="decision-tree file",
    )
    return read_text_file(path)


def _extract_domain_name(file_path: str) -> str:
    """Normalize a markdown filename into its base domain identifier."""
    stem = os.path.splitext(os.path.basename(file_path))[0]
    for suffix in ("_decision_tree", "_questions"):
        if stem.endswith(suffix):
            return stem[: -len(suffix)]
    return stem


def load_default_domain_prompt_parts(
    decision_trees_dir: str = DEFAULT_DECISION_TREES_DIR,
    questions_dir: str = DEFAULT_DOMAIN_QUESTIONS_DIR,
) -> dict:
    """Load per-domain decision trees and questions, keyed by domain name."""
    if not os.path.exists(decision_trees_dir):
        raise FileNotFoundError(f"Decision-tree directory not found: {decision_trees_dir}")

    if not os.path.exists(questions_dir):
        raise FileNotFoundError(f"Domain questions directory not found: {questions_dir}")

    tree_files = glob.glob(os.path.join(decision_trees_dir, "*.md"))
    question_files = glob.glob(os.path.join(questions_dir, "*.md"))

    tree_domains = {_extract_domain_name(path) for path in tree_files}
    question_domains = {_extract_domain_name(path) for path in question_files}

    common_domains = sorted(tree_domains.intersection(question_domains))
    if not common_domains:
        raise FileNotFoundError(
            "No overlapping domains found between decision-tree and domain-question directories."
        )

    prompt_parts = {}
    for domain_name in common_domains:
        prompt_parts[domain_name] = {
            "decision_tree_text": load_domain_decision_tree(domain_name, decision_trees_dir=decision_trees_dir),
            "domain_questions_text": load_domain_questions(domain_name, questions_dir=questions_dir),
        }

    return prompt_parts


def build_prompt(
    domain_name: str,
    intro_text: str,
    decision_tree_text: str,
    domain_questions_text: str,
    paper_text: str,
) -> str:
    """Join prompt parts into a single prompt string in the intended order."""
    guidance_intro = intro_text or ""
    decision_tree = decision_tree_text or ""
    domain_questions = domain_questions_text or ""
    paper = paper_text or ""

    applicability_gate = ""
    if domain_name == "domain_3":
        applicability_gate = (
            "5. Domain 3 applicability gate: determine if the study is observational. "
            "If not observational, set every Domain 3 answer to Not applicable and return final_risk_judgement as Not Applicable.\n"
        )
    elif domain_name == "domain_4":
        applicability_gate = (
            "5. Domain 4 applicability gate: determine if the study is experimental. "
            "If not experimental, set every Domain 4 answer to Not applicable and return final_risk_judgement as Not Applicable.\n"
        )

    sections = [
        f"--- GUIDANCE INTRO ---\n{guidance_intro}",
        f"--- DOMAIN QUESTIONS ({domain_name}) ---\n{domain_questions}",
        f"--- DECISION TREE ({domain_name}) ---\n{decision_tree}",
        (
            "--- TARGET PAPER ---\n"
            f"{paper}\n\n"
            "How to use these sections:\n"
            "1. Use GUIDANCE INTRO only as helpful background context for interpreting bias concepts.\n"
            "2. Read the TARGET PAPER and answer all DOMAIN QUESTIONS first (exactly once each, using allowed labels only).\n"
            "3. Then apply the DECISION TREE to those answers to produce decision_path and final_risk_judgement.\n"
            "4. Return JSON only, following the required schema from the system message.\n"
            f"{applicability_gate}"
        ),
    ]

    return "\n\n".join(sections)


def build_prompt_messages(
    domain_name: str,
    intro_text: str,
    decision_tree_text: str,
    domain_questions_text: str,
    paper_text: str,
) -> list:
    """Build the system and user message content for the LLM."""
    prompt_text = build_prompt(
        domain_name=domain_name,
        intro_text=intro_text,
        decision_tree_text=decision_tree_text,
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
