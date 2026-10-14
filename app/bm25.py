from rank_bm25 import BM25Okapi
from app.database import collection


def bm25_search(question, top_k=5):
    stored_data = collection.get(include=["documents", "metadatas"])

    documents = stored_data["documents"]
    ids = stored_data["ids"]
    metadatas = stored_data["metadatas"]

    if not documents:
        return []

    tokenized_documents = [
        document.lower().split()
        for document in documents
    ]

    bm25 = BM25Okapi(tokenized_documents)
    scores = bm25.get_scores(question.lower().split())

    ranked_indices = sorted(
        range(len(scores)),
        key=lambda index: scores[index],
        reverse=True
    )[:top_k]

    results = []

    for index in ranked_indices:
        results.append({
            "id": ids[index],
            "text": documents[index],
            "metadata": metadatas[index],
            "score": float(scores[index])
        })

    return results