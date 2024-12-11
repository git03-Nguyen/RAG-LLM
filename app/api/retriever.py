from fastapi import APIRouter
from langchain_core.documents import Document

from app.services.knowledge_base_service import KnowledgeBaseService
from app.services.retriever_service import RetrieverService

router = APIRouter()

@router.get(
    path="/",
    tags=["Retriever"],
    description="Search the knowledge base for documents")
def search(api_key: str, collection_name: str, query: str, k: int = 5):
    result = RetrieverService.search(
        api_key=api_key,
        collection_name=collection_name,
        query=query,
        k=k)
    return {"result": result}
