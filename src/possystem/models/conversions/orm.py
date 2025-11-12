from sqlalchemy import BigInteger, Double, Text, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from ...db.session import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

class Conversion(Base):
    __tablename__ = "conversions"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("products.id"), nullable=False)
    # warehouse_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("warehouses.id"), nullable=False)
    unit_start_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("units.id"), nullable=False)
    unit_end_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("units.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=False)
    quantity_start: Mapped[float] = mapped_column(Double, nullable=False)
    quantity_end: Mapped[float] = mapped_column(Double, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=False), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=False), server_default=func.now(),
                                                 onupdate=func.now())
    deleted_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=False), nullable=True)

    # Relationships
    product: Mapped["Product"] = relationship("Product", back_populates="conversions")
    unit_start: Mapped["Unit"] = relationship(
        "Unit", back_populates="conversions_from", foreign_keys=[unit_start_id]
    )
    unit_end: Mapped["Unit"] = relationship(
        "Unit", back_populates="conversions_to", foreign_keys=[unit_end_id]
    )
    user: Mapped["User"] = relationship("User", back_populates="conversions")
    # warehouse: Mapped["Warehouse"] = relationship("Warehouse", back_populates="conversions")
