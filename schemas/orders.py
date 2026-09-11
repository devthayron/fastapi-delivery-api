from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class OrderCreate(BaseModel):
    user_id: int


class OrderItemCreate(BaseModel):
    quantity: int
    flavor: str
    size: str
    unit_price: Decimal

    model_config = ConfigDict(from_attributes=True)


class ResponseOrder(BaseModel):
    id: int
    status: str
    price: Decimal
    items: list[OrderItemCreate]

    model_config = ConfigDict(from_attributes=True)
