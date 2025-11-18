from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

from ..products.schemas import ProductSimpleResponse


# =========================================================
# 🔹 Base schema
# =========================================================
class ProductBrandBase(BaseModel):
    name: str = Field(..., max_length=200)
    logo: Optional[str] = Field(None, max_length=255)


# =========================================================
# 🟢 Create
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
# 🟡 Update
# =========================================================
class ProductBrandUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=200)
    logo: Optional[str] = Field(None, max_length=255)

    model_config = ConfigDict(extra="forbid")


# =========================================================
# 🔵 Response simple
# =========================================================
class ProductBrandResponse(ProductBrandBase):
    id: int
    created_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)


# =========================================================
# 🧩 Detailed response (con productos)
# =========================================================
class ProductBrandDetailsResponse(ProductBrandResponse):
    products: Optional[List[ProductSimpleResponse]] = None

    model_config = ConfigDict(from_attributes=True)



# =========================================================
# 🔁 Forward references
# =========================================================
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..products.schemas import ProductSimpleResponse
