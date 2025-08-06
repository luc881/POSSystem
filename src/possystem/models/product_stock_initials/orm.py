from sqlalchemy import BigInteger, Double, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from ...db.session import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class ProductStockInitial(Base):
    __tablename__ = "product_stock_initials"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("products.id"), nullable=False)
    unit_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("units.id"), nullable=False)
    warehouse_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("warehouses.id"), nullable=False)
    price_unit_avg: Mapped[float] = mapped_column(Double, nullable=False)
    stock: Mapped[float] = mapped_column(Double, nullable=False)
    created_at: Mapped = mapped_column(TIMESTAMP(timezone=False), server_default=func.now())
    updated_at: Mapped = mapped_column(TIMESTAMP(timezone=False), onupdate=func.now())
    deleted_at: Mapped = mapped_column(TIMESTAMP(timezone=False), nullable=True)

    # Relationships
    product: Mapped["Product"] = relationship("Product", back_populates="stock_initials")
    unit: Mapped["Unit"] = relationship("Unit", back_populates="stock_initials")
    warehouse: Mapped["Warehouse"] = relationship("Warehouse", back_populates="stock_initials")
