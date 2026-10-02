from docling.document_converter import DocumentConverter

converter = DocumentConverter()

parsed_document = converter.convert("Quantum computing.pdf")
result = parsed_document.document.export_to_markdown()


if __name__=="__main__":
    print(result)

