import os
import re
import secrets
import string
import uuid
from datetime import datetime, timedelta
from typing import Any

import bcrypt
import jwt
from dotenv import load_dotenv
from fastapi import HTTPException, status
from jwt import ExpiredSignatureError, InvalidTokenError

from database.database import SessionLocal
from database.models import User
from service.meta.auth_service_meta import AuthServiceMeta

# Create database instance
db = SessionLocal()

# Load environment variables
load_dotenv()


class AuthService(AuthServiceMeta):
    """ Api key methods """
    def generate_api_key(self, length: int = 32) -> str:
        characters = string.ascii_letters + string.digits
        api_key = ''.join(secrets.choice(characters) for _ in range(length))

        return api_key

    def validate_api_key(self, key: str, user_public_id: str) -> bool:
        validated_user = db.query(User).filter(
            (User.public_id == user_public_id) & (User.api_key == key)
        ).first()

        return validated_user is not None

    """ JWT token methods """
    def tokenize(self, payload: Any, exp: int = 10080) -> str:
        expiration_time = datetime.utcnow() + timedelta(minutes=exp)
        payload['exp'] = expiration_time

        return jwt.encode(payload, os.environ.get("SECRET"), algorithm="HS256")

    def untokenize(self, token: str) -> Any:
        try:
            jwt.decode(token, os.environ.get("SECRET"), algorithms=["HS256"])
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Необходима повторная авторизация",
            )
        except InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неправильный токен",
            )

    """ Encryption methods """
    def hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

        return hashed_password.decode('utf-8')

    """ Validation methods """
    def verify_password(self, password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

    """ UUID methods """
    def generate_uuid(self) -> str:
        return str(uuid.uuid4())
