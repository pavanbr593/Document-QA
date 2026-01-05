import requests
from backend.pdf_loader import load_pdf
from backend.chunker import chunk_text
from backend.embeddings import embed_text
from backend.vector_store import build_faiss_index, search_index


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "phi3"


def generate_answer(question, chunks, index):
    # Embed the question
    question_embedding = embed_text([question])[0]

    # Retrieve top chunks
    indices, distances = search_index(index, question_embedding, top_k=3)

    retrieved_chunks = [chunks[i] for i in indices]

    # Build context
    context = "\n\n".join(retrieved_chunks)

    prompt = f"""
You are a document-based assistant.

Answer the question using ONLY the information provided in the context.
If the answer is not present, say "The document does not contain this information."

Context:
{context}

Question:
{question}

Answer:
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"], retrieved_chunks


if __name__ == "__main__":
    pdf_path = "data/uploads/test.pdf"

    # Load document
    text = load_pdf(pdf_path)
    chunks = chunk_text(text)

    # Embed + index
    embeddings = embed_text(chunks)
    index = build_faiss_index(embeddings)

    # Ask question
    question = "Define soil health and explain its importance."

    answer, sources = generate_answer(question, chunks, index)

    print("\nQUESTION:")
    print(question)

    print("\nANSWER:")
    print(answer)

    print("\n--- SOURCES USED ---")
    for i, src in enumerate(sources):
        print(f"\nSource {i+1}:")
        print(src[:400])