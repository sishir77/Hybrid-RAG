from docling.document_converter import DocumentConverter


converter = DocumentConverter()

parsed_document = converter.convert("Quantum computing.pdf")

print(parsed_document.document.export_to_markdown())


