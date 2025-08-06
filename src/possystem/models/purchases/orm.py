from sqlalchemy import (
    Column, BigInteger, SmallInteger, String, Double, Text, TIMESTAMP, ForeignKey
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func
from ...db.session import Base

class Purchase(Base):
    __tablename__ = "purchases"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    warehouse_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("warehouses.id"))
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    branch_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("branches.id"))
    date_emision: Mapped = mapped_column(TIMESTAMP(timezone=False))
    state: Mapped[int] = mapped_column(SmallInteger, comment="1=SOLICITUD, 2=REVISION, 3=PARCIAL, 4=ENTREGADO")
    type_comprobant: Mapped[str] = mapped_column(String(100))
    n_comprobant: Mapped[str] = mapped_column(String(100))
    supplier_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("suppliers.id"))
    total: Mapped[float] = mapped_column(Double)
    importe: Mapped[float] = mapped_column(Double)
    igv: Mapped[float] = mapped_column(Double)
    date_entrega: Mapped = mapped_column(TIMESTAMP(timezone=False))
    created_at: Mapped = mapped_column(TIMESTAMP(timezone=False), server_default=func.now())
    updated_at: Mapped = mapped_column(TIMESTAMP(timezone=False), onupdate=func.now())
    deleted_at: Mapped = mapped_column(TIMESTAMP(timezone=False), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    # Relationships (assuming you have these models)
    warehouse = relationship("Warehouse", back_populates="purchases")
    user = relationship("User", back_populates="purchases")
    branch = relationship("Branch", back_populates="purchases")
    supplier = relationship("Supplier", back_populates="purchases")


