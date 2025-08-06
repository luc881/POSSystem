from sqlalchemy import String, BigInteger, Boolean, TIMESTAMP
from sqlalchemy.sql import func
from ...db.session import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Branch(Base):
    __tablename__ = "branches"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped = mapped_column(TIMESTAMP(timezone=False), server_default=func.now())
    updated_at: Mapped = mapped_column(TIMESTAMP(timezone=False), onupdate=func.now())
    deleted_at: Mapped = mapped_column(TIMESTAMP(timezone=False), nullable=True)

    users: Mapped[list["User"]] = relationship("User", back_populates="branch")
    warehouses: Mapped[list["Warehouse"]] = relationship("Warehouse", back_populates="branch")
    product_wallets: Mapped[list["ProductWallet"]] = relationship("ProductWallet", back_populates="branch")
    clients: Mapped[list["Client"]] = relationship("Client", back_populates="branch")

