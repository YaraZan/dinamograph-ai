from typing import Annotated
from fastapi import APIRouter, Depends, Header, HTTPException, status

from middleware.api_key import validate_api_key
from schemas.dnm import DnmGetRandomResponse, DnmMarkRequest
from service.impl.api_key_service import ApiKeyService
from service.impl.dnm_service import DnmService

# Create router instance
router = APIRouter()


@router.get("/dnm/{public_id}", response_model=DnmGetRandomResponse)
async def get_random_dnm(
        public_id: str,
        dnm_service: DnmService = Depends(DnmService),
        _=Depends(validate_api_key),
) -> DnmGetRandomResponse:
    """ Get random dinamogram based on user public id """

    return dnm_service.get_random_dnm(public_id)


@router.post("/dnm/")
async def mark_dnm(
        marking_data: DnmMarkRequest,
        dnm_service: DnmService = Depends(DnmService),
        _=Depends(validate_api_key),
):
    """ Mark dinamogram based on given id and marker """

    return dnm_service.mark_dnm(marking_data)
