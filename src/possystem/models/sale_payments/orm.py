from sqlalchemy import String, BigInteger, Double, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ...db.session import Base
from datetime import datetime

class SalePayment(Base):
    __tablename__ = "sale_payments"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    sale_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("sales.id"), nullable=False)
    method_payment: Mapped[str] = mapped_column(String(100), nullable=False)
    n_transaction: Mapped[str] = mapped_column(String(100), nullable=True)
    bank: Mapped[str] = mapped_column(String(100), nullable=True)
    amount: Mapped[float] = mapped_column(Double, nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=False), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=False), server_default=func.now(),onupdate=func.now())
    deleted_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=False), nullable=True)

    # Relationship
    sale: Mapped["Sale"] = relationship("Sale", back_populates="sale_payments")
