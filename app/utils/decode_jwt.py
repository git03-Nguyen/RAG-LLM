import os
import jwt
from fastapi import HTTPException

from app.utils.exceptions import CustomException


def decode_jwt(token: str):
    try:
        payload = jwt.decode(
            jwt=token,
            key=os.getenv('SECRET_KEY'),
            algorithms=[os.getenv('ALGORITHM')]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise CustomException(
            status=403,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError:
        raise CustomException(
            status=403,
            detail="Invalid token"
        )