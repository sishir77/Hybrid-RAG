from docling.document_converter import DocumentConverter

converter = DocumentConverter()

parsed_document = converter.convert("Quantum computing.pdf")
document = parsed_document.document
result = document.export_to_markdown()

tables=[]
for table in document.tables:
    tables.append(table.export_to_markdown(doc=document))

if __name__=="__main__":
       print("Number of tables:", len(document.tables))

       for table in tables:
        print(table.export_to_markdown())
        
       print(result)
