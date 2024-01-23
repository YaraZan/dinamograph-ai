from typing import Annotated

from pydantic import BaseModel
from fastapi import APIRouter, Header, HTTPException

from api.v1.response import Response
from app.auth import validate_api_key
from app.converter.converter import get_random_unmarked_dinamogramm, mark_dinamogramm


router = APIRouter()

@router.get("/{public_id}")
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


@router.post("/")
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