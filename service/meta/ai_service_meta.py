from abc import ABC, abstractmethod
from typing import Any, List

from schemas.ai import AIModelUpdateRequest, AIModelResponse, AIModelCreateRequest, \
    AIModelGetAllResponse


class AIServiceMeta(ABC):
    @abstractmethod
    def get_all_models(self) -> AIModelGetAllResponse:
        pass

    @abstractmethod
    def get_model_detail(self, model_public_id: str) -> AIModelResponse:
        pass

    @abstractmethod
    def create_model(self, create_model_request: AIModelCreateRequest):
        pass

    @abstractmethod
    def update_model(self, model_update_request: AIModelUpdateRequest):
        pass

    @abstractmethod
    def delete_model(self, model_public_id: str):
        pass



