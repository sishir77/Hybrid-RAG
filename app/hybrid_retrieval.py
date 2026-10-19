from app.retrieval import similarity_search
from app.bm25 import bm25_search


def reciprocal_rank_fusion(result_list, rank_constant=60, top_k=5):
    fused_scores={}
    chunk_data={}

    for results in result_list:
        for rank, chunk in enumerate(results, start=1):
            chunk_id = str(chunk['id'])

            #store the chunk details
            chunk_data[chunk_id]= chunk

            #add its reciprocal rank contribution
            score = 1 / (rank_constant+rank)

            fused_scores[chunk_id]= (
                fused_scores.get(chunk_id, 0)+score
                )
            
    # Sort chunks by their combined RRF scores
    ranked_ids = sorted(
        fused_scores,
        key=lambda chunk_id: fused_scores[chunk_id],
        reverse=True
    )

    final_results = []

    for chunk_id in ranked_ids[:top_k]:
       # print("Ranked IDs:", ranked_ids)
       # print("Stored IDs:", list(chunk_data.keys()))
        chunk = chunk_data[chunk_id].copy()
        chunk["rrf_score"] = fused_scores[chunk_id]
        final_results.append(chunk)

    return final_results


def hybrid_search(question,document_id, k=5):
    semantic_results = similarity_search(question, document_id=document_id, k=k)
    bm25_results =  bm25_search(question,document_id=document_id, top_k=k)

    #print("Semantic IDs:", [r["id"] for r in semantic_results])
    #print("BM25 IDs:", [r["id"] for r in bm25_results])
    """ print("\n--- SEMANTIC SEARCH ---")
    for rank, chunk in enumerate(semantic_results, start=1):
        print(f"Rank: {rank} | ID: {chunk['id']}")

    print("\n--- BM25 SEARCH ---")
    for rank, chunk in enumerate(bm25_results, start=1):
        print(f"Rank: {rank} | ID: {chunk['id']}")"""
    

    fused_results= reciprocal_rank_fusion(
        [semantic_results, bm25_results],
        top_k=k
    )
      # Temporarily inspect the final hybrid ranking
    """ print("\n--- FINAL HYBRID RESULTS ---")
    for result in fused_results:
        print(
            f"ID: {result['id']} | "
            f"RRF: {result['rrf_score']:.6f}"
        )"""

    return fused_results




if __name__ == "__main__":
    question = "What are opportunities and risks in encryption?"

    results = hybrid_search(question, k=5)

    for result in results:
        print("ID:", result["id"])
        print("RRF Score:", result["rrf_score"])
        print("Text:", result["text"])
        print("-" * 60)
         





