import structlog
from fastapi import APIRouter

from app.models.response_model import ErrorResponse
from app.services.knowledge_base_service import KnowledgeBaseService
from app.services.tmdb_service import TMDBService
from app.utils.decode_jwt import decode_jwt
from app.utils.transform_document import transform_document

logger = structlog.get_logger(__name__)
router = APIRouter()

async def logic_sync(tmdb_service: TMDBService, google_api_key: str):
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
    return {
        "status": 200,
        "message": "Synced successfully"
    }

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

    tmdb_service = TMDBService()

    try:
        return await logic_sync(tmdb_service, google_api_key)
    except Exception as e:
        tmdb_service.raise_error_sync()
        logger.error("Error syncing knowledge base", exc_info=e)
        return ErrorResponse(
            status=500,
            detail="Error syncing knowledge base"
        )

@router.post(path="/sync-with-auto-retry",
    tags=["Knowledge Base"],
    description="Sync the knowledge base with the mongodb database with auto retry")
async def sync_with_auto_retry(google_api_key: str, token: str, retry_count: int = 0, max_retries: int = 50):
    print(f"Syncing knowledge base (Attempt {retry_count + 1})")
    payload = decode_jwt(token)
    if payload.get("role") != "admin":
        return ErrorResponse(
            status=403,
            detail="Access denied"
        )

    tmdb_service = TMDBService()

    try:
        return await logic_sync(tmdb_service, google_api_key)
    except Exception as e:
        tmdb_service.raise_error_sync()
        logger.error(f"Error syncing knowledge base (Attempt {retry_count + 1})", exc_info=e)

        # Retry logic
        if retry_count < max_retries:
            return sync_with_auto_retry(google_api_key, token, retry_count=retry_count + 1, max_retries=max_retries)
        else:
            return ErrorResponse(
                status=500,
                detail="Error syncing knowledge base after multiple attempts"
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
        return {
            "status": 200,
            "message": "All collections dropped successfully"
        }
    except Exception as e:
        logger.error("Error dropping knowledge base", exc_info=e)
        return ErrorResponse(
            status=500,
            detail="Error dropping knowledge base"
        )