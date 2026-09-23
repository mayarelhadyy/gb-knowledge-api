from services.embedding_service import create_query_embedding
from services.vector_service import search_chunks


test_questions = [
    # Relevant questions
    "What are the rules for working from home?",
    "What happens if an employee is repeatedly late?",
    "How should confidential information be handled?",
    "What types of leave are available?",
    "How can an employee report a workplace concern?",
    "What happens if an employee violates company policy?",

    # Irrelevant questions
    "Who won the World Cup?",
    "How do I cook pasta?",
    "What is the capital of Japan?",
    "How does Bitcoin mining work?",
    "What is machine learning?",
    "How do I repair a car engine?"
]


for question in test_questions:

    query_embedding = create_query_embedding(
        question
    )

    results = search_chunks(
        query_embedding,
        top_k=3
    )

    print("\n" + "=" * 70)
    print("QUESTION:", question)
    print("=" * 70)

    for i in range(len(results["documents"][0])):

        distance = results["distances"][0][i]
        metadata = results["metadatas"][0][i]
        text = results["documents"][0][i]

        print(
            f"\nRank #{i + 1}"
            f"\nDistance: {distance:.4f}"
            f"\nChunk: {metadata['chunk_index']}"
            f"\n{text[:200]}"
        )