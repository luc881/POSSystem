from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

from ..product_categories.schemas import ProductCategoryResponse
from ..products.schemas import ProductSimpleResponse


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
# 🟡 Update schema
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
# 🔵 Response simple
# =========================================================
class ProductMasterResponse(ProductMasterBase):
    id: int
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# =========================================================
# 🧩 Detailed response
# =========================================================
class ProductMasterDetailsResponse(ProductMasterResponse):
    category: Optional[ProductCategoryResponse] = None
    products: Optional[List[ProductSimpleResponse]] = None

    model_config = ConfigDict(from_attributes=True)



# =========================================================
# 🔁 Forward references
# =========================================================
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..products.schemas import ProductSimpleResponse
