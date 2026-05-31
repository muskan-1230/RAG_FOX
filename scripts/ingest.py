from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json
import os


def extract_text(pdf_path):

    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


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


pdf_path = "data/sample.pdf"

document_name = "sample"

save_folder = f"vector_store/{document_name}"

os.makedirs(save_folder, exist_ok=True)

print("Reading PDF...")

text = extract_text(pdf_path)

chunks = chunk_text(text)

print("Chunks:", len(chunks))

print("Loading embedding model...")

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

embeddings = model.encode(chunks)

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(
    np.array(embeddings).astype("float32")
)

faiss.write_index(
    index,
    f"{save_folder}/index.faiss"
)

metadata = {}

for i, chunk in enumerate(chunks):

    metadata[str(i)] = {
    "chunk_id": i,
    "source": "sample.pdf",
    "text": chunk
}

with open(
    f"{save_folder}/metadata.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        metadata,
        f,
        indent=4,
        ensure_ascii=False
    )

print("\nIngestion Complete!")