from docling.document_converter import DocumentConverter



def parse_file(file_path):
    converter= DocumentConverter()

    parsed_document = converter.convert(file_path)
    document = parsed_document.document

    result = document.export_to_markdown()

    tables=[]
    for table in document.tables:
       tables.append(table.export_to_markdown(doc=document))

    return result, tables

if __name__=="__main__":
    result, tables = parse_file("Quantum computing.pdf")



    print("Number of tables:", len(tables) )
    for table in tables:
        print(table)
        
    print(result)
