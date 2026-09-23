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
from services.llm_service import generate_answer
from services.output_guardrail_service import validate_answer


FALLBACK_ANSWER = (
    "The provided documents do not contain enough "
    "information to answer this question."
)


def generate_rag_answer(question: str):

    # 1. Create query embedding
    query_embedding = create_query_embedding(
        question
    )

    # 2. Retrieve relevant chunks
    results = search_chunks(
        query_embedding,
        top_k=3
    )

    # 3. Retrieval guardrail
    if not is_retrieval_relevant(results):
        return FALLBACK_ANSWER

    # 4. Format retrieved results
    formatted_results = []

    for i in range(len(results["documents"][0])):

        formatted_results.append({
            "text": results["documents"][0][i],
            "source": results["metadatas"][0][i]["filename"],
            "chunk_index": results["metadatas"][0][i]["chunk_index"],
            "distance": results["distances"][0][i]
        })

    # 5. Build context
    context = build_context(
        formatted_results
    )

    # 6. Build LLM user message
    user_message = build_user_message(
        question,
        context
    )

    # 7. Generate answer
    answer = generate_answer(
        SYSTEM_PROMPT,
        user_message
    )

    # 8. Output guardrail
    is_supported = validate_answer(
        answer,
        context
    )

    if not is_supported:
        return (
            "The generated answer could not be fully "
            "verified against the provided documents."
        )

    return answer