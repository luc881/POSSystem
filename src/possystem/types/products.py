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
# ⚖️ Unidades y fraccionamiento
# -------------------------------

ProductUnitName = Annotated[
    str,
    StringConstraints(
        min_length=1,
        max_length=50,
        pattern=r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+$"
    ),
    Field(description="Nombre de la unidad principal (ej. pieza, caja)")
]

ProductBaseUnitName = Annotated[
    str,
    StringConstraints(
        min_length=1,
        max_length=50,
        pattern=r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+$"
    ),
    Field(description="Nombre de la unidad base o fraccionada (ej. tableta, sobre)")
]

UnitsPerBase = Annotated[
    NonNegativeFloat,
    Field(gt=0, description="Cantidad de unidades base por unidad principal (ej. 10 = 1 caja contiene 10 tabletas)")
]


# -------------------------------
# 💰 Numeric and price types
# -------------------------------

PriceRetail = Annotated[
    NonNegativeFloat,
    Field(description="Precio de venta al público")
]

PriceCost = Annotated[
    NonNegativeFloat,
    Field(description="Precio de costo del producto")
]

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

IsDiscountFlag = Annotated[
    bool,
    Field(description="Indica si el producto tiene descuento")
]

IsGiftFlag = Annotated[
    bool,
    Field(description="Indica si puede ser usado como obsequio")
]

AllowWithoutStockFlag = Annotated[
    bool,
    Field(description="Permite venta sin stock")
]

IsActiveFlag = Annotated[
    bool,
    Field(description="Producto activo o desactivado")
]

IsTaxableFlag = Annotated[
    bool,
    Field(description="Aplica impuesto o no")
]

AllowWarrantyFlag = Annotated[
    bool,
    Field(description="Aplica garantía o no")
]
