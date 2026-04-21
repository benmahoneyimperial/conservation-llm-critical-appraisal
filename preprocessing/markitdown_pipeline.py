from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .section_extractor import process_paper


@dataclass
class ConversionReport:
    written_files: list[Path] = field(default_factory=list)
    skipped_files: dict[str, str] = field(default_factory=dict)


def create_markitdown() -> Any:
    """Create a MarkItDown converter with the default PDF setup."""
    try:
        from markitdown import MarkItDown
    except ImportError as exc:
        raise ImportError(
            "MarkItDown is not installed. Install it with `pip install \"markitdown[pdf]\"`."
        ) from exc

    return MarkItDown(enable_plugins=False)


def convert_pdf_to_markdown(pdf_path: str | Path, converter: Any | None = None) -> str:
    """Convert one PDF file to markdown text."""
    pdf_path = Path(pdf_path)
    converter = converter or create_markitdown()
    result = converter.convert(str(pdf_path))

    markdown = getattr(result, "text_content", None)
    if not markdown:
        raise ValueError(f"No markdown content was returned for {pdf_path.name}.")

    return markdown


def build_extracted_markdown(paper: dict[str, str | None]) -> str:
    """Build the markdown file we want to keep for downstream appraisal."""
    parts = [f"# {Path(str(paper['filename'])).stem}"]

    if paper.get("methods"):
        parts.append(f"## Methods\n{paper['methods']}")

    if paper.get("results"):
        parts.append(f"## Results\n{paper['results']}")

    return "\n\n".join(parts).strip()


def _detect_conversion_issue(markdown: str) -> str | None:
    if markdown.count("(cid:") >= 20:
        return "converted text appears garbled and likely needs OCR or a different PDF parser"

    return None


def convert_pdf_folder_with_report(
    input_dir: str | Path = "data/papers",
    output_dir: str | Path = "data/markdown_outputs",
    converter: Any | None = None,
) -> ConversionReport:
    """Convert PDFs to markdown and record both written and skipped files."""
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    converter = converter or create_markitdown()
    report = ConversionReport()

    for pdf_path in sorted(input_dir.glob("*.pdf")):
        try:
            markdown = convert_pdf_to_markdown(pdf_path, converter=converter)
        except Exception as exc:
            report.skipped_files[pdf_path.name] = str(exc)
            continue

        paper = process_paper(markdown, f"{pdf_path.stem}.md")
        if paper["methods"] or paper["results"]:
            output_path = output_dir / f"{pdf_path.stem}.md"
            output_path.write_text(build_extracted_markdown(paper), encoding="utf-8")
            report.written_files.append(output_path)
            continue

        issue = _detect_conversion_issue(markdown)
        if issue:
            report.skipped_files[pdf_path.name] = issue
            continue

        report.skipped_files[pdf_path.name] = (
            "no Methods or Results sections were found in the converted text"
        )

    return report


def convert_pdf_folder(
    input_dir: str | Path = "data/papers",
    output_dir: str | Path = "data/markdown_outputs",
    converter: Any | None = None,
) -> list[Path]:
    """Convert PDFs to markdown and save Methods/Results-only outputs."""
    report = convert_pdf_folder_with_report(input_dir, output_dir, converter=converter)
    return report.written_files
