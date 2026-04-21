from __future__ import annotations

import re
from pathlib import Path

METHODS_HEADINGS = (
    "methods",
    "materials and methods",
    "methods and materials",
    "methodology",
)

RESULTS_HEADINGS = (
    "results",
    "findings",
    "results and discussion",
)

COMMON_SECTION_HEADINGS = (
    "abstract",
    "introduction",
    "background",
    "methods",
    "materials and methods",
    "methods and materials",
    "methodology",
    "results",
    "results and discussion",
    "discussion",
    "conclusion",
    "conclusions",
    "references",
    "acknowledgements",
    "acknowledgments",
    "appendix",
)

_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*$", re.MULTILINE)
_SPACES_RE = re.compile(r"[ \t]+")
_BLANK_LINES_RE = re.compile(r"\n{3,}")


def clean_text(text: str) -> str:
    """Normalise spacing while keeping simple markdown structure intact."""
    text = text.replace("\x00", "")
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    lines = [_SPACES_RE.sub(" ", line).strip() for line in text.split("\n")]
    cleaned = "\n".join(lines).strip()
    return _BLANK_LINES_RE.sub("\n\n", cleaned)


def _normalise_heading(title: str) -> str:
    title = title.lower().strip()
    title = title.replace("&", "and")
    title = re.sub(r"[*_`]", "", title)
    # Strip leading numbers (e.g., "1.1 "), letters (e.g., "A. "), and roman numerals (e.g., "IV. ")
    title = re.sub(r"^(?:[\d.\s]+|(?:[a-z]|i{1,3}|iv|v|vi{1,3}|ix|x)[.)]\s*)", "", title)
    title = re.sub(r"[:.\-–—\s]+$", "", title)
    return _SPACES_RE.sub(" ", title)


def _compact_heading(title: str) -> str:
    return re.sub(r"[^a-z]+", "", _normalise_heading(title))


def _matches_heading(title: str, section_names: tuple[str, ...] | list[str], strict: bool = False) -> bool:
    normalised = _normalise_heading(title)
    compact = _compact_heading(title)

    for name in section_names:
        if strict:
            if name == normalised:
                return True
            if _compact_heading(name) and _compact_heading(name) == compact:
                return True
        else:
            if name in normalised:
                return True
            if _compact_heading(name) and _compact_heading(name) in compact:
                return True

    return False


def _is_plain_text_heading(line: str, section_names: tuple[str, ...] | list[str]) -> bool:
    stripped = line.strip()
    if not stripped or len(stripped) > 80:
        return False

    return _matches_heading(stripped, section_names, strict=True)


def _extract_plain_text_section(
    text: str,
    section_names: tuple[str, ...] | list[str],
) -> str | None:
    lines = text.splitlines()

    for index, line in enumerate(lines):
        if not _is_plain_text_heading(line, section_names):
            continue

        collected: list[str] = []

        for next_line in lines[index + 1 :]:
            if _is_plain_text_heading(next_line, COMMON_SECTION_HEADINGS):
                break
            collected.append(next_line)

        section_text = clean_text("\n".join(collected)).strip()
        return section_text or None

    return None


def extract_section(markdown_text: str, section_names: tuple[str, ...] | list[str]) -> str | None:
    """Extract the body of the first matching markdown heading."""
    text = clean_text(markdown_text)
    headings = list(_HEADING_RE.finditer(text))

    for index, heading in enumerate(headings):
        if not _matches_heading(heading.group(2), section_names):
            continue

        start = heading.end()
        end = len(text)
        level = len(heading.group(1))

        for next_heading in headings[index + 1 :]:
            if len(next_heading.group(1)) <= level:
                end = next_heading.start()
                break

        section_text = text[start:end].strip()
        return section_text or None

    return _extract_plain_text_section(text, section_names)


def process_paper(markdown_text: str, filename: str) -> dict[str, str | None]:
    """Extract the Methods and Results sections from one markdown document."""
    return {
        "filename": filename,
        "methods": extract_section(markdown_text, METHODS_HEADINGS),
        "results": extract_section(markdown_text, RESULTS_HEADINGS),
    }


def process_folder(folder_path: str | Path) -> list[dict[str, str | None]]:
    """Process every markdown file in a folder."""
    folder = Path(folder_path)
    papers: list[dict[str, str | None]] = []

    for markdown_path in sorted(folder.glob("*.md")):
        papers.append(
            process_paper(
                markdown_path.read_text(encoding="utf-8"),
                markdown_path.name,
            )
        )

    return papers


def format_for_llm(paper: dict[str, str | None]) -> str:
    """Format an extracted paper into a compact markdown prompt block."""
    parts = [f"# {paper['filename']}"]

    if paper.get("methods"):
        parts.append(f"### METHODS\n{paper['methods']}")

    if paper.get("results"):
        parts.append(f"### RESULTS\n{paper['results']}")

    return "\n\n".join(parts)
