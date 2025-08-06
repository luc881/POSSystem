from sqlalchemy import BigInteger, Double, SmallInteger, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from ...db.session import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class ProductWallet(Base):
    __tablename__ = "product_wallets"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("products.id"), nullable=False)
    type_client: Mapped[int] = mapped_column(SmallInteger, nullable=False)  # 1 = final client, 2 = company client
    unit_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("units.id"), nullable=False)
    branch_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("branches.id"), nullable=False)
    price: Mapped[float] = mapped_column(Double, nullable=False)
    created_at: Mapped = mapped_column(TIMESTAMP(timezone=False), server_default=func.now())
    updated_at: Mapped = mapped_column(TIMESTAMP(timezone=False), onupdate=func.now())
    deleted_at: Mapped = mapped_column(TIMESTAMP(timezone=False), nullable=True)

    # Relationships
    product: Mapped["Product"] = relationship("Product", back_populates="product_wallets")
    unit: Mapped["Unit"] = relationship("Unit", back_populates="product_wallets")
    branch: Mapped["Branch"] = relationship("Branch", back_populates="product_wallets")
