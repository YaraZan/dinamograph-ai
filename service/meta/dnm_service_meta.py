from abc import ABC, abstractmethod
from typing import List, Any
from schemas.dnm import DnmMarkRequest, DnmGetRandomResponse, DnmResponse


class DnmServiceMeta(ABC):

    @abstractmethod
    def get_all_dnm(self) -> List[DnmResponse]:
        pass

    @abstractmethod
    def get_random_dnm(self, user_public_id: str) -> DnmGetRandomResponse:
        pass

    @abstractmethod
    def mark_dnm(self, marking_data: List[DnmMarkRequest]):
        pass

    @abstractmethod
    def delete_dnm(self, dnm_id: int):
        pass
