from decimal import Decimal
from enum import StrEnum

from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base


class OrderStatusEnum(StrEnum):
    PENDING = "pending"
    CANCELED = "canceled"
    COMPLETED = "completed"


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[OrderStatusEnum] = mapped_column(
        SQLEnum(
            OrderStatusEnum, values_callable=lambda x: [e.value for e in x]
        ),  # Usa os valores definidos no Enum (ex.: "pending") em vez dos nomes (ex.: "PENDING")
        nullable=False,
        default=OrderStatusEnum.PENDING,
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=False, default=0.00
    )  # padrão recomendado para valores monetários, pois o tipo float pode gerar imprecisão

    def calcular_preco(self):
        self.price = 10


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    quantity: Mapped[int] = mapped_column(nullable=False)
    flavor: Mapped[str] = mapped_column(nullable=False)
    size: Mapped[str] = mapped_column(nullable=False)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False)
