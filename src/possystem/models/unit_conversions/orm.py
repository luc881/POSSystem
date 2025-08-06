from sqlalchemy import BigInteger, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from ...db.session import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class UnitConversion(Base):
    __tablename__ = "unit_conversions"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    unit_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("units.id"), nullable=False)
    unit_to_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("units.id"), nullable=False)
    created_at: Mapped = mapped_column(TIMESTAMP(timezone=False), server_default=func.now())
    updated_at: Mapped = mapped_column(TIMESTAMP(timezone=False), onupdate=func.now())

    # Relationships
    unit: Mapped["Unit"] = relationship(
        "Unit", back_populates="conversions_from", foreign_keys=[unit_id]
    )
    unit_to: Mapped["Unit"] = relationship(
        "Unit", back_populates="conversions_to", foreign_keys=[unit_to_id]
    )
