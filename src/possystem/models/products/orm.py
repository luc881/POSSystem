from sqlalchemy import (
    String, BigInteger, Double, Text, TIMESTAMP, Boolean, ForeignKey
)
from sqlalchemy.sql import func
from ...db.session import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    image: Mapped[str] = mapped_column(String(250), nullable=True)
    product_category_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("product_categories.id", ondelete="CASCADE"),
        nullable=True
    )

    # --- Precios ---
    price_retail: Mapped[float] = mapped_column(Double, nullable=False)  # precio normal
    price_cost: Mapped[float] = mapped_column(Double, nullable=False)    # precio de compra

    # --- Descripción y control ---
    description: Mapped[str] = mapped_column(Text, nullable=True)
    sku: Mapped[str] = mapped_column(String(100), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    allow_without_stock: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    # --- Descuentos / impuestos ---
    is_discount: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    max_discount: Mapped[float] = mapped_column(Double, nullable=True)  # %
    is_taxable: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    tax_percentage: Mapped[float] = mapped_column(Double, nullable=True)

    # --- Garantía ---
    allow_warranty: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    warranty_days: Mapped[float] = mapped_column(Double, nullable=True)

    # --- Unidades / fraccionamiento ---
    unit_name: Mapped[str] = mapped_column(String(50), nullable=False, default="pieza")
    base_unit_name: Mapped[str] = mapped_column(String(50), nullable=True)  # ej. “tableta”
    units_per_base: Mapped[float] = mapped_column(Double, nullable=True)    # ej. 10 = 1 caja → 10 tabletas

    # --- Tiempos ---
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=False), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=False), server_default=func.now(), onupdate=func.now()
    )

    # --- Relaciones ---
    category: Mapped["ProductCategory"] = relationship("ProductCategory", back_populates="products")
    sale_details: Mapped[list["SaleDetail"]] = relationship("SaleDetail", back_populates="product")
    refund_products: Mapped[list["RefundProduct"]] = relationship("RefundProduct", back_populates="product")
    purchase_details = relationship("PurchaseDetail", back_populates="product")
    batches: Mapped[list["ProductBatch"]] = relationship(
        "ProductBatch", back_populates="product", cascade="all, delete-orphan"
    )

# from sqlalchemy import String, BigInteger, Double, SmallInteger, Text, TIMESTAMP, Boolean, ForeignKey
# from sqlalchemy.sql import func
# from ...db.session import Base
# from sqlalchemy.orm import Mapped, mapped_column, relationship
# from datetime import datetime
#
#
# class Product(Base):
#     __tablename__ = "products"
#
#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
#     title: Mapped[str] = mapped_column(String(250), nullable=False)
#     image: Mapped[str] = mapped_column(String(250), nullable=True)
#     product_category_id: Mapped[int] = mapped_column(
#         BigInteger,
#         ForeignKey("product_categories.id", ondelete="CASCADE"),
#         nullable=True
#     )
#     price_retail: Mapped[float] = mapped_column(Double, nullable=False)
#     price_cost: Mapped[float] = mapped_column(Double, nullable=False)
#     description: Mapped[str] = mapped_column(Text, nullable=True)
#     is_discount: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
#     max_discount: Mapped[float] = mapped_column(Double, nullable=True)  # in %
#     is_gift: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
#     allow_without_stock: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
#     is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
#     allow_warranty: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
#     warranty_days: Mapped[float] = mapped_column(Double, nullable=True)
#     is_taxable: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
#     tax_percentage: Mapped[float] = mapped_column(Double, nullable=True)
#     created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=False), server_default=func.now())
#     updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=False), server_default=func.now(), onupdate=func.now())
#     sku: Mapped[str] = mapped_column(String(100), nullable=True)
#     # stock_state: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=1)  # 1 available, 2 low stock, 3 out of stock
#     # deleted_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=False), nullable=True)
#
#
#     category: Mapped["ProductCategory"] = relationship("ProductCategory", back_populates="products")
#     sale_details: Mapped[list["SaleDetail"]] = relationship("SaleDetail", back_populates="product")
#     refund_products: Mapped[list["RefundProduct"]] = relationship("RefundProduct", back_populates="product")
#     purchase_details = relationship("PurchaseDetail", back_populates="product")
#     batches: Mapped[list["ProductBatch"]] = relationship(
#         "ProductBatch", back_populates="product", cascade="all, delete-orphan"
#     )
#     # product_warehouses: Mapped[list["ProductWarehouse"]] = relationship("ProductWarehouse", back_populates="product")
#     # product_wallets: Mapped[list["ProductWallet"]] = relationship("ProductWallet", back_populates="product")
#     # transport_details: Mapped[list["TransportDetail"]] = relationship(
#     #     "TransportDetail", back_populates="product"
#     # )
#     # conversions: Mapped[list["Conversion"]] = relationship(
#     #     "Conversion", back_populates="product"
#     # )
#     # stock_initials: Mapped[list["ProductStockInitial"]] = relationship(
#     #     "ProductStockInitial", back_populates="product"
#     # )
#     # sale_detail_attentions: Mapped[list["SaleDetailAttention"]] = relationship(
#     #     "SaleDetailAttention", back_populates="product"
#     # )
