from fastapi import APIRouter

from app.services.retriever_service import RetrieverService

router = APIRouter()

@router.get(
    path="/",
    tags=["Retriever"],
    description="Search the knowledge base for documents")
async def search(api_key: str, collection_name: str, query: str, k: int = 5):
    result = await RetrieverService.search(
        api_key=api_key,
        collection_name=collection_name,
        query=query,
        k=k)
    return {"result": result}
