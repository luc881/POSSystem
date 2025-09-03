from sqlalchemy import String, BigInteger, Integer, Double, Text, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from ...db.session import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime


class Transport(Base):
    __tablename__ = "transports"


    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    warehouse_origin_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("warehouses.id"), nullable=False)
    warehouse_destination_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("warehouses.id"), nullable=False)
    emission_date: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=False), nullable=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=False)
    state: Mapped[int] = mapped_column(Integer, nullable=False, default=1)  # 1=Request, 2=Revision, etc.
    total: Mapped[float] = mapped_column(Double, nullable=True)
    amount: Mapped[float] = mapped_column(Double, nullable=True)
    vat: Mapped[float] = mapped_column(Double, nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    delivery_date: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=False), nullable=True)
    departure_date: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=False), nullable=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=False), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=False), server_default=func.now(), onupdate=func.now())
    deleted_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=False), nullable=True)

    # Relationships
    # user: Mapped["User"] = relationship("User", back_populates="transports")
    # warehouse_origin: Mapped["Warehouse"] = relationship(
    #     "Warehouse",
    #     back_populates="origin_transports",
    #     foreign_keys=[warehouse_origin_id]
    # )
    # warehouse_destination: Mapped["Warehouse"] = relationship(
    #     "Warehouse",
    #     back_populates="destination_transports",
    #     foreign_keys=[warehouse_destination_id]
    # )
    # details: Mapped[list["TransportDetail"]] = relationship(
    #     "TransportDetail", back_populates="transport"
    # )

