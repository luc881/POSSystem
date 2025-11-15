from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


# =========================================================
# 🔹 Base schema (campos compartidos)
# =========================================================
class ProductBrandBase(BaseModel):
    name: str = Field(..., max_length=200)
    logo: Optional[str] = Field(None, max_length=255)


# =========================================================
# 🟢 Create schema
# =========================================================
class ProductBrandCreate(ProductBrandBase):
    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "name": "Genoma Lab",
                "logo": "https://example.com/logos/genomalab.png"
            }
        }
    )


# =========================================================
# 🟡 Update schema (todos los campos opcionales)
# =========================================================
class ProductBrandUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=200)
    logo: Optional[str] = Field(None, max_length=255)

    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "logo": "https://example.com/logos/genomalab_v2.png"
            }
        }
    )


# =========================================================
# 🔵 Response schema (sin relaciones)
# =========================================================
class ProductBrandResponse(ProductBrandBase):
    id: int
    created_at: Optional[datetime]

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Genoma Lab",
                "logo": "https://example.com/logos/genomalab.png",
                "created_at": "2025-11-12T09:30:00"
            }
        }
    )


# =========================================================
# 🧩 Detailed response (con relación a productos)
# =========================================================
class ProductBrandDetailsResponse(ProductBrandResponse):
    products: Optional[List["ProductSimpleResponse"]] = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Genoma Lab",
                "logo": "https://example.com/logos/genomalab.png",
                "products": [
                    {
                        "id": 20,
                        "title": "Paracetamol 500mg Genoma Lab",
                        "sku": "PARA500-GEN",
                        "price_retail": 39.0,
                        "is_active": True
                    }
                ]
            }
        }
    )


# =========================================================
# 🔁 Forward references
# =========================================================
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..products.schemas import ProductSimpleResponse
