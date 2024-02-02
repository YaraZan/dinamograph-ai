from typing import Union, List, Dict

from fastapi import File, UploadFile
from pydantic import BaseModel


class MarkerResponse(BaseModel):
    id: int
    name: str
    url: str


class CreateMarkerRequest(BaseModel):
    name: str
    image: UploadFile = None
