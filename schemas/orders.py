from decimal import Decimal

from pydantic import BaseModel


class OrderCreate(BaseModel):
    user_id: int


class OrderItemCreate(BaseModel):
    quantity: int
    flavor: str
    size: str
    unit_price: Decimal
