from fastapi import APIRouter

router = APIRouter(prefix="/orders",tags=["orders"])

@router.get("/")
async def orders():
    """
    Essa é a rota Pedidos do nosso sistema
    """
    return {
        "mensagem": "you acessed orders site"
        }
