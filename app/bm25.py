from chunking import chunked_documents
from rank_bm25 import BM25Okapi


documents = [chunk['text']  for chunk in chunked_documents]

tokenize_documents = [document.split() for document in documents]

bm25 = BM25Okapi(tokenize_documents)

print(bm25)

