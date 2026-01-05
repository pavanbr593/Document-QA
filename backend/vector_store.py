import faiss
import numpy as np


def build_faiss_index(embeddings):
    """
    Create FAISS index from embeddings
    """
    dim = embeddings.shape[1]  # 384
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings).astype("float32"))
    return index


def search_index(index, query_embedding, top_k=3):
    """
    Search FAISS index using query embedding
    """
    distances, indices = index.search(
        np.array([query_embedding]).astype("float32"),
        top_k
    )
    return indices[0], distances[0]


if __name__ == "__main__":
    from backend.pdf_loader import load_pdf
    from backend.chunker import chunk_text
    from backend.embeddings import embed_text

    pdf_path = "data/uploads/test.pdf"

    # Load + chunk
    text = load_pdf(pdf_path)
    chunks = chunk_text(text)

    # Embed
    embeddings = embed_text(chunks)

    # Build FAISS
    index = build_faiss_index(embeddings)

    # Ask a test question
    question = "What is soil health?"
    question_embedding = embed_text([question])[0]

    # Search
    indices, distances = search_index(index, question_embedding)

    print("\nTop matching chunks:\n")
    for i, idx in enumerate(indices):
        print(f"Result {i+1} (distance={distances[i]:.4f})")
        print(chunks[idx][:500])
        print("-" * 50)