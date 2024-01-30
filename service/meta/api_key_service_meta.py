from abc import abstractmethod, ABC
from typing import Any

from constants.constants import Constants


class ApiKeyServiceMeta(ABC):
    @abstractmethod
    def create_api_key(self, user_public_id: str):
        pass

    @abstractmethod
    def delete_api_key(self, key_public_id: str):
        pass

    @abstractmethod
    def get_user_api_keys(self, user_public_id: str):
        pass



