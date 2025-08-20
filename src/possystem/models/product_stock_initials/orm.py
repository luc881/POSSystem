from sqlalchemy import BigInteger, Double, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from ...db.session import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

class ProductStockInitial(Base):
    __tablename__ = "product_stock_initials"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    price_unit_avg: Mapped[float] = mapped_column(Double, nullable=False)
    stock: Mapped[float] = mapped_column(Double, nullable=False)
    product_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("products.id"), nullable=True)
    unit_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("units.id"), nullable=True)
    warehouse_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("warehouses.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=False), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=False), server_default=func.now(), onupdate=func.now())
    deleted_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=False), nullable=True)

    # Relationships
    unit: Mapped["Unit"] = relationship("Unit", back_populates="stock_initials")
    warehouse: Mapped["Warehouse"] = relationship("Warehouse", back_populates="stock_initials")
    product: Mapped["Product"] = relationship("Product", back_populates="stock_initials")
