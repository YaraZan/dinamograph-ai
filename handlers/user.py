from fastapi import HTTPException, status

from exceptions.user import InvalidEmailError, UserDoesntExistError, PasswordsMatchError, EmailExistsError
from schemas.auth import TokenResponse
from schemas.user import UserLoginRequest, UserRegistrationRequest
from service.impl.user_service import UserService


def handle_register_exceptions(
        registration_request: UserRegistrationRequest,
        user_service: UserService,
) -> TokenResponse:
    try:
        return user_service.register_user(registration_request)
    except InvalidEmailError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Неверный формат почты")
    except PasswordsMatchError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Пароли не совпадают")
    except EmailExistsError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Аккаунт с такой почтой уже зарегистрирован")
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Не удаётся зарегистрировать пользователя")


def handle_login_exceptions(
        login_request: UserLoginRequest,
        user_service: UserService
) -> TokenResponse:
    try:
        return user_service.login_user(login_request)
    except InvalidEmailError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Неверный формат почты")
    except UserDoesntExistError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Пользователя с такой почтой не существует")
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Не удаётся выполнить вход")
