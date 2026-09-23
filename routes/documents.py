from fastapi import APIRouter, HTTPException, Depends

from models import Document
from dependencies import require_hr
from services.vector_service import (
    get_stored_documents,
    delete_document_chunks
)

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
    dependencies=[
        Depends(require_hr)
    ]
)


documents = []

@router.get("/knowledge-base")
def get_knowledge_base_documents():
    documents = get_stored_documents()

    return {
        "documents": documents
    }

@router.delete("/knowledge-base/{filename}")
def delete_knowledge_base_document(
    filename: str
):
    delete_document_chunks(filename)

    return {
        "message": "Document deleted successfully",
        "filename": filename
    }

@router.post("/")
def create_document(
    document: Document
):
    documents.append(document)

    return {
        "message": "Document created successfully!",
        "document": document
    }


@router.get("/")
def get_documents(
    department: str | None = None,
    limit: int = 10
):
    results = documents

    if department:
        results = [
            doc for doc in results
            if doc.department == department
        ]

    return {
        "documents": results[:limit]
    }


@router.get("/{document_id}")
def get_document(
    document_id: int
):
    if (
        document_id < 0
        or document_id >= len(documents)
    ):
        raise HTTPException(
            status_code=404,
            detail="Document not found!"
        )

    return {
        "document": documents[document_id]
    }


@router.put("/{document_id}")
def update_document(
    document_id: int,
    updated_document: Document
):
    if (
        document_id < 0
        or document_id >= len(documents)
    ):
        raise HTTPException(
            status_code=404,
            detail="Document not found!"
        )

    documents[document_id] = updated_document

    return {
        "message": "Document updated successfully!",
        "document": updated_document
    }



@router.delete("/{document_id}")
def delete_document(
    document_id: int
):
    if (
        document_id < 0
        or document_id >= len(documents)
    ):
        raise HTTPException(
            status_code=404,
            detail="Document not found!"
        )

    deleted_document = documents.pop(
        document_id
    )

    return {
        "message": "Document deleted successfully!",
        "document": deleted_document
    }

