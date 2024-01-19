import re
from typing import Any
from passlib.hash import bcrypt
from fastapi import HTTPException
from app.API.requests import CreateUserRequest, LoginUserRequest
from app.database.models.user import User
from app.auth.api_key import generate_api_key
import uuid
from app.database.database import SessionLocal

# db
db = SessionLocal()

def validate_email(email):
    return re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email)


def register_user(
        user: CreateUserRequest
    ) -> dict[str, str] | HTTPException:
    if not validate_email(user.email):
        raise HTTPException(status_code=404, detail="Неверный формат почты!")

    if not user.password == user.confirm_password:
        raise HTTPException(status_code=404, detail="Пароли не совпадают!")

    hashed_password = bcrypt.hash(user.password)
    api_key = generate_api_key()
    public_id = str(uuid.uuid4())

    new_user = User(
        public_id=public_id,
        name=user.name,
        email=user.email,
        password=hashed_password,
        api_key=api_key
    )

    db.add(new_user)
    db.commit()

    return { "public_id": public_id, "email": user, "api_key": api_key, "name": user.name }


def login_user(
        user: LoginUserRequest
):
    matching_user = db.query(User).filter(User.email == user.email).first()

    if not matching_user:
        raise HTTPException(status_code=404, detail="Пользователя с такой почтой не существует!")

    if not bcrypt.hash(user.password) == matching_user.password:
        raise HTTPException(status_code=404, detail="Пароли не совпадают!")

    return { "public_id": matching_user.public_id, "name": matching_user.name,
             "email":matching_user.email, "api_key": matching_user.api_key }

