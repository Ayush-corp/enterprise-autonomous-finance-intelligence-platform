from memory.vector_store import get_db

db = get_db()

def save_memory(stock, text):
    db.add_texts(
        texts=[text],
        metadatas=[{"stock": stock}]
    )

def retrieve_memory(query):
    return db.similarity_search(query, k=3)