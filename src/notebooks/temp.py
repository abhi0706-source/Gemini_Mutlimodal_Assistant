import fitz  # PyMuPDF
import pytesseract
from PIL import Image


# Define a function to extract text from all pages of a PDF
def extract_text_from_pdf(pdf_path, dpi=300):
    """
    Extract text from all pages of a PDF.

    Args:
        pdf_path (str): Path to the PDF file.
        dpi (int): Resolution for converting PDF pages to images (default: 300).

    Returns:
        dict: A dictionary where keys are page numbers (1-based) and values are extracted text.
    """
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    extracted_text = {}

    for page_number in range(len(pdf_document)):
        # Select the page
        page = pdf_document[page_number]

        # Convert the page to an image
        pixmap = page.get_pixmap(dpi=dpi)

        # Save the image to a temporary file
        image = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)

        # Extract text from the image using Tesseract
        text = pytesseract.image_to_string(image)

        print(text)

        # Store the text in the dictionary
        extracted_text[page_number + 1] = text

    # Close the PDF document
    pdf_document.close()

    return extracted_text


# Usage example
if __name__ == "__main__":
    # pdf_path = "c:/Abhi-MTech/Sem-1/AI/Books/Artificial.Intelligence.A.Modern.Approach.4th.Edition.Peter.Norvig. Stuart.Russell.Pearson.9780134610993.EBooksWorld.ir.pdf"  # Path to your PDF file
    pdf_path = "c:/Abhi-MTech/Sem-1/AI/AI Technical.pdf"  # Path to your PDF file

    try:
        all_text = extract_text_from_pdf(pdf_path)
        for page_num, text in all_text.items():
            print(f"Page {page_num} Text:")
            print(text)
            print("-" * 80)  # Separator for readability
    except Exception as e:
        print(f"Error: {e}")
