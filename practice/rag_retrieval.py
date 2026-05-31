from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np


# -------------------------
# PDF TEXT EXTRACTION
# -------------------------

def extract_text_from_pdf(pdf_path):

    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


# -------------------------
# CHUNKING
# -------------------------

def chunk_text(text, chunk_size=300):

    sentences = text.replace("\n", " ").split(". ")

    chunks = []
    current_chunk = ""

    for sentence in sentences:

        sentence += ". "

        if len(current_chunk) + len(sentence) <= chunk_size:

            current_chunk += sentence

        else:

            chunks.append(current_chunk.strip())

            current_chunk = sentence

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


# -------------------------
# MAIN
# -------------------------

pdf_path = "data/sample.pdf"

print("Reading PDF...")

text = extract_text_from_pdf(pdf_path)

chunks = chunk_text(text)

print(f"Chunks Created: {len(chunks)}")

# -------------------------
# EMBEDDINGS
# -------------------------

print("Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

chunk_embeddings = model.encode(chunks)

# -------------------------
# FAISS
# -------------------------

dimension = chunk_embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(
    np.array(chunk_embeddings).astype("float32")
)

print("FAISS Index Ready!")

# -------------------------
# QUESTION
# -------------------------

question = input("\nAsk a question: ")

question_embedding = model.encode([question])

distances, indices = index.search(
    np.array(question_embedding).astype("float32"),
    k=3
)

print("\nTop Chunks:\n")

for rank, idx in enumerate(indices[0]):

    print("=" * 60)

    print(f"Rank {rank+1}")

    print(f"Chunk Index: {idx}")

    print(chunks[idx][:500])

    print("\n")