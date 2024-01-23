from datetime import datetime, timedelta
from typing import Any

import jwt
import os
from dotenv import load_dotenv
from fastapi import HTTPException, status
from jwt import ExpiredSignatureError, InvalidTokenError

load_dotenv()


def tokenize(payload: Any, expiration: int = 30):
    expiration_time = datetime.utcnow() + timedelta(minutes=expiration)
    payload['exp'] = expiration_time
    return jwt.encode(payload, os.environ.get("SECRET"), algorithm="HS256")


def untokenize(token: str):
    try:
        jwt.decode(token, os.environ.get("SECRET"), algorithms=["HS256"])
    except ExpiredSignatureError:
        # Handle token expiration
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Необходима повторная авторизация",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except InvalidTokenError:
        # Handle other token validation errors
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неправильный токен",
            headers={"WWW-Authenticate": "Bearer"},
        )

