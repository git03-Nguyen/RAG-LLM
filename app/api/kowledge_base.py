from fastapi import APIRouter
from langchain_core.documents import Document

from app.services.knowledge_base_service import KnowledgeBaseService

router = APIRouter()

@router.post(
    path="/add_collection",
    tags=["Knowledge Base"],
    description="Add a collection of documents to the knowledge base")
def add_collection(api_key: str):
    docs = [
        Document(
            page_content="there are cats in the pond",
            metadata={"id": 1, "location": "pond", "topic": "animals"},
        ),
        Document(
            page_content="ducks are also found in the pond",
            metadata={"id": 2, "location": "pond", "topic": "animals"},
        ),
        Document(
            page_content="fresh apples are available at the market",
            metadata={"id": 3, "location": "market", "topic": "food"},
        ),
        Document(
            page_content="the market also sells fresh oranges",
            metadata={"id": 4, "location": "market", "topic": "food"},
        ),
        Document(
            page_content="the new art exhibit is fascinating",
            metadata={"id": 5, "location": "museum", "topic": "art"},
        ),
        Document(
            page_content="a sculpture exhibit is also at the museum",
            metadata={"id": 6, "location": "museum", "topic": "art"},
        ),
        Document(
            page_content="a new coffee shop opened on Main Street",
            metadata={"id": 7, "location": "Main Street", "topic": "food"},
        ),
        Document(
            page_content="the book club meets at the library",
            metadata={"id": 8, "location": "library", "topic": "reading"},
        ),
        Document(
            page_content="the library hosts a weekly story time for kids",
            metadata={"id": 9, "location": "library", "topic": "reading"},
        ),
        Document(
            page_content="a cooking class for beginners is offered at the community center",
            metadata={"id": 10, "location": "community center", "topic": "classes"},
        ),
    ]

    KnowledgeBaseService.add_collection(
        api_key=api_key,
        collection_name="Test",
        documents=docs)

    return {"message": "Collection added successfully"}
