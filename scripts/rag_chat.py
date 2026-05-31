import os
import json
import faiss
import numpy as np

from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

import google.generativeai as genai


# =========================
# GEMINI
# =========================

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

gemini_model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


# =========================
# LOAD MODEL
# =========================

print("Loading embedding model...")

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# =========================
# LOAD FAISS
# =========================

index = faiss.read_index(
    "vector_store/sample/index.faiss"
)


# =========================
# LOAD METADATA
# =========================

with open(
    "vector_store/sample/metadata.json",
    "r",
    encoding="utf-8"
) as f:

    metadata = json.load(f)


# =========================
# CHAT LOOP
# =========================

while True:

    question = input("\nAsk a question (or type exit): ")

    if question.lower() == "exit":
        break

    question_embedding = embedding_model.encode(
        [question]
    )

    distances, indices = index.search(
        np.array(question_embedding).astype("float32"),
        k=3
    )

    retrieved_chunks = []

    for idx in indices[0]:

        retrieved_chunks.append(
            metadata[str(idx)]["text"]
        )

    context = "\n\n".join(
        retrieved_chunks
    )

    prompt = f"""
You are a helpful assistant.

Answer ONLY from the provided context.

If the answer is not present in the context,
say "I could not find that information in the document."

Context:
{context}

Question:
{question}
"""

    response = gemini_model.generate_content(
        prompt
    )

    print("\n")
    print("=" * 60)
    print("ANSWER")
    print("=" * 60)

    print(response.text)