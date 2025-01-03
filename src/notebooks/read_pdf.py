import fitz  # PyMuPDF

# Load the PDF file
pdf_path = "../data/Artificial.Intelligence.A.Modern.Approach.4th.Edition.Peter.Norvig. Stuart.Russell.Pearson.9780134610993.EBooksWorld.ir.pdf"
doc = fitz.open(pdf_path)

# Extract text from each page
for page_number in range(len(doc)):
    page = doc[page_number]
    print(f"Page {page_number + 1}:")
    print(page.get_text())
    print("-" * 50)

# Close the document
doc.close()
