from sqlalchemy import String, BigInteger, SmallInteger, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from POSSystem.src.possystem.db.session import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    surname: Mapped[str] = mapped_column(String(255), nullable=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    email_verified_at: Mapped = mapped_column(TIMESTAMP(timezone=False), nullable=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    remember_token: Mapped[str] = mapped_column(String(100), nullable=True)
    created_at: Mapped = mapped_column(TIMESTAMP(timezone=False), server_default=func.now())
    updated_at: Mapped = mapped_column(TIMESTAMP(timezone=False), onupdate=func.now())
    role_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("roles.id"), nullable=True)
    avatar: Mapped[str] = mapped_column(String(255), nullable=True)
    branch_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("branches.id"))
    phone: Mapped[str] = mapped_column(String(50), nullable=True)
    type_document: Mapped[str] = mapped_column(String(50), nullable=True)
    n_document: Mapped[str] = mapped_column(String(50), nullable=True)
    deleted_at: Mapped = mapped_column(TIMESTAMP(timezone=False), nullable=True)
    state: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=1)  # 1 = activo, 2 = inactivo
    gender: Mapped[str] = mapped_column(String(5), nullable=True)  # M = masculino, F = femenino

    # Relationship to Role
    role: Mapped["Role"] = relationship("Role", back_populates="users")
    # branch: Mapped["Branch"] = relationship("Branch", back_populates="users")
    # clients: Mapped[list["Client"]] = relationship("Client", back_populates="user")
    # sales: Mapped[list["Sale"]] = relationship("Sale", back_populates="user")
    # refund_products: Mapped[list["RefundProduct"]] = relationship("RefundProduct", back_populates="user")
    # purchases = relationship("Purchase", back_populates="user")
    # delivered_purchase_details = relationship(
    #     "PurchaseDetail",
    #     back_populates="user",
    #     foreign_keys="[PurchaseDetail.user_entrega]"
    # )
    # transports: Mapped[list["Transport"]] = relationship("Transport", back_populates="user")
    # delivered_transport_details: Mapped[list["TransportDetail"]] = relationship(
    #     "TransportDetail",
    #     back_populates="user_delivery",
    #     foreign_keys="[TransportDetail.user_delivery_id]"
    # )
    # departed_transport_details: Mapped[list["TransportDetail"]] = relationship(
    #     "TransportDetail",
    #     back_populates="user_departure",
    #     foreign_keys="[TransportDetail.user_departure_id]"
    # )
    # conversions: Mapped[list["Conversion"]] = relationship(
    #     "Conversion", back_populates="user"
    # )
