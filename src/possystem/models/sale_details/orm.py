from sqlalchemy import BigInteger, Double, SmallInteger, TIMESTAMP, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ...db.session import Base
from datetime import datetime

class SaleDetail(Base):
    __tablename__ = "sale_details"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    sale_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("sales.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("products.id"), nullable=False)
    product_category_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("product_categories.id"), nullable=True)
    quantity: Mapped[float] = mapped_column(Double, nullable=False)
    price_unit: Mapped[float] = mapped_column(Double, nullable=False)
    discount: Mapped[float] = mapped_column(Double, nullable=True)
    subtotal: Mapped[float] = mapped_column(Double, nullable=True)  # unit price - discount
    total: Mapped[float] = mapped_column(Double, nullable=True)     # subtotal * quantity
    unit_id: Mapped[int] = mapped_column(BigInteger, nullable=True)
    warehouse_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("warehouses.id"), nullable=True)
    tax: Mapped[float] = mapped_column(Double, nullable=True)  # igv, renamed to tax
    description: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=False), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=False), server_default=func.now(), onupdate=func.now())
    deleted_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=False), nullable=True)
    state_attention: Mapped[int] = mapped_column(SmallInteger, nullable=True)  # 1 = pending, 2 = partial, 3 = complete
    quantity_pending: Mapped[float] = mapped_column(Double, nullable=True)  # pending quantity to attend

    # Relationships
    sale: Mapped["Sale"] = relationship("Sale", back_populates="sale_details")
    product: Mapped["Product"] = relationship("Product", back_populates="sale_details")
    product_category: Mapped["ProductCategory"] = relationship("ProductCategory", back_populates="sale_details")
    warehouse: Mapped["Warehouse"] = relationship("Warehouse", back_populates="sale_details")
    # refund_products: Mapped[list["RefundProduct"]] = relationship("RefundProduct", back_populates="sale_detail")
    attentions: Mapped[list["SaleDetailAttention"]] = relationship(
        "SaleDetailAttention", back_populates="sale_detail"
    )
