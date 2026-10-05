from open_pdf import result, tables
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
chunked_documents = []
chunked_id=0

#detect markdown table
"""def is_table_line(line):
    return line.strip().startswith("|") and line.strip().endswith("|")"""

#extract table from normal text
"""def extract_table(text):
    lines = text.splitlines()
    tables =[]
    normal_lines= []

    current_table = []

    for line in lines:
        if is_table_line(line):
            current_table.append(line)

        else:
            if current_table:
                tables.append("\n".join(current_table))
                current_table =[]

            normal_lines.append(line)

    #handles last line if it is a table
    if current_table:
        tables.append("\n".join(current_table))

    normal_text = "\n".join(normal_lines)
    return normal_text, tables"""

#for normal text
for section in sections:
   # normal_text, tables = extract_table(section.page_content)

    #split the normal text into smaller chunks
    if section.page_content.strip():
        normal_chunks = section_splitter.split_text(section.page_content)
        for chunk in  normal_chunks:
            chunked_id +=1
            chunked_documents.append({
                "id": chunked_id,
                "text":chunk,
                "document":"...",
                "metadata": {
                    **section.metadata,
                    "type": "text"
                }
            })

#for table
for table in tables:
    table_metadata={}
    for section in sections:
        if table in section.page_content:
            table_metadata= section.metadata
            break
    chunked_id+=1
    chunked_documents.append({
        "id":chunked_id,
        "text":table,
        "document":"...",
        "metadata":{
            **table_metadata,
            "type":"table"
        }
    })


if __name__ == "__main__":
    for doc in chunked_documents:
        print("=" * 80)

        print("ID:", doc["id"])
        print("TYPE:", doc["metadata"]["type"])
        print("SECTION:", doc["metadata"])

        print("\nTEXT:")
        print(doc["text"])


 









