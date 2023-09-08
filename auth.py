import time
import uuid

from flask import request

from app import bcrypt
from config import TOKEN_TTL
from errors import ApiException
from models import TokenModel


def hash_password(password: str):
    password = password.encode()
    hashed = bcrypt.generate_password_hash(password)
    return hashed.decode()


def check_auth(session) -> TokenModel:
    try:
        token = uuid.UUID(request.headers.get("token"))
    except (ValueError, TypeError):
        raise ApiException(403, "incorrect token")
    token = session.query(TokenModel).get(token)

    if token is None:
        raise ApiException(403, "incorrect token")

    if time.time() - token.creation_time.timestamp() > TOKEN_TTL:
        raise ApiException(403, "incorrect token")

    return token