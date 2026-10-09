from database import collection
from sentence_transformers import SentenceTransformer



model = SentenceTransformer('all-MiniLM-L6-v2')


def similarity_search(query, k=3):
    question_embeddings = model.encode(query).tolist()

    results = collection.query(
        query_embeddings = [question_embeddings],
        n_results = k
    )

    return results

if __name__ == "__main__":
    question = "What are opportunities and risks in encryption?"
    results = similarity_search(question)
    for i in range(3):
        print("ID:", results['ids'][0][i])
        print("Metadata:", results['metadatas'][0][i])
        print("Document:", results['documents'][0][i])
        print("distance:", results['distances'][0][i])
        print("=" *80)
    


        



