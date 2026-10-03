from sentence_transformers import SentenceTransformer
from chunking import chunked_documents

model = SentenceTransformer('all-MiniLM-l6-v2')


embedded_chunks=[]

for chunk in chunked_documents:
    embedding = model.encode(chunk["text"])
    embedded_chunks.append({
        "id": chunk['id'],
        "metadata": chunk['metadata'],
        "text": chunk['text'],
        "embedding": embedding
    })

if __name__ =="__main__":
    print(len(embedded_chunks[0]['embedding']))
    for embed in embedded_chunks: 
     print("="*80)
     print(embed['id'], embed['metadata'], embed['text'][:50], embed['embedding'][:5])