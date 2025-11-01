from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag_pipeline import SystemDesignRAG

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow your Next.js frontend
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)
rag = SystemDesignRAG()

class Query(BaseModel):
    question: str

@app.post("/design")
async def design(q: Query):
    answer = rag.generate(q.question)
    return {"answer": answer}

