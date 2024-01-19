import jwt
import os
from dotenv import load_dotenv

load_dotenv()


def tokenize(payload: dict):
    return jwt.encode(payload, os.environ.get("SECRET"), algorithm="HS256")


def untokenize(token: str):
    jwt.decode(token, os.environ.get("SECRET"), algorithms=["HS256"])

