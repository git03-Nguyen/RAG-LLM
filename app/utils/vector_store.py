import os
from langchain_postgres.vectorstores import PGVector
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from pydantic import SecretStr
from sqlalchemy.ext.asyncio import create_async_engine


class VectorStore:
    _connection = (f"postgresql+psycopg://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
                f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}")

    _engine = create_async_engine(
        _connection,
        pool_size=5,  # Number of permanent connections to keep in the pool
        max_overflow=10,  # Number of additional connections allowed beyond pool_size
        pool_timeout=30,  # Number of seconds to wait before giving up on getting a connection from the pool
        pool_recycle=-1,  # Number of seconds after which to recycle a connection
    )

    @classmethod
    def get_vector_store(cls, api_key: str, collection_name: str) -> PGVector:
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/text-embedding-004",
            google_api_key=SecretStr(api_key))

        return PGVector(
            embeddings=embeddings,
            collection_name=collection_name,
            connection=cls._engine,
            use_jsonb=True,
            async_mode=True
        )