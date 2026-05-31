from sentence_transformers import SentenceTransformer
from sentence_transformers import util

model = SentenceTransformer("all-MiniLM-L6-v2")

sentence1 = "Python is a programming language"
sentence2 = "Python is used for software development"
sentence3 = "I like eating pizza"

embedding1 = model.encode(sentence1)
embedding2 = model.encode(sentence2)
embedding3 = model.encode(sentence3)

score_1_2 = util.cos_sim(embedding1, embedding2)
score_1_3 = util.cos_sim(embedding1, embedding3)

print(f"Similarity (1,2): {score_1_2.item():.4f}")
print(f"Similarity (1,3): {score_1_3.item():.4f}")