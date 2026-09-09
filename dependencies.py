import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from sqlalchemy.orm import sessionmaker

from core.config import ALGORITHM, SECRET_KEY
from database.connection import db

SessionLocal = sessionmaker(bind=db)

password_hasher = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login-oauth2")


def get_session():
    try:
        session = SessionLocal()
        yield session
    finally:
        session.close()


def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")

    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")


def verify_token(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)

    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Token inválido",
        )

    return int(user_id)
