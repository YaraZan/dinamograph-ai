from typing import Optional

from pydantic import BaseModel

from schemas.marker import MarkerResponse


class DnmGetRandomResponse(BaseModel):
    id: int
    url: str


class DnmMarkRequest(BaseModel):
    id: int
    marker_id: int
