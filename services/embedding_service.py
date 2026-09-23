from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def create_embeddings(chunks):
    embeddings = embedding_model.encode(chunks)
    return embeddings


def create_query_embedding(question: str):
    embedding = embedding_model.encode(question)
    return embedding
