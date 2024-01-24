from abc import ABC, abstractmethod

from schemas.marker import MarkerGetAllResponse


class MarkerServiceMeta(ABC):
    @abstractmethod
    def get_all_markers(self) -> MarkerGetAllResponse:
        pass

