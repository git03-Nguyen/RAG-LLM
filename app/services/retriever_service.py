from langchain_core.documents import Document

from app.utils.vector_store import VectorStore


class RetrieverService:
    @classmethod
    async def search(cls, api_key:str, collection_name: str, query: str, k: int = 5) -> [Document]:
        store = VectorStore.get_vector_store(
            api_key=api_key,
            collection_name=collection_name)
        retriever = store.as_retriever(search_type="mmr", search_kwargs={"k": k})
        return await retriever.ainvoke(query)
