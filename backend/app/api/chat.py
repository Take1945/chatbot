from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.core.dependencies import get_llm, get_vector_store
from app.core.state import RAGState

router = APIRouter(prefix="/api", tags=["chat"])

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str
    sources: list[dict]

def get_rag_service(
    vector_store=Depends(get_vector_store),
    llm=Depends(get_llm),
) -> RAGState:
    return RAGState(vector_store=vector_store, llm=llm)

@router.post("/chat", response_model=ChatResponse)
async def chat(body: ChatRequest, rag: RAGState = Depends(get_rag_service)):
    result = await rag.ask_async(body.question)
    return ChatResponse(answer=result["answer"], sources=result["sources"])