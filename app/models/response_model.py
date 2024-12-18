from pydantic import BaseModel, Field

class UserResponse(BaseModel):
    status: int = Field(description="Status code", examples=[200])
    data: dict = Field(description="Response data", examples=[{"result": "my_result"}])

class RAGResponse(BaseModel):
    status: int = Field(description="Status code", examples=[200])
    data: dict = Field(description="Response data", examples=[{"result": "my_result"}])

class KnowledgeBaseResponse(BaseModel):
    status: int = Field(description="Status code", examples=[200])
    data:dict = Field(description="Response data", examples=[{"message": "my_message"}])

class ErrorResponse(BaseModel):
    status: int = Field(description="Status code", examples=[404])
    detail: str = Field(description="Error message", examples=["Not found"])
