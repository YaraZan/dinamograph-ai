from pydantic import BaseModel
from fastapi import APIRouter, HTTPException

from api.v1.response import Response
from app.auth.auth import register_user, login_user
from app.auth.jwt import tokenize

router = APIRouter()


class CreateUserRequest(BaseModel):
    name: str
    email: str
    password: str
    confirm_password: str


class LoginUserRequest(BaseModel):
    email: str
    password: str


@router.post("/register")
async def register(
        request: CreateUserRequest
) -> Response:
    try:
        user = register_user(user=request)

        response = Response(
            data=user,
            message="Вы успешно зарегистрировались",
            status=200
        )

        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при создании пользователя: {str(e)}")


@router.post("/login")
async def register(
        request: LoginUserRequest
) -> Response:
    try:
        user = login_user(user=request)

        response = Response(
            data={
                'token': tokenize({
                    'user': user,
                })
            },
            message="Вы успешно авторизовались",
            status=200
        )

        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при создании пользователя: {str(e)}")