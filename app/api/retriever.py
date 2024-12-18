from sys import exc_info

import structlog
from fastapi import APIRouter

from app.models.response_model import UserResponse, ErrorResponse
from app.services.retriever_service import RetrieverService

logger = structlog.getLogger(__name__)
router = APIRouter()

@router.get(
    path="/",
    tags=["Retriever"],
    description="Search the knowledge base for documents")
async def search(
        google_api_key: str,
        collection_name: str,
        query: str,
        k: int):
    try:
        result = await RetrieverService.search(
            api_key=google_api_key,
            collection_name=collection_name,
            query=query,
            k=k)

        ids = [doc.id for doc in result]
        return UserResponse(
            status=200,
            data={"result": ids}
        )
    except Exception as e:
        logger.error(f"Error searching collection: {collection_name} "
                     f"with query: {query}", exc_info=e)
        return ErrorResponse(
            status=500,
            detail="Error searching collection"
        )