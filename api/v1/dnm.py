from typing import Annotated, List
from fastapi import APIRouter, Depends, Header, HTTPException, status

from middleware.api_key import validate_api_key
from middleware.user import is_admin
from schemas.dnm import DnmGetRandomResponse, DnmMarkRequest, DnmResponse
from service.impl.api_key_service import ApiKeyService
from service.impl.dnm_service import DnmService

# Create router instance
router = APIRouter()


@router.get("/dnm/all", response_model=List[DnmResponse])
async def get_all_dnm(
        dnm_service: DnmService = Depends(DnmService),
        _=Depends(is_admin),
) -> List[DnmResponse]:
    """ Get random dinamogram based on user public id """

    return dnm_service.get_all_dnm()


@router.get("/dnm/random/{public_id}", response_model=DnmGetRandomResponse)
async def get_random_dnm(
        public_id: str,
        dnm_service: DnmService = Depends(DnmService),
        _=Depends(validate_api_key),
) -> DnmGetRandomResponse:
    """ Get random dinamogram based on user public id """

    return dnm_service.get_random_dnm(public_id)


@router.post("/dnm/mark")
async def mark_dnm(
        marking_data: List[DnmMarkRequest],
        dnm_service: DnmService = Depends(DnmService),
        _=Depends(validate_api_key),
):
    """ Mark dinamogram based on given id and marker """

    return dnm_service.mark_dnm(marking_data)


@router.delete("/dnm/delete")
async def get_all_dnm(
        dnm_id: int,
        dnm_service: DnmService = Depends(DnmService),
        _=Depends(is_admin),
):
    """ Get random dinamogram based on user public id """

    return dnm_service.delete_dnm(dnm_id)
