from fastapi import APIRouter, Depends

from dependencies import require_hr
from models import SearchRequest
from services.embedding_service import create_query_embedding
from services.vector_service import (
    search_chunks,
    is_retrieval_relevant
)
from services.context_service import build_context
from services.prompt_service import (
    SYSTEM_PROMPT,
    build_user_message
)
from services.output_guardrail_service import validate_answer
from services.llm_service import generate_answer

router = APIRouter(
    prefix="/search",
    tags=["Search"],
    dependencies=[
        Depends(require_hr)
    ]
)

@router.post("/")
def search_documents(request: SearchRequest):

    query_embedding = create_query_embedding(
        request.question
    )

    results = search_chunks(
        query_embedding,
        top_k=3
    )
    if not is_retrieval_relevant(results):
        return {
            "answer": (
                "The provided documents do not contain enough "
                "information to answer this question."
            )
        }

    formatted_results = []

    for i in range(len(results["documents"][0])):

        formatted_results.append({
            "text": results["documents"][0][i],
            "source": results["metadatas"][0][i]["filename"],
            "chunk_index": results["metadatas"][0][i]["chunk_index"],
            "distance": results["distances"][0][i]
        })

    context = build_context(
        formatted_results
    )

    user_message = build_user_message(
    request.question,
    context
)

    answer = generate_answer(
        SYSTEM_PROMPT,
        user_message
    )

    is_supported = validate_answer(
    answer,
    context
)

    if not is_supported:
        answer = (
            "The generated answer could not be fully verified "
            "against the provided documents."
        )

    return {
    "answer": answer
}