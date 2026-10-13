from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.hybrid_retrieval import hybrid_search
from app.llm import generate_answer



app = FastAPI()


@app.get("/")
def home():
    return("welcome to homepage of hybrid rag")

class question_request(BaseModel):
    question :str


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
    results = hybrid_search(request.question, k=3)

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

