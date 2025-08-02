from sqlalchemy import BigInteger, ForeignKey
from ...db.session import Base
from sqlalchemy.orm import Mapped, mapped_column


class RoleHasPermission(Base):
    __tablename__ = "role_has_permissions"

    role_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("roles.id", ondelete="CASCADE"),
        primary_key=True
    )
    permission_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("permissions.id", ondelete="CASCADE"),
        primary_key=True
    )
