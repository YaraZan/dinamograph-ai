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
from sqlalchemy.exc import SQLAlchemyError

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
    def get_user_api_keys(self, user_public_id: str) -> List[ApiKeyResponse]:
        """
        Returns list of user's API keys

        Parameters:
            user_public_id (str): Public key of user, trying to authenticate operation
        """
        try:
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
        except SQLAlchemyError:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Server: Не удаётся получить API-ключи пользователя")
        finally:
            db.close()

    def create_api_key(self, user_public_id: str):
        """
        Creates a new API-key for the user.

        Parameters:
            user_public_id (str): Public key of the user trying to authenticate the operation
        """
        try:
            matching_user = db.query(User).filter(User.public_id == user_public_id).first()

            if not matching_user:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Некорректные данные запроса")

            user_api_keys = db.query(ApiKey).filter(ApiKey.user == matching_user).all()

            if len(user_api_keys) >= 4:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Максимум ключей")

            attempts = 0

            while attempts < constants.DB_MAX_QUERIES:
                new_api_key = self.generate_api_key()

                existing_key = db.query(ApiKey).filter(ApiKey.key == new_api_key).first()

                if not existing_key:
                    new_api_key_object = ApiKey(key=new_api_key)
                    db.add(new_api_key_object)
                    new_api_key_object.user = matching_user
                    db.commit()
                    break

                attempts += 1

            if attempts == constants.DB_MAX_QUERIES:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail="Server: Не удаётся создать уникальный API-ключ")

        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Server: Не удаётся создать API-ключ SqlAlchemy: {e}")

        finally:
            db.close()

    def delete_api_key(self, key_public_id: str):
        try:
            matching_api_key = db.query(ApiKey).filter(ApiKey.public_id == key_public_id).first()

            if not matching_api_key:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail="API-ключ не найден")

            db.delete(matching_api_key)
            db.commit()

        except SQLAlchemyError:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Server: Не удаётся удалить API-ключ")
        finally:
            db.close()

    @staticmethod
    def generate_api_key(length: int = 64) -> str:
        """
        Generate api key for user.

        Parameters:
            length (int, optional): Length of api key. Defaults to 32.

        Returns:
            str: A key generated from method.
        """
        characters = string.ascii_letters + string.digits
        api_key = ''.join(secrets.choice(characters) for _ in range(length))

        return api_key


    @staticmethod
    def validate_api_key(key: str):
        """
        Validate api key provided by user.

        Parameters:
            key (str): API key provided by user.

        Returns:
            bool: Returns true if api key is valid, false otherwise
        """
        try:
            validated_api_key = db.query(ApiKey).filter(ApiKey.key == key).first()

            if validated_api_key is None:
                HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Ошибка доступа")
        except SQLAlchemyError:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Server: Не удаётся проверить подлинность ключа")
        finally:
            db.close()




