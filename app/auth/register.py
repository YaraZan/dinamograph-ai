import re
from typing import Any

from passlib.hash import bcrypt
from app.requests.user_create_request import UserCreate
from fastapi import HTTPException
from app.database.models.user import User
from app.auth.api_key import generate_api_key
import uuid

from app.database.database import SessionLocal

db = SessionLocal()


def validate_email(email):
    if re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
        return True
    else:
        return False


def register_user(user: UserCreate) -> dict[Any, Any]:
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

    return { "name": user.name, "email": user.email, "public_id": public_id, "api_key": api_key }
