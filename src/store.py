from sentence_transformers import SentenceTransformer
import chromadb

def store_chunks(chunks, db_path="codebase_db"):
    """Store code chunks as embeddings in a vector DB."""
    model = SentenceTransformer("all-MiniLM-L6-v2")
    client = chromadb.PersistentClient(path=db_path)
    collection = client.get_or_create_collection("codebase")

    for chunk in chunks:
        embedding = model.encode(chunk["content"]).tolist()
        collection.add(
            ids=[f"{chunk['file']}_{chunk['chunk_id']}"],
            embeddings=[embedding],
            metadatas=[{"file": chunk["file"], "content": chunk["content"]}]
        )
    return collection

def retrieve_context(query, collection, top_k=5):
    """Retrieve relevant chunks based on a query."""
    model = SentenceTransformer("all-MiniLM-L6-v2")
    query_embedding = model.encode(query).tolist()
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)
    return [meta["content"] for meta in results["metadatas"][0]]
