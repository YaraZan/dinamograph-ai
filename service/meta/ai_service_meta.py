from abc import ABC, abstractmethod
from typing import Any


class AiServiceMeta(ABC):
    """ Training methods """
    @abstractmethod
    def train(self, model: str) -> bool:
        pass



