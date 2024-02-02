import json

from fastapi import APIRouter, Depends, status, Response
from fastapi.responses import JSONResponse

from middleware.user import current_user
from schemas.auth import TokenResponse
from schemas.user import UserRegistrationRequest, UserLoginRequest, UserResponse
from service.impl.token_service import TokenService
from service.impl.user_service import UserService

# Create router instance
router = APIRouter()

@router.post("/")
async def welcome():
    return JSONResponse(content={"message": "Welcome!"})


@router.post("/user/register")
async def register_user(
        registration_request: UserRegistrationRequest,
        user_service: UserService = Depends(UserService),
        token_service: TokenService = Depends(TokenService),
):
    """ Get random dinamogram based on user public id """

    user = user_service.register_user(registration_request)
    token = token_service.tokenize(user)

    return {"at": token, "ud": {"role": user["role"]["name"]}}


@router.post("/user/login")
async def login_user(
        login_request: UserLoginRequest,
        user_service: UserService = Depends(UserService),
        token_service: TokenService = Depends(TokenService),
):
    """ Get random dinamogram based on user public id """
    user = user_service.login_user(login_request)
    token = token_service.tokenize(user)

    return {"at": token, "ud": {"role": user["role"]["name"]}}


@router.get("/user/me", response_model=UserResponse)
async def get_user_data(
        user_service: UserService = Depends(UserService),
        user: dict = Depends(current_user),
) -> UserResponse:
    """ Get random dinamogram based on user public id """
    return user_service.get_user_details(user['public_id'])
