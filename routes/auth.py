from fastapi import APIRouter, Depends

from dependencies import get_session
from models.users import User

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
async def register(email: str, password: str, name: str, session=Depends(get_session)):
    user = session.query(User).filter(User.email == email).first()

    if user:
        return {"mensagem": "ja existe usuario com esse email"}

    user_new = User(name=name, email=email, password_hash=password)
    session.add(user_new)
    session.commit()
    return {"mensagem": "User cadastrado"}
