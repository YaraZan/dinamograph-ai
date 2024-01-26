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
from service.meta.api_key_service_meta import ApiKeyServiceMeta

# Create database instance
db = MainSession()

# Load environment variables
load_dotenv()

# Constants instance
constants = Constants()


class ApiKeyService(ApiKeyServiceMeta):
    """
        Auth service class

        Implements AuthServiceMeta class methods.
        Used to authenticate and retrieve user.
        Also includes token, encryption and api_key
        methods
    """
    def create_api_key(self, user_public_id: str):
        """
        Creates new API-key for user

        Parameters:
            user_public_id (str): Public key of user, trying to authenticate operation
        """
        matching_user = db.query(User).filter(User.public_id == user_public_id).first()

        if not matching_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Некорректные данные запроса")

        new_api_key = ApiKey(
            key=self.generate_api_key()
        )
        db.add(new_api_key)

        new_api_key.user = matching_user
        db.commit()

    def get_user_api_keys(self, user_public_id: str) -> List[ApiKeyResponse]:
        """
        Returns list of user's API keys

        Parameters:
            user_public_id (str): Public key of user, trying to authenticate operation
        """
        matching_user = db.query(User).filter(User.public_id == user_public_id).first()

        if not matching_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Некорректные данные запроса")

        user_api_keys = db.query(ApiKey).filter(ApiKey.user == matching_user).all()

        api_key_responses = []

        for api_key in user_api_keys:
            api_key_responses.append(
                ApiKeyResponse(
                    public_id=api_key.public_id,
                    key=api_key.key
                )
            )

        return user_api_keys

    def generate_api_key(self, length: int = 64) -> str:
        """
        Generate api key for user.

        Parameters:
            length (int, optional): Length of api key. Defaults to 32.

        Returns:
            str: A key generated from method.
        """
        characters = string.ascii_letters + string.digits
        api_key = ''.join(secrets.choice(characters) for _ in range(length))

        queries = 0

        while queries < constants.DB_MAX_QUERIES:
            if not db.query(ApiKey).filter(ApiKey.key == api_key).first():
                break
            queries += 1

        if queries == constants.DB_MAX_QUERIES:
            raise Exception

        return api_key

    def validate_api_key(self, key: str):
        """
        Validate api key provided by user.

        Parameters:
            key (str): API key provided by user.

        Returns:
            bool: Returns true if api key is valid, false otherwise
        """
        validated_api_key = db.query(ApiKey).filter(ApiKey.key == key).first()

        if validated_api_key is None:
            HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Ошибка доступа")




