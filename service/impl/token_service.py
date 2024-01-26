import os
import secrets
import string
import uuid
from datetime import datetime, timedelta
from typing import Any, List

import bcrypt
import jwt
from dotenv import load_dotenv
from fastapi import HTTPException, status
from jwt import ExpiredSignatureError, InvalidTokenError

from constants.constants import Constants
from database.database import MainSession
from database.models import User
from database.models.api_key import ApiKey
from schemas.api_key import ApiKeyResponse
from service.meta.token_service_meta import TokenServiceMeta

# Create database instance
db = MainSession()

# Load environment variables
load_dotenv()

# Constants instance
constants = Constants()


class TokenService(TokenServiceMeta):
    """
        Token service class

        Implements TokenServiceMeta class methods.
        Used to authenticate and retrieve user.
        Also includes token, encryption and api_key
        methods
    """
    def tokenize(self, payload: dict, exp: int = constants.AUTHORIZATION_TOKEN_LIFETIME) -> str:
        """
        Transform provided payload to JWT string.

        Parameters:
            payload (Any): Data that should be tokenized.
            exp (int, optional): Expiration time in minutes. Defaults to 10080.

        Returns:
            str: JWT encoded payload
        """
        expiration_time = datetime.utcnow() + timedelta(minutes=exp)

        json_payload = {"payload": payload, "exp": expiration_time}

        return jwt.encode(json_payload, os.environ.get("SECRET"), algorithm="HS256")

    def untokenize(self, token: str) -> Any:
        """
        Transform provided payload to JWT string.

        Parameters:
            token: JWT encoded payload.

        Returns:
            Any: Decoded data.
        """
        try:
            return jwt.decode(token, os.environ.get("SECRET"), algorithms=["HS256"])
        except ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Необходима повторная авторизация")
        except InvalidTokenError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Ошибка доступа")

