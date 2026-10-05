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
    question = "What is quantum computing?"
    results = similarity_search(question)
    print(results)
        



