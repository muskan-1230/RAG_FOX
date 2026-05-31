def chunk_text(text, chunk_size=500):
    
    chunks = []

    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]
        chunks.append(chunk)

    return chunks


sample_text = """
Python is a programming language.

It is widely used in AI.

FastAPI is a backend framework.

RAG stands for Retrieval Augmented Generation.

Vector databases store embeddings.
"""


chunks = chunk_text(sample_text, chunk_size=50)

for index, chunk in enumerate(chunks):
    print(f"\n----- Chunk {index + 1} -----")
    print(chunk)