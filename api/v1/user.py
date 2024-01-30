from fastapi import APIRouter, Depends

from middleware.user import current_user
from schemas.auth import TokenResponse
from schemas.user import UserRegistrationRequest, UserLoginRequest, UserResponse
from service.impl.user_service import UserService

# Create router instance
router = APIRouter()


@router.post("/user/register", response_model=TokenResponse)
async def register_user(
        registration_request: UserRegistrationRequest,
        user_service: UserService = Depends(UserService)
) -> TokenResponse:
    """ Get random dinamogram based on user public id """
    return user_service.register_user(registration_request)


@router.post("/user/login", response_model=TokenResponse)
async def login_user(
        login_request: UserLoginRequest,
        user_service: UserService = Depends(UserService)
) -> TokenResponse:
    """ Get random dinamogram based on user public id """
    return user_service.login_user(login_request)


@router.get("/user/me", response_model=UserResponse)
async def register_user(
        user_service: UserService = Depends(UserService),
        user: dict = Depends(current_user),
) -> UserResponse:
    """ Get random dinamogram based on user public id """
    return user_service.get_user_details(user['public_id'])
