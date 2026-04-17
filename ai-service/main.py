from fastapi import FastAPI, UploadFile, File, Depends
from sqlalchemy.orm import Session
from database import engine, get_db, Base
from models import Document, Chunk
from schemas import DocumentResponse
import fitz
from langchain_text_splitters import RecursiveCharacterTextSplitter
import uuid
import os

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/upload", response_model=DocumentResponse)
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):

    # Step 1 - Save file
    os.makedirs("uploads", exist_ok=True)
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Step 2 - Save document record
    document = Document(filename=file.filename)
    db.add(document)
    db.commit()
    db.refresh(document)

    # Step 3 - Extract text
    pdf = fitz.open(file_path)
    raw_text = ""
    for page in pdf:
        raw_text += page.get_text()

    # Step 4 - Chunk text
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_text(raw_text)

    # Step 5 - Store chunks
    for i, chunk_text in enumerate(chunks):
        chunk = Chunk(document_id=document.id, text=chunk_text, chunk_index=i)
        db.add(chunk)
    db.commit()

    return DocumentResponse(document_id=document.id, chunks=chunks)