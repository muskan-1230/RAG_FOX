import os
import json
import faiss
import numpy as np

from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import google.generativeai as genai


# =====================
# Gemini Setup
# =====================

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

gemini_model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


# =====================
# Embedding Model
# =====================

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def ask_document(
    document_id,
    question
):

    # ---------------------
    # Load FAISS
    # ---------------------

    index = faiss.read_index(
        f"vector_store/{document_id}/index.faiss"
    )

    # ---------------------
    # Load Metadata
    # ---------------------

    with open(
        f"vector_store/{document_id}/metadata.json",
        "r",
        encoding="utf-8"
    ) as f:

        metadata = json.load(f)

    # ---------------------
    # Question Embedding
    # ---------------------

    question_embedding = (
        embedding_model.encode(
            [question]
        )
    )

    distances, indices = index.search(
        np.array(question_embedding)
        .astype("float32"),
        k=3
    )

    retrieved_chunks = []

    sources = []

    for idx in indices[0]:

        retrieved_chunks.append(
            metadata[str(idx)]["text"]
        )

        sources.append({
            "chunk_id":
            metadata[str(idx)]["chunk_id"],

            "source":
            metadata[str(idx)]["source"]
        })

    context = "\n\n".join(
        retrieved_chunks
    )

    prompt = f"""
Answer ONLY using the context.

If the answer is not present,
say:

'I could not find that information in the document.'

Context:

{context}

Question:

{question}
"""

    response = (
        gemini_model.generate_content(
            prompt
        )
    )

    return {
        "answer": response.text,
        "sources": sources
    }