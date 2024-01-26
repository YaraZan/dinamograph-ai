from abc import ABC, abstractmethod
from typing import List, Any
from schemas.dnm import DnmMarkRequest, DnmGetRandomResponse


class DnmServiceMeta(ABC):
    @abstractmethod
    def get_random_dnm(self, user_public_id: str) -> DnmGetRandomResponse:
        pass

    @abstractmethod
    def mark_dnm(self, marking_data: DnmMarkRequest):
        pass
