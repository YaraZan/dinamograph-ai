import datetime
from typing import Union, List, Dict, Optional

from pydantic import BaseModel, UUID4

from schemas.role import RoleResponse


class TokenResponse(BaseModel):
    token: str


class ApiKeyResponse(BaseModel):
    public_id: UUID4
    key: str
