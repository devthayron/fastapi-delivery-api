from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies import get_session
from models.orders import Order
from schemas.orders import OrderCreate

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get("/")
async def orders():
    """
    Essa é a rota Pedidos do nosso sistema
    """
    return {"mensagem": "você está na rota de pedidos"}


@router.post("/")
async def create_order(order: OrderCreate, session: Session = Depends(get_session)):  # noqa: B008
    """
    Essa é a rota de criação de pedidos do nosso sistema
    """

    order_new = Order(user_id=order.user_id)

    session.add(order_new)
    session.commit()

    return {"mensagem": "Pedido criado com sucesso!", "ID do pedido": order_new.id}
