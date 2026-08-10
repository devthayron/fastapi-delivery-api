from fastapi import APIRouter

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get("/")
async def orders():
    """
    Essa é a rota Pedidos do nosso sistema
    """
    return {"mensagem": "você está na rota de pedidos"}
