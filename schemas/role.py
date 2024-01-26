from typing import Union, List, Dict

from pydantic import BaseModel


class RoleResponse(BaseModel):
    id: int
    name: str

