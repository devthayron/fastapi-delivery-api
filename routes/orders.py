from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from dependencies import get_session, verify_token
from models.orders import Order, OrderItem, OrderStatusEnum
from models.users import User
from schemas.orders import OrderCreate, OrderItemCreate

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


@router.post("/add/{order_id}")
async def add_order(
    order_id: int,
    order_item: OrderItemCreate,
    session: Session = Depends(get_session),
    user: User = Depends(verify_token),
):
    order = session.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Pedido inexistente!")

    if not user.is_admin and user.id != order.user_id:
        raise HTTPException(
            status_code=401,
            detail="Você não tem autorização para fazer essa modificação",
        )

    new_order_item = OrderItem(
        quantity=order_item.quantity,
        flavor=order_item.flavor,
        size=order_item.size,
        unit_price=order_item.unit_price,
        order_id=order_id,
    )

    order.calcular_preco()

    session.add(new_order_item)
    session.commit()

    return {
        "mensagem": "Item criado com sucesso",
        "item_id": new_order_item.id,
        "preco_pedido": order.price,
    }
