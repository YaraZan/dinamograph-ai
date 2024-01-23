from abc import ABC, abstractmethod
from typing import Any


class AuthServiceMeta(ABC):
    """ Api key methods """
    @abstractmethod
    def generate_api_key(self, length: int = 32) -> str:
        pass

    @abstractmethod
    def validate_api_key(self, key: str, user_public_id: str) -> bool:
        pass

    """ JWT token methods """
    @abstractmethod
    def tokenize(self, payload: Any, exp: int = 10080) -> str:
        pass

    @abstractmethod
    def untokenize(self, key: str) -> Any:
        pass

    """ Encryption methods """
    @abstractmethod
    def hash_password(self, password: str) -> str:
        pass

    """ Validation methods """
    @abstractmethod
    def verify_password(self, password: str, hashed_password: str) -> bool:
        pass

    """ UUID methods """
    @abstractmethod
    def generate_uuid(self) -> str:
        pass
