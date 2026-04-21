import argparse
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from preprocessing import convert_pdf_folder_with_report


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert PDFs to markdown and save Methods/Results sections."
    )
    parser.add_argument(
        "--input-dir",
        default="data/papers",
        help="Directory containing source PDF files.",
    )
    parser.add_argument(
        "--output-dir",
        default="data/markdown_outputs",
        help="Directory where extracted markdown files will be written.",
    )
    args = parser.parse_args()

    try:
        report = convert_pdf_folder_with_report(args.input_dir, args.output_dir)
    except Exception as exc:
        print(f"An error occurred during conversion: {exc}")
        return

    if not report.written_files:
        print("No markdown files were written.")
    else:
        print(f"Wrote {len(report.written_files)} markdown files to {args.output_dir}:")
        for path in report.written_files:
            print(f"- {path}")

    if report.skipped_files:
        print("\nSkipped files:")
        for filename, reason in report.skipped_files.items():
            print(f"- {filename}: {reason}")


if __name__ == "__main__":
    main()
