import tempfile
import unittest
from pathlib import Path

from preprocessing import (
    build_extracted_markdown,
    clean_text,
    convert_pdf_folder,
    convert_pdf_folder_with_report,
    extract_section,
    format_for_llm,
    process_folder,
    process_paper,
)


class SectionExtractorTests(unittest.TestCase):
    def test_extracts_methods_and_combined_results(self) -> None:
        text = """# Title

## Methods
We sampled 20 sites.

## Results and Discussion
Intervention success increased.
"""
        paper = process_paper(text, "paper.md")

        self.assertEqual(paper["methods"], "We sampled 20 sites.")
        self.assertEqual(paper["results"], "Intervention success increased.")

    def test_extract_section_returns_none_when_missing(self) -> None:
        text = "# Introduction\nBackground only."
        self.assertIsNone(extract_section(text, ["methods"]))

    def test_extracts_plain_text_sections(self) -> None:
        text = """Title

Methods
We sampled 20 sites.

Results
Intervention success increased.

Discussion
The intervention is promising.
"""
        paper = process_paper(text, "paper.md")

        self.assertEqual(paper["methods"], "We sampled 20 sites.")
        self.assertEqual(paper["results"], "Intervention success increased.")

    def test_extracts_numbered_compact_sections(self) -> None:
        text = """2.materialsandmethods
Field protocol.

2.1.studyarea
Forest plot details.

3.results
Positive effect.

4.discussion
Interpretation.
"""
        paper = process_paper(text, "paper.md")

        self.assertIn("Field protocol.", paper["methods"])
        self.assertIn("Forest plot details.", paper["methods"])
        self.assertEqual(paper["results"], "Positive effect.")

    def test_clean_text_removes_nulls_and_extra_space(self) -> None:
        cleaned = clean_text("A\x00 line.\r\n\r\n\r\nB   line.  ")
        self.assertEqual(cleaned, "A line.\n\nB line.")

    def test_process_folder_and_formatter(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            paper_path = Path(tmp_dir) / "sample.md"
            paper_path.write_text(
                "# Methodology\nProtocol details.\n\n# Findings\nClear effect.",
                encoding="utf-8",
            )

            papers = process_folder(tmp_dir)

        self.assertEqual(len(papers), 1)
        self.assertEqual(papers[0]["filename"], "sample.md")
        self.assertIn("### METHODS\nProtocol details.", format_for_llm(papers[0]))
        self.assertIn("### RESULTS\nClear effect.", format_for_llm(papers[0]))

    def test_builds_output_markdown(self) -> None:
        paper = {
            "filename": "sample.md",
            "methods": "Protocol details.",
            "results": "Clear effect.",
        }

        output = build_extracted_markdown(paper)

        self.assertIn("# sample", output)
        self.assertIn("## Methods\nProtocol details.", output)
        self.assertIn("## Results\nClear effect.", output)

    def test_convert_pdf_folder_writes_extracted_sections(self) -> None:
        class DummyResult:
            def __init__(self, text_content: str) -> None:
                self.text_content = text_content

        class DummyConverter:
            def convert(self, path: str) -> DummyResult:
                self.last_path = path
                return DummyResult(
                    "# Methods\nField protocol.\n\n# Results and Discussion\nPositive effect."
                )

        with tempfile.TemporaryDirectory() as tmp_dir:
            input_dir = Path(tmp_dir) / "papers"
            output_dir = Path(tmp_dir) / "markdown_outputs"
            input_dir.mkdir()
            (input_dir / "sample.pdf").write_bytes(b"%PDF-1.4")

            written_files = convert_pdf_folder(
                input_dir=input_dir,
                output_dir=output_dir,
                converter=DummyConverter(),
            )

            self.assertEqual([path.name for path in written_files], ["sample.md"])
            output = (output_dir / "sample.md").read_text(encoding="utf-8")
            self.assertIn("## Methods\nField protocol.", output)
            self.assertIn("## Results\nPositive effect.", output)

    def test_convert_pdf_folder_with_report_tracks_skipped_files(self) -> None:
        class DummyResult:
            def __init__(self, text_content: str) -> None:
                self.text_content = text_content

        class DummyConverter:
            def convert(self, path: str) -> DummyResult:
                if path.endswith("good.pdf"):
                    return DummyResult("2.materialsandmethods\nProtocol.\n\n3.results\nEffect.")
                if path.endswith("garbled.pdf"):
                    return DummyResult("(cid:12)" * 30)
                return DummyResult("Background only.")

        with tempfile.TemporaryDirectory() as tmp_dir:
            input_dir = Path(tmp_dir) / "papers"
            output_dir = Path(tmp_dir) / "markdown_outputs"
            input_dir.mkdir()
            (input_dir / "good.pdf").write_bytes(b"%PDF-1.4")
            (input_dir / "garbled.pdf").write_bytes(b"%PDF-1.4")
            (input_dir / "missing.pdf").write_bytes(b"%PDF-1.4")

            report = convert_pdf_folder_with_report(
                input_dir=input_dir,
                output_dir=output_dir,
                converter=DummyConverter(),
            )

            self.assertEqual([path.name for path in report.written_files], ["good.md"])
            self.assertEqual(
                report.skipped_files["garbled.pdf"],
                "converted text appears garbled and likely needs OCR or a different PDF parser",
            )
            self.assertEqual(
                report.skipped_files["missing.pdf"],
                "no Methods or Results sections were found in the converted text",
            )


if __name__ == "__main__":
    unittest.main()
