from fastapi import APIRouter

router = APIRouter(prefix="/auth",tags=["auth"])

@router.get("/")
async def auth():
    """
    Essa é a rota padão de autenticação do nosso sistema
    """
    return {
        "mensagem": "você acessou a rota padão de autenticação",
        "autenticacao": False
    }