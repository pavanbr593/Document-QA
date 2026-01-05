def qa_prompt(context: str, question: str) -> str:
    return f"""
You are a document-based assistant.

Answer the question using ONLY the information provided in the context.
If the answer is not present in the context, say:
"The document does not contain this information."

Context:
{context}

Question:
{question}

Answer:
"""