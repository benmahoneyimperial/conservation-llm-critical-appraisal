import pdfplumber

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

if __name__ == "__main__":
    # This is an example of how to use the function.
    # Note: 'data/sample_paper.pdf' is currently an empty file.
    # To test this script, replace it with a real PDF file.
    pdf_path = "data/sample_paper.pdf"
    try:
        text = extract_text_from_pdf(pdf_path)
        if not text:
            print(f"No text found in {pdf_path}. The file might be empty or contain only images.")
        else:
            print(f"Extracted text from {pdf_path}:")
            print(text)
    except Exception as e:
        print(f"An error occurred: {e}")
