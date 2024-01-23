from fastapi import APIRouter, Depends, HTTPException, status

from exceptions.user import InvalidEmailError, PasswordsMatchError, EmailExistsError
from schemas.user import UserRegistrationRequest, UserRegistrationResponse
from service.impl.user_service import UserService

# Create router instance
router = APIRouter()


@router.post("/user/register", response_model=UserRegistrationResponse)
def get_random_dnm(
        registration_request: UserRegistrationRequest,
        user_service: UserService = Depends(UserService)
    ) -> UserRegistrationResponse:
    """ Get random dinamogram based on user public id """
    try:
        return user_service.register_user(registration_request)
    except PasswordsMatchError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Пароли не совпадают!")
    except EmailExistsError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Аккаунт с такой почтой уже зарегистрирован!")
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Не удаётся зарегистрировать пользователя")