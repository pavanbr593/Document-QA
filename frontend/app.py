import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="Document Intelligence",
    page_icon="📄",
    layout="wide"
)

# -------------------- CUSTOM CSS --------------------
st.markdown(
    """
    <style>
        body {
            background-color: #0f1117;
        }
        .main {
            background-color: #0f1117;
        }
        h1, h2, h3, h4 {
            color: #ffffff;
        }
        p, span, label {
            color: #c9d1d9;
        }
        .block-container {
            padding-top: 2rem;
        }
        .card {
            background-color: #161b22;
            padding: 1.5rem;
            border-radius: 12px;
            margin-bottom: 1.5rem;
            border: 1px solid #30363d;
        }
        .success {
            color: #3fb950;
        }
        .error {
            color: #f85149;
        }
        .source-box {
            background-color: #0d1117;
            border: 1px solid #30363d;
            border-radius: 8px;
            padding: 1rem;
            margin-top: 0.5rem;
            font-size: 0.9rem;
        }
        footer {
            visibility: hidden;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------- HEADER --------------------
st.markdown(
    """
    <h1>📄 Document Intelligence Platform</h1>
    <p>
    Ask questions and get accurate, citation-grounded answers from your documents
    using <b>Retrieval-Augmented Generation (RAG)</b>.
    </p>
    """,
    unsafe_allow_html=True
)

# -------------------- LAYOUT --------------------
col1, col2 = st.columns([1, 1.4])

# -------------------- LEFT: UPLOAD --------------------
with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📤 Upload Document")

    uploaded_file = st.file_uploader(
        "Upload a PDF document",
        type=["pdf"],
        label_visibility="collapsed"
    )

    if uploaded_file:
        with st.spinner("Indexing document…"):
            response = requests.post(
                f"{BACKEND_URL}/upload",
                files={"file": uploaded_file}
            )

        if response.status_code == 200:
            data = response.json()
            st.markdown(
                f"""
                <p class="success">
                ✅ Document indexed successfully<br>
                📄 Chunks created: <b>{data['chunks']}</b>
                </p>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                "<p class='error'>❌ Failed to upload document</p>",
                unsafe_allow_html=True
            )

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------- RIGHT: Q&A --------------------
with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("💬 Ask a Question")

    question = st.text_area(
        "Type your question",
        height=90,
        placeholder="e.g. Define soil health and explain its importance",
        label_visibility="collapsed"
    )

    ask_btn = st.button("Ask Question", use_container_width=True)

    if ask_btn:
        if not question.strip():
            st.warning("Please enter a valid question.")
        else:
            with st.spinner("Generating answer…"):
                response = requests.post(
                    f"{BACKEND_URL}/ask",
                    params={"question": question}
                )

            if response.status_code == 200:
                result = response.json()

                st.markdown("### ✅ Answer")
                st.write(result["answer"])

                st.markdown("### 📚 Sources")
                for i, src in enumerate(result["sources"]):
                    with st.expander(f"Source {i+1}"):
                        st.markdown(
                            f"<div class='source-box'>{src}</div>",
                            unsafe_allow_html=True
                        )
            else:
                st.error("Failed to get response from backend.")

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------- FOOTER --------------------
st.markdown(
    """
    <hr>
    <p style="text-align:center; font-size:0.85rem;">
    Built with FAISS • SentenceTransformers • FastAPI • Ollama (Phi-3)
    </p>
    """,
    unsafe_allow_html=True
)