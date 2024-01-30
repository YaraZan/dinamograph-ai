from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.exc import SQLAlchemyError

from database.database import MainSession
from database.models import User
from database.models.api_key import ApiKey
from service.impl.token_service import TokenService

# Create database instance
db = MainSession()


def current_user(
        authorization: str = Header(...),
        token_service: TokenService = Depends(TokenService)
) -> dict:
    scheme, token = authorization.split()

    if scheme.lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Некорректный формат токена авторизации")

    return token_service.untokenize(token)['payload']


def is_admin(
        user: dict = Depends(current_user),
):
    if not user['role']['name'] == 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Ошибка доступа")


def is_api_key_owner(
        key_public_id: str,
        user: dict = Depends(current_user),
):
    try:
        matching_user = db.query(User).filter(User.public_id == user['public_id']).first()
        matching_api_key = db.query(ApiKey).filter(ApiKey.public_id == key_public_id).first()

        if not matching_api_key:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="API-ключ не найден")

        if not matching_user.id == matching_api_key.user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Ошибка доступа")

        return key_public_id

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Server: Не удаётся удалить API-ключ")
    finally:
        db.close()
