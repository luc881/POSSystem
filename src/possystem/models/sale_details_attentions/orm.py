from sqlalchemy import BigInteger, Double, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from ...db.session import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

class SaleDetailAttention(Base):
    __tablename__ = "sale_detail_attentions"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    sale_detail_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("sale_details.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("products.id"), nullable=False)
    warehouse_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("warehouses.id"), nullable=False)
    unit_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("units.id"), nullable=False)
    quantity: Mapped[float] = mapped_column(Double, nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=False), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=False), server_default=func.now(),onupdate=func.now())
    deleted_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=False), nullable=True)

    # Relationships
    sale_detail: Mapped["SaleDetail"] = relationship("SaleDetail", back_populates="attentions")
    product: Mapped["Product"] = relationship("Product", back_populates="sale_detail_attentions")
    warehouse: Mapped["Warehouse"] = relationship("Warehouse", back_populates="sale_detail_attentions")
    unit: Mapped["Unit"] = relationship("Unit", back_populates="sale_detail_attentions")
