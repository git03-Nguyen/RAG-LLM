import os
import jwt
from fastapi import HTTPException

def decode_jwt(token: str):
    try:
        payload = jwt.decode(
            jwt=token,
            key=os.getenv("SECRET_KEY"),
            algorithms=[os.getenv("ALGORITHM")]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=403, detail="Invalid token")