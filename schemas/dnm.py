from typing import Optional

from pydantic import BaseModel

from schemas.marker import MarkerResponse


class DnmGetRandomResponse(BaseModel):
    id: int
    url: str


class DnmResponse(BaseModel):
    id: int
    author: str
    marker: str | None = None
    raw_url: str


class DnmMarkRequest(BaseModel):
    id: int
    marker_id: int
