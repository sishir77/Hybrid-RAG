from open_pdf import result
from langchain_text_splitters import MarkdownTextSplitter,RecursiveCharacterTextSplitter,MarkdownHeaderTextSplitter

#split the text into sections based on the headers
headers =[
   ("#", "h1"),
   ("##", "h2"),
   ("###", "h3"),
   ("####", "h4")
]
splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers)
sections = splitter.split_text(result)


#split the splitted sections by header into smaller chunks of text based on separators with chunk size.
section_splitter = RecursiveCharacterTextSplitter(
   chunk_size=500,
   chunk_overlap=100,
   separators=["\n\n", "\n", " ", ""]
)

chunks = section_splitter.split_documents(sections)

chunk_documents = []
chunk_id = 0
for chunk in chunks:
    chunk_id += 1
    chunk_documents.append({
        "id": chunk_id,
        "text":chunk.document,
        "metadata": chunk.metadata,
        "document": "quantum computing.pdf"  #this is for the testing, we change it on production.
    })


if __name__=="__main__":
  for chunk in chunk_documents:
     print(chunk)
     print()







