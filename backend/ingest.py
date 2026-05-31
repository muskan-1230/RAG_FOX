from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json
import os


# Load embedding model once
embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


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

        sentence = sentence.strip()

        if not sentence:
            continue

        sentence += ". "

        if len(current_chunk) + len(sentence) <= chunk_size:

            current_chunk += sentence

        else:

            chunks.append(current_chunk.strip())

            current_chunk = sentence

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


def ingest_document(pdf_path, document_id):

    print(f"\nStarting ingestion: {document_id}")

    # -------------------------
    # Extract Text
    # -------------------------

    text = extract_text(pdf_path)

    # -------------------------
    # Chunking
    # -------------------------

    chunks = chunk_text(text)

    print(f"Chunks Created: {len(chunks)}")

    # -------------------------
    # Embeddings
    # -------------------------

    embeddings = embedding_model.encode(chunks)

    # -------------------------
    # Create Vector Store Folder
    # -------------------------

    save_folder = f"vector_store/{document_id}"

    os.makedirs(
        save_folder,
        exist_ok=True
    )

    # -------------------------
    # FAISS
    # -------------------------

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(
        dimension
    )

    index.add(
        np.array(embeddings).astype(
            "float32"
        )
    )

    faiss.write_index(
        index,
        f"{save_folder}/index.faiss"
    )

    # -------------------------
    # Metadata
    # -------------------------

    metadata = {}

    file_name = os.path.basename(
        pdf_path
    )

    for i, chunk in enumerate(chunks):

        metadata[str(i)] = {

            "chunk_id": i,

            "source": file_name,

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

    print(
        f"Ingestion Complete: {document_id}"
    )

    return {
        "document_id": document_id,
        "chunks": len(chunks)
    }