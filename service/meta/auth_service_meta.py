from abc import ABC, abstractmethod
from typing import Any

from constants.constants import Constants

# Constants instance
constants = Constants()


class AuthServiceMeta(ABC):
    @abstractmethod
    def create_api_key(self, user_public_id: str):
        pass

    @abstractmethod
    def get_user_api_keys(self, user_public_id: str):
        pass

    @abstractmethod
    def generate_api_key(self, length: int = 32) -> str:
        pass

    @abstractmethod
    def validate_api_key(self, key: str) -> bool:
        pass

    @abstractmethod
    def tokenize(self, payload: dict, exp: int = constants.AUTHORIZATION_TOKEN_LIFETIME) -> str:
        pass

    @abstractmethod
    def untokenize(self, key: str) -> Any:
        pass

    @abstractmethod
    def hash_password(self, password: str) -> str:
        pass

    @abstractmethod
    def verify_password(self, password: str, hashed_password: str) -> bool:
        pass

    @abstractmethod
    def generate_uuid(self) -> str:
        pass


