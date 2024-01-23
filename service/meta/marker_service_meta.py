from abc import ABC, abstractmethod

from schemas.marker import MarkerGet


class MarkerServiceMeta(ABC):
    @abstractmethod
    def get_marker(self) -> MarkerGet:
        pass

