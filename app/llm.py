import os
from groq import Groq
from dotenv import load_dotenv
from pathlib import Path




PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = PROJECT_ROOT / ".env"

load_dotenv(ENV_FILE, override=True)



api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY is missing from the .env file")

client = Groq(api_key=api_key)

def generate_answer(question: str, context: str) -> str:
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": (
                    " You are a precise question-answering assistant. "
                    "Answer the user's question using the provided context. "
                    "Preserve the technical meaning of the source material. "
                    "Do not introduce unsupported facts or claim that one "
                    "algorithm solves a different problem. "
                    "If the context is insufficient, say so clearly."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Context:\n{context}\n\n"
                    f"Question:\n{question}"
                ),
            },
        ],
        temperature=0.2,
        max_tokens=700,
    )

    return response.choices[0].message.content or ""





