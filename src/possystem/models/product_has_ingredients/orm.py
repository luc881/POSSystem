from sqlalchemy import Table, Column, ForeignKey, BigInteger, String
from ...db.session import Base

product_has_ingredients = Table(
    "product_has_ingredients",
    Base.metadata,
    Column("product_id", BigInteger, ForeignKey("products.id", ondelete="CASCADE"), primary_key=True),
    Column("ingredient_id", BigInteger, ForeignKey("ingredients.id", ondelete="CASCADE"), primary_key=True),

    # Cantidad de ingrediente, ej: "500 mg", "5%"
    Column("amount", String(50), nullable=True)
)
