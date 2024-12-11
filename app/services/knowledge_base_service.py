from typing import List
from langchain_core.documents import Document

from app.utils.vector_store import VectorStore


class KnowledgeBaseService:

    @classmethod
    def add_document(cls):
        pass

    @classmethod
    def remove_document(cls):
        pass

    @classmethod
    def add_collection(cls, api_key: str, collection_name: str, documents: [Document]):
        store = VectorStore.get_vector_store(
            api_key=api_key,
            collection_name=collection_name)
        store.add_documents(documents, ids=[doc.metadata["id"] for doc in documents])

    @classmethod
    def remove_collection(cls):
        pass

