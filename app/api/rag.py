from fastapi import APIRouter

from app.services.rag_service import ask_question
from app.services.retriever_service import RetrieverService

router = APIRouter()

@router.post(
    path="/",
    tags=["RAG"],
    description="Ask question related to the knowledge base")
async def chat(api_key: str, collection_name: str, query: str):
    result = await ask_question(
        api_key=api_key,
        collection_name=collection_name,
        question=query
    )
    return {"result": result}
