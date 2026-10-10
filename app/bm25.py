from chunking import chunked_documents
from rank_bm25 import BM25Okapi


documents = [chunk['text']  for chunk in chunked_documents]

tokenize_documents = [document.split() for document in documents]

splitted_store = BM25Okapi(tokenize_documents)

def bm25_search(question, k=3):
    tokenize_query = question.split()

    scores = splitted_store.get_scores(tokenize_query)

    ranked_indices= sorted(
        range(len(scores)),
        key= lambda i:  scores[i],
        reverse= True
    )[:k]
    results=[]

    for index in ranked_indices:
        results.append({
            "id": chunked_documents[index]["id"],
            "text": chunked_documents[index]['text'],
            "metadata": chunked_documents[index]['metadata'],
            'score': float(scores[index])
        })

    return results

if __name__ == "__main__":
    question = "What are opportunities and risks in encryption?"

    results = bm25_search(question, k=3)

    for result in results:
        print("ID:", result["id"])
        print("Score:", result["score"])
        print("Text:", result["text"])
        print("-" * 50)









