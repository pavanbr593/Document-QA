def chunk_text(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []

    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk_words = words[start:end]
        chunk = " ".join(chunk_words)
        chunks.append(chunk)

        start = end - overlap  # move with overlap

    return chunks


if __name__ == "__main__":
    from backend.pdf_loader import load_pdf

    pdf_path = "data/uploads/test.pdf"
    text = load_pdf(pdf_path)

    chunks = chunk_text(text)

    print(f"Total chunks created: {len(chunks)}")
    print("\n--- SAMPLE CHUNK ---\n")
    print(chunks[0][:1500])