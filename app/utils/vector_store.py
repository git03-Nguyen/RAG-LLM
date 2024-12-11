import os
from langchain_postgres.vectorstores import PGVector
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from pydantic import SecretStr


class VectorStore:
    _connection = (f"postgresql+psycopg://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
                f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}")


    @classmethod
    def get_vector_store(cls, api_key: str, collection_name: str) -> PGVector:
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/text-embedding-004",
            google_api_key=SecretStr(api_key))

        return PGVector(
            embeddings=embeddings,
            collection_name=collection_name,
            connection=cls._connection,
            use_jsonb=True,
        )