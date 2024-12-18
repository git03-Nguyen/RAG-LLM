from pydantic import BaseModel, Field

class AdminRequest(BaseModel):
    google_api_key: str = Field(description="Google API key", examples=["AIzaSyD1q"])
    token: str = Field(description="Admin token", examples=["my_token"])

class UserRequest(BaseModel):
    google_api_key: str = Field(description="Google API key", examples=["AIzaSyD1q"])
    collection_name: str = Field(description="Collection name", examples=["my_collection"])
    query: str = Field(description="Query string", examples=["Suggest scientific films"])
    k: int = Field(description="Number of results", examples=[5])

class RAGRequest(BaseModel):
    google_api_key: str = Field(description="Google API key", examples=["AIzaSyD1q"])
    collection_name: str = Field(description="Collection name", examples=["my_collection"])
    query: str = Field(description="Query string", examples=["Suggest scientific films"])