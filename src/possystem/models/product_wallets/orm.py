from sqlalchemy import BigInteger, Double, SmallInteger, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from ...db.session import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class ProductWallet(Base):
    __tablename__ = "product_wallets"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    type_client: Mapped[int] = mapped_column(SmallInteger, nullable=False)  # 1 = final client, 2 = company client
    price: Mapped[float] = mapped_column(Double, nullable=False)
    product_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("products.id"), nullable=False)
    unit_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("units.id"), nullable=False)
    branch_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("branches.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=False), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=False), server_default=func.now(), onupdate=func.now())
    deleted_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=False), nullable=True)

    # Relationships
    product: Mapped["Product"] = relationship("Product", back_populates="product_wallets")
    unit: Mapped["Unit"] = relationship("Unit", back_populates="product_wallets")
    branch: Mapped["Branch"] = relationship("Branch", back_populates="product_wallets")
