from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.security import create_token
from dependencies import (
    get_session,
    password_hasher,
    verify_refresh_token,
)
from models.users import User
from schemas.users import UserCreate, UserLogin

router = APIRouter(prefix="/auth", tags=["Auth"])


def authenticate_user(email: str, password: str, session: Session):
    user = session.query(User).filter(User.email == email).first()

    if not user or not password_hasher.verify(password, user.hashed_password):
        return None

    return user


@router.get("/")
async def auth():
    """
    Essa é a rota padão de autenticação do nosso sistema
    """
    return {
        "mensagem": "você acessou a rota padão de autenticação",
        "autenticacao": False,
    }


@router.post("/register")
async def register(user: UserCreate, session: Session = Depends(get_session)):  # noqa: B008
    existing_user = session.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Ja existe usuario com esse email")

    hashed_password = password_hasher.hash(user.password)

    new_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_password,
        is_active=user.is_active,
        is_admin=user.is_admin,
    )

    session.add(new_user)
    session.commit()

    return {"mensagem": f"User {new_user.email} cadastrado com sucesso!"}


@router.post("/login")
async def login(credentials: UserLogin, session: Session = Depends(get_session)):  # noqa
    user = authenticate_user(credentials.email, credentials.password, session)

    if not user:
        raise HTTPException(status_code=401, detail="Usuario ou senha incorretos")

    access_token = create_token(user.id, jwt_type="access")
    refresh_token = create_token(user.id, timedelta(days=7), jwt_type="refresh")

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.get("/refresh")
async def refresh_access_token(user_id: int = Depends(verify_refresh_token)):

    access_token = create_token(user_id, jwt_type="access")

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
