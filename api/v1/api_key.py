from typing import Annotated, List
from fastapi import APIRouter, Depends, Header, HTTPException, status

from middleware.user import current_user, is_api_key_owner
from schemas.api_key import ApiKeyResponse
from schemas.dnm import DnmGetRandomResponse, DnmMarkRequest
from service.impl.api_key_service import ApiKeyService
from service.impl.token_service import TokenService
from service.impl.dnm_service import DnmService

# Create router instance
router = APIRouter()


@router.get("/api-key/", response_model=List[ApiKeyResponse])
async def get_user_api_keys(
        api_key_service: ApiKeyService = Depends(ApiKeyService),
        user: dict = Depends(current_user),
) -> List[ApiKeyResponse]:
    """ Get all user API keys """

    return api_key_service.get_user_api_keys(user['public_id'])


@router.post("/api-key/")
async def create_api_key(
        api_key_service: ApiKeyService = Depends(ApiKeyService),
        user: dict = Depends(current_user),
):
    """ Create a new API key for user """

    return api_key_service.create_api_key(user['public_id'])


@router.delete("/api-key/{key_public_id}")
async def delete_api_key(
        api_key_service: ApiKeyService = Depends(ApiKeyService),
        owner_key: str = Depends(is_api_key_owner)
):
    """ Create a new API key for user """

    return api_key_service.delete_api_key(owner_key)
