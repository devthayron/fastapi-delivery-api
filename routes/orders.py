from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from dependencies import get_session, verify_token
from models.orders import Order, OrderStatusEnum
from models.users import User
from schemas.orders import OrderCreate

router = APIRouter(
    prefix="/orders", tags=["Orders"], dependencies=[Depends(verify_token)]
)


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


@router.post("/cancel/{order_id}")
async def cancel_order(
    order_id: int,
    session: Session = Depends(get_session),  # noqa: B008
    user: User = Depends(verify_token),  # noqa: B008
):
    """
    Essa é a rota de cancelamento de pedidos do nosso sistema
    """

    order = session.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    if order.status == OrderStatusEnum.CANCELED:
        raise HTTPException(status_code=400, detail="Pedido já está cancelado")

    if not user.is_admin and user.id != order.user_id:
        raise HTTPException(
            status_code=401,
            detail="Você não tem autorização para fazer essa modificação",
        )

    order.status = OrderStatusEnum.CANCELED
    session.commit()

    return {
        "mensagem": f"Pedido número {order.id} cancelado com sucesso!",
        "pedido": order,
    }


@router.get("/list")
async def list_order(
    session: Session = Depends(get_session), user: User = Depends(verify_token)
):
    if not user.is_admin:
        raise HTTPException(
            status_code=401,
            detail="Você não tem autorização para fazer essa operação",
        )

    orders = session.query(Order).all()

    return {"pedidos": orders}
