from sentence_transformers import SentenceTransformer
from app.chunking import create_chunks

model = SentenceTransformer('all-MiniLM-L6-v2')

def create_embeddings(chunks):
   embedded_chunks = []

   for chunk in chunks:
    embedding = model.encode(chunk["text"]).tolist()

    embedded_chunks.append({
        "id": chunk["id"],
        "text": chunk["text"],
        "metadata": chunk["metadata"],
        "embedding": embedding
    })

   return embedded_chunks


if __name__ == "__main__":
    chunks = create_chunks("Quantum computing.pdf")
    embeddings = create_embeddings(chunks)
    print("Total embedded chunks:", len(embeddings))