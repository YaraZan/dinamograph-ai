from typing import Annotated
from fastapi import APIRouter, Depends

from schemas.dnm import DnmGetRandomResponse, DnmMarkRequest
from service.impl import dnm_service
from service.impl.dnm_service import DnmService

# Create router instance
router = APIRouter()


@router.get("/dnm/{public_id}", response_model=DnmGetRandomResponse)
def get_random_dnm(
        public_id: str,
        dnm_service: DnmService = Depends(DnmService)
    ) -> DnmGetRandomResponse:
    """ Get random dinamogram based on user public id """
    return dnm_service.get_random_dnm(public_id)


@router.post("/dnm/", response_model=None)
def mark_dnm(
        marking_data: DnmMarkRequest,
        dnm_service: DnmService = Depends(DnmService)
    ) -> None:
    """ Mark dinamogram based on given id and marker """
    return dnm_service.mark_dnm(marking_data)