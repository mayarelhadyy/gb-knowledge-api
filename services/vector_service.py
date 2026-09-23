import chromadb
import uuid

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(
    name = "gb_documents",
)

def store_chunks(chunks, embeddings, filename):

    ids = []
    metadatas = []

    for index in range(len(chunks)):

        ids.append(str(uuid.uuid4()))

        metadatas.append({
            "filename": filename,
            "chunk_index": index
        })

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings.tolist(),
        metadatas=metadatas
    )

    return len(chunks)

def search_chunks(query_embedding, top_k=10):

    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=top_k
    )

    return results

def is_retrieval_relevant(
    results,
    max_distance=1.4
):
    if not results["documents"][0]:
        return False

    best_distance = results["distances"][0][0]

    return best_distance <= max_distance

def get_stored_documents():
    """
    Return unique PDF documents currently
    stored in the Chroma knowledge base.
    """

    data = collection.get(
        include=["metadatas"]
    )

    metadatas = data.get(
        "metadatas",
        []
    )

    filenames = set()

    for metadata in metadatas:
        if metadata:
            filename = metadata.get(
                "filename"
            )

            if filename:
                filenames.add(filename)

    documents = [
        {
            "name": filename
        }
        for filename in sorted(filenames)
    ]

    return documents

def delete_document_chunks(filename: str):
    """
    Delete all chunks that belong
    to a specific PDF document.
    """

    collection.delete(
        where={
            "filename": filename
        }
    )