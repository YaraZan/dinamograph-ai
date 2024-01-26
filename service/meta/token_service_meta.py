from abc import ABC, abstractmethod
from typing import Any

from constants.constants import Constants

# Constants instance
constants = Constants()


class TokenServiceMeta(ABC):
    @abstractmethod
    def tokenize(self, payload: dict, exp: int = constants.AUTHORIZATION_TOKEN_LIFETIME) -> str:
        pass

    @abstractmethod
    def untokenize(self, key: str) -> Any:
        pass


