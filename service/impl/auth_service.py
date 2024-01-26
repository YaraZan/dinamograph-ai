import os
import secrets
import string
import uuid
from datetime import datetime, timedelta
from typing import Any, List

import bcrypt
import jwt
from dotenv import load_dotenv
from jwt import ExpiredSignatureError, InvalidTokenError

from constants.constants import Constants
from database.database import MainSession
from database.models import User
from database.models.api_key import ApiKey
from exceptions.auth import ExpiredApiKeyError, InvalidApiKeyError
from exceptions.user import UserDoesntExistError
from schemas.auth import ApiKeyResponse
from service.meta.auth_service_meta import AuthServiceMeta

# Create database instance
db = MainSession()

# Load environment variables
load_dotenv()

# Constants instance
constants = Constants()


class AuthService(AuthServiceMeta):
    """
        Auth service class

        Implements AuthServiceMeta class methods.
        Used to authenticate and retrieve user.
        Also includes token, encryption and api_key
        methods
    """
    def create_api_key(self, user_public_id: str):
        matching_user = db.query(User).filter(User.public_id == user_public_id).first()

        if not matching_user:
            raise UserDoesntExistError

        new_api_key = ApiKey(
            key=self.generate_api_key()
        )
        db.add(new_api_key)

        new_api_key.user = matching_user
        db.commit()

    def get_user_api_keys(self, user_public_id: str) -> List[ApiKeyResponse]:
        matching_user = db.query(User).filter(User.public_id == user_public_id).first()

        if not matching_user:
            raise UserDoesntExistError

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

    def validate_api_key(self, key: str) -> bool:
        """
        Validate api key provided by user.

        Parameters:
            key (str): API key provided by user.

        Returns:
            bool: Returns true if api key is valid, false otherwise
        """
        validated_api_key = db.query(ApiKey).filter(ApiKey.key == key).first()

        return validated_api_key is not None

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
            raise ExpiredApiKeyError
        except InvalidTokenError:
            raise InvalidApiKeyError

    def hash_password(self, password: str) -> str:
        """
        Hashes the provided password using SHA256 algorithm.

        Parameters:
            password (str): Password to hash

        Returns:
            str: Hashed password
        """
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

        return hashed_password.decode('utf-8')

    def verify_password(self, password: str, hashed_password: str) -> bool:
        """
        Verifies the provided password against the provided hashed password.

        Parameters:
            password (str): Given password
            hashed_password (str): The hashed password

        Returns:
            bool: True if password matches, False otherwise
        """
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

    def generate_uuid(self) -> str:
        """
        Generates a random UUID

        Returns:
            str: Random UUID
        """
        return str(uuid.uuid4())
