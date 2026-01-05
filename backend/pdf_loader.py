import os
from PyPDF2 import PdfReader


def load_pdf(pdf_path: str) -> str:
    print(f"Trying to load PDF from: {pdf_path}")

    if not os.path.exists(pdf_path):
        print("❌ PDF file not found")
        return ""

    reader = PdfReader(pdf_path)
    print(f"Total pages: {len(reader.pages)}")

    full_text = ""

    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        print(f"Page {i+1} extracted length:", 0 if text is None else len(text))
        if text:
            full_text += f"\n--- Page {i+1} ---\n"
            full_text += text

    return full_text


if __name__ == "__main__":
    pdf_path = "data/uploads/test.pdf"
    text = load_pdf(pdf_path)

    print("\n========== FINAL OUTPUT ==========")
    if text.strip():
        print(text[:2000])
    else:
        print("❌ No text extracted from PDF")