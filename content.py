import fitz  # PyMuPDF
import re


def extract_text_from_pdf(pdf_path, output_md):
    doc = fitz.open(pdf_path)
    extracted_text = "# LPDP Handbook Extracted Content\n\n"

    for page_num, page in enumerate(doc, start=1):
        text = page.get_text("text")
        text = re.sub(r'\n+', '\n', text).strip()  # Normalize newlines

        if text:
            extracted_text += f"## Page {page_num}\n\n{text}\n\n"

    with open(output_md, "w", encoding="utf-8") as f:
        f.write(extracted_text)

    print(f"Extraction complete. Saved to {output_md}")


# Example usage:
pdf_path = "lpdp-handbook-content.pdf"  # Change to your PDF file
output_md = "lpdp_extracted.md"
extract_text_from_pdf(pdf_path, output_md)