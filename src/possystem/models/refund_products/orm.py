from sqlalchemy import BigInteger, Double, SmallInteger, TIMESTAMP, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ...db.session import Base

class RefundProduct(Base):
    __tablename__ = "refund_products"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("products.id"), nullable=False)
    unit_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("units.id"), nullable=True)  # FK to units
    warehouse_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("warehouses.id"), nullable=True)
    quantity: Mapped[float] = mapped_column(Double, nullable=False)
    sale_detail_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("sale_details.id"), nullable=True)
    client_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("clients.id"), nullable=True)
    type: Mapped[int] = mapped_column(SmallInteger, nullable=False, comment="1=Repair, 2=Replacement, 3=Return")
    state: Mapped[int] = mapped_column(SmallInteger, nullable=False, comment="1=Pending, 2=Review, 3=Repaired, 4=Discarded")
    description: Mapped[str] = mapped_column(Text, nullable=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=True)
    resolution_date: Mapped = mapped_column(TIMESTAMP(timezone=False), nullable=True)
    description_resolution: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped = mapped_column(TIMESTAMP(timezone=False), server_default=func.now())
    updated_at: Mapped = mapped_column(TIMESTAMP(timezone=False), onupdate=func.now())
    deleted_at: Mapped = mapped_column(TIMESTAMP(timezone=False), nullable=True)
    state_clone: Mapped[int] = mapped_column(SmallInteger, nullable=True)

    # Relationships
    product: Mapped["Product"] = relationship("Product", back_populates="refund_products")
    unit: Mapped["Unit"] = relationship("Unit", back_populates="refund_products")  # NEW
    warehouse: Mapped["Warehouse"] = relationship("Warehouse", back_populates="refund_products")
    sale_detail: Mapped["SaleDetail"] = relationship("SaleDetail", back_populates="refund_products")
    client: Mapped["Client"] = relationship("Client", back_populates="refund_products")
    user: Mapped["User"] = relationship("User", back_populates="refund_products")
