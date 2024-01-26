from abc import ABC, abstractmethod
from typing import Any, List


class AIServiceMeta(ABC):
    @abstractmethod
    def create_model(self, model_name: str):
        pass

    # @abstractmethod
    # def train(self, model_name: str, epochs: int = 35):
    #     pass

    @abstractmethod
    def predict(self, model_name: str, image_bytes: bytes):
        pass



