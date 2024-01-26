from typing import List, Any

from fastapi import HTTPException, status

from exceptions.auth import ExpiredApiKeyError, InvalidApiKeyError
from exceptions.user import UserDoesntExistError
from schemas.auth import ApiKeyResponse
from service.impl.auth_service import AuthService

# Authorization handlers ---------------------------------- V


def handle_validate_api_key_exceptions(
        authorization: str,
        auth_service: AuthService
):
    scheme, api_key = authorization.split()

    if scheme != "Basic":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Некорректный формат токена авторизации")

    if not auth_service.validate_api_key(api_key):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Ошибка доступа")


def handle_validate_token_exceptions(
        authorization: str,
        auth_service: AuthService
) -> Any:
    scheme, token = authorization.split()

    if scheme != "Bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Некорректный формат токена авторизации")

    try:
        return auth_service.untokenize(token)
    except ExpiredApiKeyError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Необходима повторная авторизация")
    except InvalidApiKeyError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Ошибка доступа")


# CRUD handlers ---------------------------------- V


def handle_get_user_api_keys_exceptions(
        public_id: str,
        auth_service: AuthService
) -> List[ApiKeyResponse]:
    try:
        return auth_service.get_user_api_keys(public_id)
    except UserDoesntExistError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Некорректные данные запроса")


def handle_create_api_key_exceptions(
        public_id: str,
        auth_service: AuthService
):
    try:
        return auth_service.create_api_key(public_id)
    except UserDoesntExistError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Некорректные данные запроса")

