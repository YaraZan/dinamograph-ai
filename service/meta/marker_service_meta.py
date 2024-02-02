from abc import ABC, abstractmethod
from typing import List

from schemas.marker import MarkerResponse, CreateMarkerRequest


class MarkerServiceMeta(ABC):
    @abstractmethod
    def get_all_markers(self) -> List[MarkerResponse]:
        pass

    @abstractmethod
    def get_markers_by_ai_model(self, model_public_id: str) -> List[MarkerResponse]:
        pass

    @abstractmethod
    def create_marker(self, create_marker_request: CreateMarkerRequest):
        pass

    @abstractmethod
    def delete_marker(self, marker_id):
        pass

