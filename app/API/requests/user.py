from pydantic import BaseModel

class CreateUserRequest(BaseModel):
    name: str
    email: str
    password: str
    confirm_password: str

class LoginUserRequest(BaseModel):
    email: str
    password: str