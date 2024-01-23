import enum
from typing import Optional
from pydantic import BaseModel

from schemas.role import RoleResponse


class UserRegistrationRequest(BaseModel):
    name: str
    email: str
    password: str
    confirm_password: str


class UserRegistrationResponse(BaseModel):
    public_id: str
    name: str
    email: str
    api_key: str
    role: Optional[RoleResponse]


class UserLoginRequest(BaseModel):
    email: str
    password: str


class UserLoginResponse(BaseModel):
    public_id: str
    name: str
    email: str
    api_key: str
    role: Optional[RoleResponse]
