from enum import Enum
from typing import Annotated, Optional
from pydantic import StringConstraints, Field, HttpUrl
from pydantic.types import NonNegativeFloat


# -------------------------------
# 🔤 String types
# -------------------------------

ProductTitleStr = Annotated[
    str,
    StringConstraints(
        min_length=1,
        max_length=250,
        pattern=r"^[a-zA-Z0-9áéíóúÁÉÍÓÚñÑ\-.,'\"() ]+$"
    ),
    Field(description="Título del producto")
]

ProductDescriptionStr = Annotated[
    str,
    StringConstraints(
        max_length=2000
    ),
    Field(description="Descripción del producto")
]

ProductImageURL = Annotated[
    HttpUrl,
    StringConstraints(
        max_length=250,
    ),
    Field(description="Imagen del producto")
]

ProductSKUStr = Annotated[
    str,
    StringConstraints(
        min_length=1,
        max_length=100,
        pattern=r"^[A-Z0-9\-_.]+$"
    ),
    Field(description="Código SKU del producto")
]


# -------------------------------
# 💰 Numeric and price types
# -------------------------------

PriceRetail = Annotated[NonNegativeFloat, Field(description="Precio de venta al público")]
PriceCost = Annotated[NonNegativeFloat, Field(description="Precio de costo del producto")]
DiscountPercentage = Annotated[
    Optional[NonNegativeFloat],
    Field(le=100, description="Porcentaje de descuento máximo permitido")
]
TaxPercentage = Annotated[
    Optional[NonNegativeFloat],
    Field(le=100, description="Porcentaje de impuesto aplicado al producto")
]
WarrantyDays = Annotated[
    Optional[NonNegativeFloat],
    Field(description="Número de días de garantía del producto")
]


# -------------------------------
# ⚙️ Enumerations and state types
# -------------------------------

class StockStateEnum(int, Enum):
    AVAILABLE = 1     # Disponible
    LOW_STOCK = 2     # Bajo stock
    OUT_OF_STOCK = 3  # Agotado


# -------------------------------
# ⚡ Boolean flags (semánticos)
# -------------------------------

class ProductFlags:
    IS_DISCOUNT = Field(default=False, description="Indica si el producto tiene descuento")
    IS_GIFT = Field(default=False, description="Indica si puede ser usado como obsequio")
    ALLOW_WITHOUT_STOCK = Field(default=True, description="Permite venta sin stock")
    IS_ACTIVE = Field(default=True, description="Producto activo o desactivado")
    IS_TAXABLE = Field(default=True, description="Aplica impuesto o no")
    ALLOW_WARRANTY = Field(default=False, description="Aplica garantía o no")
