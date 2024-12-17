from fastapi import APIRouter, HTTPException
from langchain_core.documents import Document

from app.services.knowledge_base_service import KnowledgeBaseService
from app.services.tmdb_service import TMDBService
from app.utils.decode_jwt import decode_jwt
from app.utils.transform_document import transform_document

router = APIRouter()

@router.post(
    path="/add_test_collection",
    tags=["Knowledge Base"],
    description="Add a test collection of documents to the knowledge base")
def add_collection(api_key: str, token: str):
    payload = decode_jwt(token)
    if payload.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Access denied")

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

@router.post(
    path="/sync",
    tags=["Knowledge Base"],
    description="Sync the knowledge base with the mongodb database")
async def sync(api_key: str, token: str):
    payload = decode_jwt(token)
    if payload.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Access denied")

    tmdb_service = TMDBService()
    tmdb_service.connect()

    # Stream data in batches from all collections
    batch_size = 200
    for collection_name, batch in tmdb_service.stream_all_collections_data(batch_size=batch_size):
        print(f"\nCollection: {collection_name}")
        print(f"Batch size: {len(batch)}")
        documents = [transform_document(doc) for doc in batch]
        await KnowledgeBaseService.add_collection(
            api_key=api_key,
            collection_name=collection_name,
            documents=documents
        )

    tmdb_service.close()
    return {"message": "Synced successfully"}

@router.post(
    path="/drop",
    tags=["Knowledge Base"],
    description="Drop the knowledge base")
async def drop(api_key: str, token: str):
    payload = decode_jwt(token)
    if payload.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Access denied")

    tmdb_service = TMDBService()
    tmdb_service.connect()
    collection_names = tmdb_service.list_collections()

    for collection_name in collection_names:
        print("Dropping collection:", collection_name)
        await KnowledgeBaseService.delete_collection(
            api_key=api_key,
            collection_name=collection_name
        )

    tmdb_service.close()
    return {"message": "All collections dropped successfully"}





