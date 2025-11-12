from sqlalchemy import String, BigInteger, SmallInteger, Double, TIMESTAMP, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ...db.session import Base
from datetime import datetime

class Sale(Base):
    __tablename__ = "sales"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=True)
    branch_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("branches.id"), nullable=True)
    subtotal: Mapped[float] = mapped_column(Double, nullable=True)
    total: Mapped[float] = mapped_column(Double, nullable=True)
    discount: Mapped[float] = mapped_column(Double, nullable=True)
    tax: Mapped[float] = mapped_column(Double, nullable=True)  # igv Could rename to 'tax' if you prefer
    description: Mapped[str] = mapped_column(Text, nullable=True)
    date_sale: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=False), default=func.now())
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=False), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=False), server_default=func.now(), onupdate=func.now())
    # state_sale: Mapped[int] = mapped_column(SmallInteger, nullable=False)  # 1 = sale, 2 = quotation
    # date_validation: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=False), nullable=True)  # sale date
    # state_payment: Mapped[int] = mapped_column(SmallInteger, nullable=False)  # 1 = pending, 2 = partial, 3 = complete
    # date_pay_complete: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=False), nullable=True)
    # debt: Mapped[float] = mapped_column(Double, nullable=True)
    # paid_out: Mapped[float] = mapped_column(Double, nullable=True)  # paid or canceled
    # client_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("clients.id"), nullable=True)
    # type_client: Mapped[int] = mapped_column(SmallInteger, nullable=False)  # 1 = end customer, 2 = company
    # deleted_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=False), nullable=True)
    # state_delivery: Mapped[int] = mapped_column(SmallInteger, nullable=True)  # 1 = pending, 2 = partial, 3 = complete

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="sales")
    branch: Mapped["Branch"] = relationship("Branch", back_populates="sales")
    sale_details: Mapped[list["SaleDetail"]] = relationship("SaleDetail", back_populates="sale")
    sale_payments: Mapped[list["SalePayment"]] = relationship("SalePayment", back_populates="sale")
    # client: Mapped["Client"] = relationship("Client", back_populates="sales")

