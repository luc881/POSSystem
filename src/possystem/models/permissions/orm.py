from sqlalchemy import String, BigInteger, TIMESTAMP
from sqlalchemy.sql import func
from ...db.session import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Permission(Base):
    __tablename__ = "permissions"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    created_at: Mapped = mapped_column(TIMESTAMP(timezone=False), server_default=func.now())
    updated_at: Mapped = mapped_column(TIMESTAMP(timezone=False), onupdate=func.now())

    roles: Mapped[list["Role"]] = relationship(
        "Role",
        secondary="role_has_permissions",  # pivot table name
        back_populates="permissions"
    )
