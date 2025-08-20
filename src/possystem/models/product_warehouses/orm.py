from sqlalchemy import BigInteger, Double, SmallInteger, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from ...db.session import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

class ProductWarehouse(Base):
    __tablename__ = "product_warehouses"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("products.id"), nullable=False)
    warehouse_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("warehouses.id"), nullable=False)
    unit_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("units.id"), nullable=False)
    stock: Mapped[float] = mapped_column(Double, nullable=False, default=0)  # current stock
    threshold: Mapped[float] = mapped_column(Double, nullable=False, default=0)  # minimum threshold before low stock alert
    state_stock: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=1)  # 1 = available, 2 = low stock, 3 = out of stock
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=False), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=False), server_default=func.now(), onupdate=func.now())
    deleted_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=False), nullable=True)

    # Relationships
    product: Mapped["Product"] = relationship("Product", back_populates="product_warehouses")
    warehouse: Mapped["Warehouse"] = relationship("Warehouse", back_populates="product_warehouses")
    unit: Mapped["Unit"] = relationship("Unit", back_populates="product_warehouses")
