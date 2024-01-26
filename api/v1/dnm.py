from typing import Annotated
from fastapi import APIRouter, Depends, Header, HTTPException, status

from schemas.dnm import DnmGetRandomResponse, DnmMarkRequest
from service.impl.api_key_service import ApiKeyService
from service.impl.dnm_service import DnmService

# Create router instance
router = APIRouter()


@router.get("/dnm/{public_id}", response_model=DnmGetRandomResponse)
async def get_random_dnm(
        public_id: str,
        dnm_service: DnmService = Depends(DnmService),
        api_key_service: ApiKeyService = Depends(ApiKeyService),
        authorization: str = Header(...),
) -> DnmGetRandomResponse:
    """ Get random dinamogram based on user public id """
    scheme, token = authorization.split()

    if scheme.lower() != "basic":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Некорректный формат токена авторизации")

    api_key_service.validate_api_key(token)

    return dnm_service.get_random_dnm(public_id)


@router.post("/dnm/")
async def mark_dnm(
        marking_data: DnmMarkRequest,
        dnm_service: DnmService = Depends(DnmService),
        api_key_service: ApiKeyService = Depends(ApiKeyService),
        authorization: str = Header(...),
):
    """ Mark dinamogram based on given id and marker """
    scheme, token = authorization.split()

    if scheme.lower() != "basic":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Некорректный формат токена авторизации")

    api_key_service.validate_api_key(authorization)

    return dnm_service.mark_dnm(marking_data)
