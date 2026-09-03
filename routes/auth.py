from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from dependencies import get_session, password_hasher
from models.users import User
from schemas.users import UserCreate

router = APIRouter(prefix="/auth", tags=["Auth"])


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
