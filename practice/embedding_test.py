from sentence_transformers import SentenceTransformer

print("Loading model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Model loaded!")

text = "Hello World"

embedding = model.encode(text)

print("\nEmbedding Length:", len(embedding))

print("\nFirst 10 values:")
print(embedding[:10])