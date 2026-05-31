from sentence_transformers import SentenceTransformer
from sentence_transformers import util

model = SentenceTransformer("all-MiniLM-L6-v2")

chunks = [
    "Python is a programming language.",
    "FastAPI is a modern web framework.",
    "RAG uses embeddings and vector databases.",
    "Pizza is an Italian food."
]

question = "What does RAG use?"

question_embedding = model.encode(question)

best_score = -1
best_chunk = ""

for chunk in chunks:

    chunk_embedding = model.encode(chunk)

    score = util.cos_sim(
        question_embedding,
        chunk_embedding
    )

    print(f"\nChunk: {chunk}")
    print(f"Score: {score.item():.4f}")

    if score > best_score:
        best_score = score
        best_chunk = chunk

print("\n======================")
print("BEST MATCH:")
print(best_chunk)
print("======================")