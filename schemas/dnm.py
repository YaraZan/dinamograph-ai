from typing import Optional

from pydantic import BaseModel

from schemas.marker import MarkerResponse


class DnmGetRandomResponse(BaseModel):
    dnm_id: int
    url: str


class DnmMarkRequest(BaseModel):
    dnm_id: int
    marker_id: int
