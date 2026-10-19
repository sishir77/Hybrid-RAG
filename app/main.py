from fastapi import FastAPI, HTTPException, File, UploadFile
from pydantic import BaseModel
from app.hybrid_retrieval import hybrid_search
from app.llm import generate_answer
import shutil
import os
import uuid
from app.embeddings import create_embeddings
from app.database import store_embeddings
from app.chunking import create_chunks



app = FastAPI()


@app.get("/")
def home():
    return("welcome to homepage of hybrid rag")

UPLOAD_DIR = "app/uploads"

os.makedirs(UPLOAD_DIR, exist_ok= True)

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    # Give each upload unique chunk IDs
    upload_id = uuid.uuid4().hex[:12]

    file_path = os.path.join(
           UPLOAD_DIR,
          f"{upload_id}_{os.path.basename(file.filename)}"
          )
    
    with open(file_path, "wb") as buffer:
     shutil.copyfileobj(file.file, buffer)


    chunks = create_chunks(file_path)
    

    for chunk in chunks:
       chunk["id"] = f"{upload_id}_{chunk['id']}"
       chunk['metadata']['document_id']= upload_id

    # Convert chunks into embeddings
    embedded_chunks = create_embeddings(chunks)

    # Save chunks and embeddings in ChromaDB
    store_embeddings(embedded_chunks)
    return {
     "message": "PDF uploaded, chunked, embedded, and stored successfully",
     "filename": file.filename,
     "document_id": upload_id,
     "total_chunks": len(chunks) 
     
   }


class question_request(BaseModel):
    question :str
    document_id:str


class SourceResponse(BaseModel):
    chunk_id: int | str
    section: str | None = None
    text: str


class AnswerResponse(BaseModel):
    question: str
    answer: str
    sources: list[SourceResponse]

@app.post("/ask", response_model=AnswerResponse)
def ask_question(request:question_request):
    results = hybrid_search(request.question, request.document_id,k=3)

    if not results:
        raise HTTPException(
            status_code=404,
            detail="No relevant information was found."
        )

    # 2. Combine retrieved chunk text into context
    context = "\n\n".join(
        f"Source {i + 1}:\n{chunk['text']}"
        for i, chunk in enumerate(results)
    )

    # 3. Generate an answer using Groq
    try:
        answer = generate_answer(
            question=request.question,
            context=context
        )
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail="Failed to generate an answer with the LLM."
        ) from exc
    sources = [
    {
        "chunk_id": chunk["id"],
        "section": chunk.get("metadata", {}).get("h2"),
        "text": chunk["text"],
    }
    for chunk in results
]

    # 4. Return the answer and source chunks
    return {
        "question": request.question,
        "answer": answer,
        "sources": sources
    }

