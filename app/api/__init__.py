from fastapi import APIRouter
from app.api.kowledge_base import router as knowledge_base_router
from app.api.retriever import router as retriever_router
from app.api.create_token import router as create_token_router

router = APIRouter()

router.include_router(
    knowledge_base_router,
    prefix="/knowledge_base",
    tags=["Knowledge Base"]
)

router.include_router(
    retriever_router,
    prefix="/retriever",
    tags=["Retriever"]
)

router.include_router(
    create_token_router,
    prefix="/create_token",
    tags=["Token"]
)