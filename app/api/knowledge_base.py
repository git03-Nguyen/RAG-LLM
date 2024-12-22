import structlog
from fastapi import APIRouter, HTTPException
from langchain_core.documents import Document

from app.models.response_model import ErrorResponse
from app.services.knowledge_base_service import KnowledgeBaseService
from app.services.tmdb_service import TMDBService
from app.utils.decode_jwt import decode_jwt
from app.utils.transform_document import transform_document

logger = structlog.get_logger(__name__)
router = APIRouter()

@router.post(
    path="/sync",
    tags=["Knowledge Base"],
    description="Sync the knowledge base with the mongodb database")
async def sync(google_api_key: str, token: str):
    print("Syncing knowledge base")
    payload = decode_jwt(token)
    if payload.get("role") != "admin":
        return ErrorResponse(
            status=403,
            detail="Access denied"
        )

    try:
        tmdb_service = TMDBService()
        tmdb_service.connect()

        # Stream data in batches from all collections
        batch_size = 200
        for collection_name, batch in tmdb_service.stream_all_collections_data(batch_size=batch_size):
            print(f"\nCollection: {collection_name}")
            print(f"Batch size: {len(batch)}")
            documents = [transform_document(doc) for doc in batch]
            await KnowledgeBaseService.add_collection(
                api_key=google_api_key,
                collection_name=collection_name,
                documents=documents
            )

        tmdb_service.close()
        print("Synced successfully")
        return {"message": "Synced successfully"}
    except Exception as e:
        logger.error("Error syncing knowledge base", exc_info=e)
        return ErrorResponse(
            status=500,
            detail="Error syncing knowledge base"
        )

@router.post(
    path="/drop",
    tags=["Knowledge Base"],
    description="Drop the knowledge base")
async def drop(google_api_key: str, token: str):
    payload = decode_jwt(token)
    if payload.get("role") != "admin":
        return ErrorResponse(
            status=403,
            detail="Access denied"
        )

    try:
        tmdb_service = TMDBService()
        tmdb_service.connect()
        collection_names = tmdb_service.list_collections()

        for collection_name in collection_names:
            print("Dropping collection:", collection_name)
            await KnowledgeBaseService.delete_collection(
                api_key=google_api_key,
                collection_name=collection_name
            )

        tmdb_service.close()
        return {"message": "All collections dropped successfully"}
    except Exception as e:
        logger.error("Error dropping knowledge base", exc_info=e)
        return ErrorResponse(
            status=500,
            detail="Error dropping knowledge base"
        )