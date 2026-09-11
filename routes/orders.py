from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from dependencies import get_session, verify_token
from models.orders import Order, OrderItem, OrderStatusEnum
from models.users import User
from schemas.orders import OrderCreate, OrderItemCreate, ResponseOrder

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
    session: Session = Depends(get_session),  # noqa: B008
    user: User = Depends(verify_token),  # noqa: B008
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
    session: Session = Depends(get_session),  # noqa: B008
    user: User = Depends(verify_token),  # noqa: B008
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

    session.add(new_order_item)

    order.calcular_preco()

    session.commit()

    return {
        "mensagem": "Item criado com sucesso",
        "item_id": new_order_item.id,
        "preco_pedido": order.price,
    }


@router.post("/remove/{order_item_id}")
async def remove_order(
    order_item_id: int,
    session: Session = Depends(get_session),  # noqa: B008
    user: User = Depends(verify_token),  # noqa: B008
):
    order_item = session.query(OrderItem).filter(OrderItem.id == order_item_id).first()

    order = order_item.order

    if not order_item:
        raise HTTPException(status_code=404, detail="Item do pedido inexistente!")

    if not user.is_admin and user.id != order.user_id:
        raise HTTPException(
            status_code=401,
            detail="Você não tem autorização para fazer essa modificação",
        )

    order.items.remove(order_item)

    order.calcular_preco()

    session.delete(order_item)
    session.commit()

    return {
        "mensagem": "Item removido com sucesso",
        "preco_pedido": order.price,
        "resumo_pedido": order,
    }


@router.post("/completed/{order_id}")
async def completed_order(
    order_id: int,
    session: Session = Depends(get_session),  # noqa: B008
    user: User = Depends(verify_token),  # noqa: B008
):
    """
    Essa é a rota de completar pedidos do nosso sistema
    """

    order = session.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    if order.status == OrderStatusEnum.COMPLETED:
        raise HTTPException(status_code=400, detail="Pedido já está cancelado")

    if not user.is_admin and user.id != order.user_id:
        raise HTTPException(
            status_code=401,
            detail="Você não tem autorização para fazer essa modificação",
        )

    order.status = OrderStatusEnum.COMPLETED
    session.commit()

    return {
        "mensagem": f"Pedido número {order.id} finalizado com sucesso!",
        "pedido": order,
    }


@router.get("/{order_id}")
async def view_order(
    order_id: int,
    session: Session = Depends(get_session),
    user: User = Depends(verify_token),
):
    order = session.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    if order.status == OrderStatusEnum.COMPLETED:
        raise HTTPException(status_code=400, detail="Pedido já está cancelado")

    if not user.is_admin and user.id != order.user_id:
        raise HTTPException(
            status_code=401,
            detail="Você não tem autorização para fazer essa modificação",
        )

    return {
        "quantidade_itens": len(order.items),
        "pedidos": order,
    }


@router.get("/list/user_orders", response_model=list[ResponseOrder])
async def list_order_user(
    session: Session = Depends(get_session),  # noqa: B008
    user: User = Depends(verify_token),  # noqa: B008
):

    orders = session.query(Order).filter(Order.user_id == user.id).all()

    return orders
