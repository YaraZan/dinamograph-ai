from fastapi import APIRouter, Depends

from handlers.user import handle_register_exceptions, handle_login_exceptions
from schemas.auth import TokenResponse
from schemas.user import UserRegistrationRequest, UserLoginRequest
from service.impl.user_service import UserService

# Create router instance
router = APIRouter()


@router.post("/user/register", response_model=TokenResponse)
def register_user(
        registration_request: UserRegistrationRequest,
        user_service: UserService = Depends(UserService)
) -> TokenResponse:
    """ Get random dinamogram based on user public id """
    return handle_register_exceptions(registration_request, user_service)


@router.post("/user/login", response_model=TokenResponse)
def login_user(
        login_request: UserLoginRequest,
        user_service: UserService = Depends(UserService)
) -> TokenResponse:
    """ Get random dinamogram based on user public id """
    return handle_login_exceptions(login_request, user_service)
