import pdfplumber
import os
import sys
import argparse
from tqdm import tqdm

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extracts text from a PDF file.

    Args:
        pdf_path: The path to the PDF file.

    Returns:
        A string containing the text from the PDF.
    """
    paper_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            paper_text += page.extract_text()
    return paper_text


def preprocess_all_pdfs(input_dir: str, output_dir: str):
    """
    Extracts text from all PDF files in an input directory and saves them as .txt files
    in an output directory.
    """
    print(f"Starting PDF preprocessing...")
    print(f"Input directory: '{input_dir}'")
    print(f"Output directory: '{output_dir}'")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    pdf_files = [f for f in os.listdir(input_dir) if f.endswith(".pdf")]
    
    if not pdf_files:
        print("No PDF files found in the input directory.")
        return

    for pdf_file in tqdm(pdf_files, desc="Processing PDFs"):
        pdf_path = os.path.join(input_dir, pdf_file)
        text_filename = pdf_file + ".txt"
        text_path = os.path.join(output_dir, text_filename)

        try:
            paper_text = extract_text_from_pdf(pdf_path)
            with open(text_path, "w", encoding="utf-8") as f:
                f.write(paper_text)
        except Exception as e:
            print(f"Error processing {pdf_file}: {e}")

    print(f"Preprocessing complete. {len(pdf_files)} files processed.")


if __name__ == "__main__":
    # This allows running the script from the command line.
    # Example usage:
    # python paper_processing/pdf_processor.py data/papers data/processed_text

    parser = argparse.ArgumentParser(
        description="Extract text from PDF files in a directory."
    )
    parser.add_argument(
        "input_dir",
        type=str,
        help="The directory containing PDF files."
    )
    parser.add_argument(
        "output_dir",
        type=str,
        help="The directory where extracted .txt files will be saved."
    )

    args = parser.parse_args()
    preprocess_all_pdfs(args.input_dir, args.output_dir)