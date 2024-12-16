import os
import jwt
from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime, timedelta, timezone

router = APIRouter()

def create_jwt_token(role: str):
    expiration = datetime.now(timezone.utc) + timedelta(hours=2160)  # Token expires in 90 days
    payload = {
        "role": role,
        "exp": expiration,
        "iat": datetime.now(timezone.utc),
    }
    token = jwt.encode(
        payload=payload,
        key=os.getenv("SECRET_KEY"),
        algorithm=os.getenv("ALGORITHM")
    )
    return token

@router.post("/", tags=["Token"], description="Create a JWT token")
def create_token():
    token = create_jwt_token("admin")
    print("token: ", token)
    return "Token created successfully!"