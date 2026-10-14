
from app.open_pdf import parse_file
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    MarkdownHeaderTextSplitter
)


def create_chunks(file_path):
    # Parse the PDF
    result, tables = parse_file(file_path)

    # Split Markdown by headings
    headers = [
        ("#", "h1"),
        ("##", "h2"),
        ("###", "h3"),
        ("####", "h4")
    ]

    splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=headers
    )
    sections = splitter.split_text(result)

    # Split sections into smaller chunks
    section_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        separators=["\n\n", "\n", " ", ""]
    )

    chunked_documents = []
    chunked_id = 0

    # Chunk normal text
    for section in sections:
        if section.page_content.strip():
            normal_chunks = section_splitter.split_text(
                section.page_content
            )

            for chunk in normal_chunks:
                chunked_id += 1
                chunked_documents.append({
                    "id": chunked_id,
                    "text": chunk,
                    "document": file_path,
                    "metadata": {
                        **section.metadata,
                        "type": "text"
                    }
                })

    # Add extracted tables
    for table in tables:
        table_metadata = {}

        for section in sections:
            if table in section.page_content:
                table_metadata = section.metadata
                break

        chunked_id += 1
        chunked_documents.append({
            "id": chunked_id,
            "text": table,
            "document": file_path,
            "metadata": {
                **table_metadata,
                "type": "table"
            }
        })

    return chunked_documents


if __name__ == "__main__":
    chunks = create_chunks("Quantum computing.pdf")

    print("Total chunks:", len(chunks))

    for doc in chunks:
        print("=" * 80)
        print("ID:", doc["id"])
        print("TYPE:", doc["metadata"]["type"])
        print("SECTION:", doc["metadata"])
        print("\nTEXT:")
        print(doc["text"])
