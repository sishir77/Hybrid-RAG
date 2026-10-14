
import chromadb

client = chromadb.PersistentClient(path="app/chromadb")
collection = client.get_or_create_collection("data")


def store_embeddings(embedded_chunks):
    for chunk in embedded_chunks:
        collection.upsert(
            ids= [str(chunk['id'])],
            metadatas= [chunk['metadata']],
            documents =  [chunk['text']],
            embeddings= [chunk['embedding']]
        )

    return collection


if __name__ == "__main__":
    print(collection)
    print("Total record:", collection.count())