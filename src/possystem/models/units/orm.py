from sqlalchemy import String, BigInteger, Text, TIMESTAMP, Boolean
from sqlalchemy.sql import func
from ...db.session import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Unit(Base):
    __tablename__ = "units"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped = mapped_column(TIMESTAMP(timezone=False), server_default=func.now())
    updated_at: Mapped = mapped_column(TIMESTAMP(timezone=False), onupdate=func.now())
    deleted_at: Mapped = mapped_column(TIMESTAMP(timezone=False), nullable=True)

    product_warehouses: Mapped[list["ProductWarehouse"]] = relationship("ProductWarehouse", back_populates="unit")
    product_wallets: Mapped[list["ProductWallet"]] = relationship("ProductWallet", back_populates="unit")
    refund_products: Mapped[list["RefundProduct"]] = relationship("RefundProduct", back_populates="unit")
    purchase_details = relationship("PurchaseDetail", back_populates="unit")

