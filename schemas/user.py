import enum
from typing import Optional, Union, Any
from pydantic import BaseModel, UUID4

from schemas.role import RoleResponse


class UserRegistrationRequest(BaseModel):
    name: str
    email: str
    password: str
    confirm_password: str


class UserLoginRequest(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    public_id: UUID4
    name: str
    email: str
    role: Optional[RoleResponse]


