import secrets
import string
from fastapi import HTTPException
from database.database import SessionLocal
from database.models import user

db = SessionLocal()


def generate_api_key(length=32):
    characters = string.ascii_letters + string.digits
    api_key = ''.join(secrets.choice(characters) for _ in range(length))
    return api_key


def validate_api_key(key: str):
    validated_user = db.query(user.User).filter(user.User.api_key == key).first()
    db.close()

    if validated_user is None:
        raise HTTPException(
            status_code=403,
            detail="Неверный API ключ",
        )
    return validated_user

