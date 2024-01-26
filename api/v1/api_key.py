from typing import Annotated, List
from fastapi import APIRouter, Depends, Header, HTTPException, status

from schemas.api_key import ApiKeyResponse
from schemas.dnm import DnmGetRandomResponse, DnmMarkRequest
from service.impl.api_key_service import ApiKeyService
from service.impl.token_service import TokenService
from service.impl.dnm_service import DnmService

# Create router instance
router = APIRouter()


@router.get("/api-key/", response_model=List[ApiKeyResponse])
async def get_user_api_keys(
        token_service: TokenService = Depends(TokenService),
        api_key_service: ApiKeyService = Depends(ApiKeyService),
        authorization: str = Header(...),
) -> List[ApiKeyResponse]:
    """ Get all user API keys """
    scheme, token = authorization.split()

    if scheme.lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Некорректный формат токена авторизации")

    untokenized = token_service.untokenize(token)

    return api_key_service.get_user_api_keys(untokenized['payload']['public_id'])


@router.post("/api-key/")
async def create_api_key(
        token_service: TokenService = Depends(TokenService),
        api_key_service: ApiKeyService = Depends(ApiKeyService),
        authorization: str = Header(...),
):
    """ Create a new API key for user """
    scheme, token = authorization.split()

    if scheme.lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Некорректный формат токена авторизации")

    untokenized = token_service.untokenize(token)

    return api_key_service.create_api_key(untokenized['payload']['public_id'])

