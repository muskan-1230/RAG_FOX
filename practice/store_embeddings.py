from sentence_transformers import SentenceTransformer
import json

model = SentenceTransformer("all-MiniLM-L6-v2")

chunks = [
    "Python is a programming language.",
    "FastAPI is a modern web framework.",
    "RAG uses embeddings and vector databases.",
    "Pizza is an Italian food."
]

stored_data = []

for chunk in chunks:

    embedding = model.encode(chunk)

    stored_data.append({
        "text": chunk,
        "embedding": embedding.tolist()
    })

with open("embeddings.json", "w") as f:
    json.dump(stored_data, f)

print("Embeddings saved!")