from typing import Annotated
from fastapi import APIRouter, Depends, Header

from handlers.auth import handle_validate_api_key_exceptions
from handlers.dnm import handle_get_random_dnm_exceptions, handle_mark_dnm_exceptions
from schemas.dnm import DnmGetRandomResponse, DnmMarkRequest
from service.impl.auth_service import AuthService
from service.impl.dnm_service import DnmService

# Create router instance
router = APIRouter()


@router.get("/dnm/{public_id}", response_model=DnmGetRandomResponse)
async def get_random_dnm(
        public_id: str,
        dnm_service: DnmService = Depends(DnmService),
        auth_service: AuthService = Depends(AuthService),
        authorization: str = Header(...),
) -> DnmGetRandomResponse:
    """ Get random dinamogram based on user public id """
    handle_validate_api_key_exceptions(authorization, auth_service)

    return handle_get_random_dnm_exceptions(public_id, dnm_service)


@router.post("/dnm/")
async def mark_dnm(
        marking_data: DnmMarkRequest,
        dnm_service: DnmService = Depends(DnmService),
        auth_service: AuthService = Depends(AuthService),
        authorization: str = Header(...),
):
    """ Mark dinamogram based on given id and marker """
    handle_validate_api_key_exceptions(authorization, auth_service)

    return handle_mark_dnm_exceptions(marking_data, dnm_service)
