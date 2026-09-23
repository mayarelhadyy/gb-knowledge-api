from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException,
    Depends
)
import os

from services.vector_service import store_chunks
from services.pdf_service import extract_text_from_pdf
from services.chunk_service import chunk_text
from services.embedding_service import create_embeddings
from dependencies import require_hr


router = APIRouter(
    prefix="/upload",
    tags=["Upload"],
    dependencies=[
        Depends(require_hr)
    ]
)

@router.post("/pdf")
async def upload_pdf(
    file: UploadFile = File(...)
):

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only PDF files are allowed."
        )

    content = await file.read()

    os.makedirs("uploads", exist_ok=True)

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as saved_file:
        saved_file.write(content)

    extracted_text = extract_text_from_pdf(file_path)

    chunks = chunk_text(extracted_text)

    embeddings = create_embeddings(chunks)

    stored_count = store_chunks(
    chunks,
    embeddings,
    file.filename
)

    return {
        "message": "PDF accepted",
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(content),
        "extracted_text": extracted_text,
        "chunks": chunks,
        "first_embedding": embeddings[0].tolist(),
        "stored_chunks": stored_count
    }