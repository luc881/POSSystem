from sqlalchemy import String, BigInteger, Double, Date, ForeignKey, Integer, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from ...db.session import Base


class ProductBatch(Base):
    __tablename__ = "product_batches"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False
    )
    lot_code: Mapped[str] = mapped_column(String(100), nullable=True)  # opcional, si la farmacia usa código de lote
    expiration_date: Mapped[datetime] = mapped_column(Date, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    purchase_price: Mapped[float] = mapped_column(Double, nullable=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())

    product: Mapped["Product"] = relationship("Product", back_populates="batches")
