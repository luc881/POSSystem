from sqlalchemy import String, BigInteger, SmallInteger, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ...db.session import Base
from datetime import datetime

class Client(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(250), nullable=True)
    surname: Mapped[str] = mapped_column(String(250), nullable=True)
    full_name: Mapped[str] = mapped_column(String(250), nullable=True)
    phone: Mapped[str] = mapped_column(String(35), nullable=True)
    email: Mapped[str] = mapped_column(String(250), nullable=True)
    type_client: Mapped[int] = mapped_column(SmallInteger, nullable=False)  # 1 = cliente final, 2 = empresa
    type_document: Mapped[str] = mapped_column(String(200), nullable=True)
    n_document: Mapped[str] = mapped_column(String(100), nullable=True, unique=True)
    birth_date: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=False), nullable=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=True)
    branch_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("branches.id"), nullable=True)
    state: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=1)  # 1 = activo, 2 = inactivo

    ubigeo_region: Mapped[str] = mapped_column(String(25), nullable=True)
    ubigeo_provincia: Mapped[str] = mapped_column(String(25), nullable=True)
    ubigeo_distrito: Mapped[str] = mapped_column(String(25), nullable=True)
    region: Mapped[str] = mapped_column(String(100), nullable=True)
    provincia: Mapped[str] = mapped_column(String(100), nullable=True)
    distrito: Mapped[str] = mapped_column(String(100), nullable=True)
    address: Mapped[str] = mapped_column(String(250), nullable=True)

    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=False), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=False), server_default=func.now(), onupdate=func.now())
    deleted_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=False), nullable=True)
    gender: Mapped[str] = mapped_column(String(4), nullable=True)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="clients")
    branch: Mapped["Branch"] = relationship("Branch", back_populates="clients")
    sales: Mapped[list["Sale"]] = relationship("Sale", back_populates="client")
    refund_products: Mapped[list["RefundProduct"]] = relationship("RefundProduct", back_populates="client")
