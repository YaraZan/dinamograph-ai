from typing import Annotated

from fastapi import APIRouter, Header, HTTPException

from api.v1.response import Response
from app.auth import validate_api_key
from app.converter.converter import get_dinamogramm_markers

router = APIRouter()

@router.get("/")
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