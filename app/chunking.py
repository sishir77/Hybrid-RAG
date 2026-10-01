from open_pdf import parsed_document
from langchain_text_splitters import MarkdownTextSplitter

splitter = MarkdownTextSplitter(chunk_size=300, chunk_overlap=50)

chunks = splitter.split_text(parsed_document)

chunk_id = 0
for chunk in chunks:
    chunk_id += 1
    chunks.append({
        "id": chunk_id,
        "text":chunk,
        "document": "quantum computing.pdf"  #this is for the testing, we change it on production.

    })

print(chunks)






