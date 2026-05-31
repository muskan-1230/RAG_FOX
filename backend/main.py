from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel

from backend.ingest import ingest_document
from backend.rag_engine import ask_document

import os
import shutil
import uuid


app = FastAPI()


# =========================
# Request Models
# =========================

class ChatRequest(BaseModel):
    document_id: str
    question: str


# =========================
# Home Route
# =========================

@app.get("/")
def home():
    return {
        "message": "RAG_FOX Backend Running"
    }


# =========================
# Upload Route
# =========================

@app.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...)
):

    document_id = str(uuid.uuid4())

    upload_folder = f"uploads/{document_id}"

    os.makedirs(
        upload_folder,
        exist_ok=True
    )

    file_path = (
        f"{upload_folder}/{file.filename}"
    )

    # Save uploaded PDF
    with open(file_path, "wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    # Run ingestion
    result = ingest_document(
        file_path,
        document_id
    )

    return {
        "message": "Upload Successful",
        "document_id": document_id,
        "filename": file.filename,
        "chunks": result["chunks"]
    }


# =========================
# Chat Route
# =========================

@app.post("/chat")
def chat(
    request: ChatRequest
):

    result = ask_document(
        request.document_id,
        request.question
    )

    return result