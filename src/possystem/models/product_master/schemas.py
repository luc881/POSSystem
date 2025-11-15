from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

from ..product_categories.schemas import ProductCategoryResponse


# =========================================================
# 🔹 Base schema (campos compartidos)
# =========================================================
class ProductMasterBase(BaseModel):
    name: str = Field(..., max_length=250)
    description: Optional[str] = Field(None, max_length=2000)

    product_category_id: int = Field(..., gt=0, description="ID de la categoría del medicamento")


# =========================================================
# 🟢 Create schema
# =========================================================
class ProductMasterCreate(ProductMasterBase):
    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "name": "Paracetamol",
                "description": "Medicamento analgésico y antipirético.",
                "product_category_id": 2
            }
        }
    )


# =========================================================
# 🟡 Update schema (todos los campos opcionales)
# =========================================================
class ProductMasterUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=250)
    description: Optional[str] = Field(None, max_length=2000)
    product_category_id: Optional[int] = Field(None, gt=0)

    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "description": "Analgesico suave ampliamente utilizado",
                "product_category_id": 3
            }
        }
    )


# =========================================================
# 🔵 Response schema (sin relaciones)
# =========================================================
class ProductMasterResponse(ProductMasterBase):
    id: int
    created_at: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Paracetamol",
                "description": "Medicamento analgésico y antipirético.",
                "product_category_id": 2,
                "created_at": "2025-11-12T10:00:00"
            }
        }
    )


# =========================================================
# 🧩 Detailed response (con relaciones)
# =========================================================
class ProductMasterDetailsResponse(ProductMasterResponse):
    category: Optional[ProductCategoryResponse] = None
    products: Optional[List["ProductSimpleResponse"]] = None   # respuesta liviana de productos

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Paracetamol",
                "description": "Medicamento analgésico y antipirético.",
                "product_category_id": 2,
                "category": {"id": 2, "name": "Analgésicos", "is_active": True},
                "products": [
                    {
                        "id": 10,
                        "title": "Paracetamol 500mg caja 10 tabletas",
                        "sku": "PARA500-10TAB",
                        "price_retail": 35.0,
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
