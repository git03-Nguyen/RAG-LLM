import structlog
from fastapi import APIRouter

from app.models.response_model import ErrorResponse, RAGResponse
from app.services.rag_service import ask_question

logger = structlog.get_logger(__name__)
router = APIRouter()

@router.post(
    path="/",
    tags=["RAG"],
    description="Ask question related to the knowledge base")
async def chat(
        google_api_key:str,
        collection_name: str,
        query: str
):
    try:
        result = await ask_question(
            api_key=google_api_key,
            collection_name=collection_name,
            question=query
        )
        return RAGResponse(
            status=200,
            data={"result": result}
        )
    except Exception as e:
        logger.error("Error asking question", exc_info=e)
        return ErrorResponse(
            status=500,
            detail="Call retriever service failed"
        )