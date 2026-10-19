from app.database import collection
from sentence_transformers import SentenceTransformer



model = SentenceTransformer('all-MiniLM-L6-v2')


def similarity_search(query, document_id,k=3):
    question_embeddings = model.encode(query).tolist()

    results = collection.query(
        query_embeddings = [question_embeddings],
        n_results = k,
        where={'document_id': document_id}
    )
    top_chunks=[]

    for i in range(len(results["ids"][0])):
        top_chunks.append({
            "id": results["ids"][0][i],
            "text": results["documents"][0][i],
            "metadata": results["metadatas"][0][i]
            



        })


    return top_chunks

if __name__ == "__main__":
    question = "What are the reponsibilities of Sishir gautam?"
    results = similarity_search(question, document_id="your_document_id", k=3)
    print(results)
    


        



