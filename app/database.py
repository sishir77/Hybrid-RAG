from embeddings import embedded_chunks
import chromadb

client = chromadb.PersistentClient(path="app/chromadb")
collection = client.get_or_create_collection("data")

for chunk in embedded_chunks:
    collection.add(
        ids=[str(chunk['id'])],
        metadatas=[chunk['metadata']],
        documents=[chunk['text']],
        embeddings=[chunk['embedding']]
    )

if __name__ == "__main__":
    print(collection)
    print("Total record:", collection.count())