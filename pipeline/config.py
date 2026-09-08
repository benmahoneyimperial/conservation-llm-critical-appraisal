"""Run configuration. Edit this file to change the scope of a run."""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

MODELS = [
    "anthropic/claude-opus-5",
    "deepseek/deepseek-v4-pro",
    "z-ai/glm-5.2",
]

METHODS = ["sequential", "tree_guided", "question_scoring"]

# Papers to evaluate (inclusive range of numeric paper IDs).
PAPER_FIRST = 200
PAPER_LAST = 350

CHUNK_SIZE = 25

PAPERS_DIR = REPO_ROOT / "data" / "papers" / "json" / "all_papers"
GUIDANCE_PATH = REPO_ROOT / "data" / "guidance_intro_md" / "guidance_intro.md"
RESULTS_DIR = REPO_ROOT / "output"

# Short directory names used under output/ for each model.
MODEL_DIR_NAMES = {
    "anthropic/claude-opus-5": "claude-opus-5",
    "deepseek/deepseek-v4-pro": "deepseek-v4-pro",
    "z-ai/glm-5.2": "glm-5.2",
    "openai/gpt-5.6-sol": "gpt-5.6-sol",
}


def model_tag(model: str) -> str:
    """Filesystem directory name for a model."""
    if model in MODEL_DIR_NAMES:
        return MODEL_DIR_NAMES[model]
    return model.replace("/", "_").replace(":", "_").replace(" ", "_")
