from typing import Annotated, Union
from fastapi import FastAPI, HTTPException, Header

from app.API.responses import Response
from app.API.requests import CreateUserRequest
from app.API.requests import DnmMarkRequest
from app.API.responces import CreateUserResponce
from app.database.database import SessionLocal
from app.converter.converter import get_random_unmarked_dinamogramm
from app.converter.converter import get_dinamogramm_markers
from app.converter.converter import mark_dinamogramm
from app.auth.auth import register_user
from app.auth.api_key import validate_api_key
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set this to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/datasets", StaticFiles(directory="datasets"), name="datasets")

@app.get("/")
def home():
    return {'message': 'home'}


@app.post("/register")
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


@app.get("/d/{public_id}")
async def get_unmarked_dinamogram(
        public_id: str,
        x_api_key: Annotated[str | None, Header()] = None
    ) -> Response:
    validate_api_key(x_api_key)

    response = Response(
        data=get_random_unmarked_dinamogramm(public_id),
        message="Успешно получена динамограмма",
        status=200
    )

    if response.data is not None:
        return response
    else:
        raise HTTPException(status_code=404, detail="Ошибка при получении динамограммы")


@app.post("/d")
async def mark_dinamogram(
        request: DnmMarkRequest,
        x_api_key: Annotated[str | None, Header()] = None
    ) -> Response:
    validate_api_key(x_api_key)

    try:
        mark_dinamogramm(
            id=request.id,
            marker_id=request.marker_id
        )

        response = Response(
            data=None,
            message="Успешно промаркеровано",
            status=200
        )

        return response
    except Exception:
        raise HTTPException(status_code=404, detail="Возникла ошибка")


@app.get("/m")
async def get_markers(
        x_api_key: Annotated[str | None, Header()] = None
    ) -> Response:
    validate_api_key(x_api_key)

    try:
        markers = get_dinamogramm_markers()

        response = Response(
            data=markers,
            message="Успешно промаркеровано",
            status=200
        )

        return response
    except Exception:
        raise HTTPException(status_code=404, detail="Возникла ошибка при получении маркеров")

