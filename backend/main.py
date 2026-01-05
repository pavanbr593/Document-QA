from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

from backend.pdf_loader import load_pdf
from backend.chunker import chunk_text
from backend.embeddings import embed_text
from backend.vector_store import build_faiss_index
from backend.rag_pipeline import generate_answer

app = FastAPI(title="Document Q&A RAG System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Global in-memory store (simple & fine for demo)
DOCUMENT_STORE = {}


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = load_pdf(file_path)
    chunks = chunk_text(text)
    embeddings = embed_text(chunks)
    index = build_faiss_index(embeddings)

    DOCUMENT_STORE["chunks"] = chunks
    DOCUMENT_STORE["index"] = index

    return {
        "message": "PDF uploaded and indexed successfully",
        "chunks": len(chunks)
    }


@app.post("/ask")
async def ask_question(question: str):
    if "index" not in DOCUMENT_STORE:
        return {"error": "No document uploaded yet"}

    answer, sources = generate_answer(
        question,
        DOCUMENT_STORE["chunks"],
        DOCUMENT_STORE["index"]
    )

    return {
        "question": question,
        "answer": answer,
        "sources": sources
    }