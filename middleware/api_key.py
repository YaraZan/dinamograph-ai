from fastapi import Depends, HTTPException, status, Header

from service.impl.api_key_service import ApiKeyService


def validate_api_key(
        authorization: str = Header(...),
        api_key_service: ApiKeyService = Depends(ApiKeyService)
):
    scheme, key = authorization.split()

    if scheme.lower() != "basic":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Некорректный формат токена авторизации")

    api_key_service.validate_api_key(key)