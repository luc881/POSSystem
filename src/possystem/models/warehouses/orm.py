from sqlalchemy import String, BigInteger, SmallInteger, TIMESTAMP, ForeignKey, Boolean
from sqlalchemy.sql import func
from ...db.session import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Warehouse(Base):
    __tablename__ = "warehouses"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    address: Mapped[str] = mapped_column(String(250), nullable=False)
    branch_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("branches.id"), nullable=False)  # FK to branches
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped = mapped_column(TIMESTAMP(timezone=False), server_default=func.now())
    updated_at: Mapped = mapped_column(TIMESTAMP(timezone=False), onupdate=func.now())
    deleted_at: Mapped = mapped_column(TIMESTAMP(timezone=False), nullable=True)

    branch: Mapped["Branch"] = relationship("Branch", back_populates="warehouses")
    product_warehouses: Mapped[list["ProductWarehouse"]] = relationship("ProductWarehouse", back_populates="warehouse")
    product_warehouses: Mapped[list["ProductWarehouse"]] = relationship("ProductWarehouse", back_populates="warehouse")
    sale_details: Mapped[list["SaleDetail"]] = relationship("SaleDetail", back_populates="warehouse")
    refund_products: Mapped[list["RefundProduct"]] = relationship("RefundProduct", back_populates="warehouse")
    purchases = relationship("Purchase", back_populates="warehouse")
    origin_transports: Mapped[list["Transport"]] = relationship(
        "Transport",
        back_populates="warehouse_origin",
        foreign_keys="[Transport.warehouse_origin_id]"
    )
    destination_transports: Mapped[list["Transport"]] = relationship(
        "Transport",
        back_populates="warehouse_destination",
        foreign_keys="[Transport.warehouse_destination_id]"
    )
