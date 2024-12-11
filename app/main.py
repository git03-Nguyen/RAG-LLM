import os
from fastapi import FastAPI

from app.api import router


app = FastAPI(
    debug=os.getenv("DEBUG", False),
    title="Action-Executing AI Service API",
    description="This is a AI SERVICE API using FastAPI and Swagger UI.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.include_router(router)