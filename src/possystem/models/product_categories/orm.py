from sqlalchemy import String, BigInteger, TIMESTAMP, Boolean
from sqlalchemy.sql import func
from ...db.session import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class ProductCategory(Base):
    __tablename__ = "product_categories"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    image: Mapped[str] = mapped_column(String(250), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped = mapped_column(TIMESTAMP(timezone=False), server_default=func.now())
    updated_at: Mapped = mapped_column(TIMESTAMP(timezone=False), onupdate=func.now())
    deleted_at: Mapped = mapped_column(TIMESTAMP(timezone=False), nullable=True)

    # Relationship with products
    products: Mapped[list["Product"]] = relationship("Product", back_populates="category")

