from typing import Annotated, List
from fastapi import APIRouter, Depends, Header

from handlers.auth import handle_validate_api_key_exceptions, handle_get_user_api_keys_exceptions, \
    handle_validate_token_exceptions, handle_create_api_key_exceptions
from handlers.dnm import handle_get_random_dnm_exceptions, handle_mark_dnm_exceptions
from schemas.auth import ApiKeyResponse
from schemas.dnm import DnmGetRandomResponse, DnmMarkRequest
from service.impl.auth_service import AuthService
from service.impl.dnm_service import DnmService

# Create router instance
router = APIRouter()


@router.get("/auth/api-keys/", response_model=List[ApiKeyResponse])
def get_user_api_keys(
        auth_service: AuthService = Depends(AuthService),
        authorization: str = Header(...),
) -> List[ApiKeyResponse]:
    """ Get all user API keys """
    untokenized = handle_validate_token_exceptions(authorization, auth_service)

    return handle_get_user_api_keys_exceptions(untokenized['payload']['public_id'], auth_service)


@router.post("/auth/api-keys/")
def create_api_key(
        auth_service: AuthService = Depends(AuthService),
        authorization: str = Header(...),
):
    """ Create a new API key for user """
    untokenized = handle_validate_token_exceptions(authorization, auth_service)

    handle_create_api_key_exceptions(untokenized['payload']['public_id'], auth_service)

