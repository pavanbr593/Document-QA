from sentence_transformers import SentenceTransformer


# Load model once (important for performance)
model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_text(chunks):
    """
    Converts list of text chunks into embeddings
    """
    embeddings = model.encode(chunks, show_progress_bar=True)
    return embeddings


if __name__ == "__main__":
    from backend.pdf_loader import load_pdf
    from backend.chunker import chunk_text

    pdf_path = "data/uploads/test.pdf"

    text = load_pdf(pdf_path)
    chunks = chunk_text(text)

    embeddings = embed_text(chunks)

    print(f"Total chunks: {len(chunks)}")
    print(f"Embedding shape: {embeddings.shape}")
    print("\nFirst embedding (first 10 values):")
    print(embeddings[0][:10])