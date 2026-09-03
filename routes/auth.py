from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from dependencies import get_session, password_hasher
from models.users import User
from schemas.users import UserCreate, UserLogin

router = APIRouter(prefix="/auth", tags=["Auth"])


def create_token(user_id: int):
    token = f"token_for_user_{user_id}"
    return token


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

    user_new = User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_password,
        is_active=user.is_active,
        is_admin=user.is_admin,
    )

    session.add(user_new)
    session.commit()

    return {"mensagem": f"User {user_new.email} cadastrado com sucesso!"}


@router.post("/login")
async def login(user: UserLogin, session: Session = Depends(get_session)):  # noqa
    user_db = session.query(User).filter(User.email == user.email).first()

    if not user_db:
        raise HTTPException(status_code=401, detail="Usuario não encontrado")

    if not password_hasher.verify(user.password, user_db.hashed_password):
        raise HTTPException(status_code=401, detail="Usuario ou senha incorretos")

    access_token = create_token(user_db.id)

    return {
        "access_token": access_token,
        "token_type": "Bearer",
    }
