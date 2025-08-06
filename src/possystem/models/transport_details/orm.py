from sqlalchemy import String, BigInteger, Double, SmallInteger, Text, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from ...db.session import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class TransportDetail(Base):
    __tablename__ = "transport_details"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    transport_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("transports.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("products.id"), nullable=False)
    unit_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("units.id"), nullable=False)
    quantity: Mapped[float] = mapped_column(Double, nullable=False)
    unit_price: Mapped[float] = mapped_column(Double, nullable=False)
    total: Mapped[float] = mapped_column(Double, nullable=False)
    state: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=1)  # 1=PENDING, 2=DEPARTED, 3=DELIVERED
    user_delivery_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=True)
    delivery_date: Mapped = mapped_column(TIMESTAMP(timezone=False), nullable=True)
    user_departure_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=True)
    departure_date: Mapped = mapped_column(TIMESTAMP(timezone=False), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped = mapped_column(TIMESTAMP(timezone=False), server_default=func.now())
    updated_at: Mapped = mapped_column(TIMESTAMP(timezone=False), onupdate=func.now())
    deleted_at: Mapped = mapped_column(TIMESTAMP(timezone=False), nullable=True)

    # Relationships
    transport: Mapped["Transport"] = relationship("Transport", back_populates="details")
    product: Mapped["Product"] = relationship("Product", back_populates="transport_details")
    unit: Mapped["Unit"] = relationship("Unit", back_populates="transport_details")
    user_delivery: Mapped["User"] = relationship(
        "User", back_populates="delivered_transport_details", foreign_keys=[user_delivery_id]
    )
    user_departure: Mapped["User"] = relationship(
        "User", back_populates="departed_transport_details", foreign_keys=[user_departure_id]
    )
