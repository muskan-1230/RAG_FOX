import faiss
import numpy as np

dimension = 384

index = faiss.IndexFlatL2(dimension)

vectors = np.random.rand(5, dimension).astype("float32")

index.add(vectors)

print("Total vectors:", index.ntotal)