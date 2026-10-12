from database import collection
from sentence_transformers import SentenceTransformer



model = SentenceTransformer('all-MiniLM-L6-v2')


def similarity_search(query, k=3):
    question_embeddings = model.encode(query).tolist()

    results = collection.query(
        query_embeddings = [question_embeddings],
        n_results = k
    )
    top_chunks=[]

    for i in range(len(results["ids"][0])):
        top_chunks.append({
            "id": results["ids"][0][i],
            "text": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "distance": results["distances"][0][i]



        })


    return top_chunks

if __name__ == "__main__":
    question = "What are opportunities and risks in encryption?"
    results = similarity_search(question)
    print(results)
    


        



