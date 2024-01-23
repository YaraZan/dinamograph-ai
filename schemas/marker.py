from typing import Union, List, Dict

from pydantic import BaseModel


class MarkerResponse(BaseModel):
    id: int
    name: str
    url: str

