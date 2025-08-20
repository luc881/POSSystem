from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


# Base schema (shared fields)
class ProductCategoryBase(BaseModel):
    name: str = Field(..., max_length=250, description="Nombre de la categoría de producto")
    image: Optional[str] = Field(None, max_length=250, description="URL de la imagen representativa")
    is_active: Optional[bool] = Field(True, description="Estado de la categoría (True = activa, False = inactiva)")


# Schema for creation
class ProductCategoryCreate(ProductCategoryBase):
    model_config = {
        "extra": "forbid",
        "json_schema_extra": {
            "example": {
                "name": "Bebidas",
                "image": "http://example.com/bebidas.png",
                "is_active": True
            }
        }
    }


# Schema for update (all optional)
class ProductCategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=250, description="Nombre de la categoría de producto")
    image: Optional[str] = Field(None, max_length=250, description="URL de la imagen representativa")
    is_active: Optional[bool] = Field(None, description="Estado de la categoría")
    deleted_at: Optional[datetime] = Field(None, description="Fecha de eliminación")

    model_config = {
        "extra": "forbid",
        "json_schema_extra": {
            "example": {
                "name": "Snacks",
                "image": "http://example.com/snacks.png",
                "is_active": False
            }
        }
    }


# Schema for response (basic)
class ProductCategoryResponse(ProductCategoryBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "Bebidas",
                "image": "http://example.com/bebidas.png",
                "is_active": True,
                "created_at": "2024-07-01T12:00:00",
                "updated_at": "2024-07-02T09:30:00",
                "deleted_at": None
            }
        }
    }


# Schema for detailed response (with relationships)
class ProductCategoryDetailsResponse(ProductCategoryResponse):
    products: Optional[List["ProductResponse"]] = None
    sale_details: Optional[List["SaleDetailResponse"]] = None

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "Bebidas",
                "image": "http://example.com/bebidas.png",
                "is_active": True,
                "created_at": "2024-07-01T12:00:00",
                "updated_at": "2024-07-02T09:30:00",
                "deleted_at": None,
                "products": [
                    {
                        "id": 10,
                        "name": "Refresco Cola 600ml",
                        "price": 15.5,
                        "is_active": True
                    }
                ],
                "sale_details": [
                    {
                        "id": 50,
                        "sale_id": 5,
                        "product_category_id": 1,
                        "quantity": 20,
                        "price": 310.0
                    }
                ]
            }
        }
    }


# Schema for search filters
class ProductCategorySearchParams(BaseModel):
    name: Optional[str] = Field(None, max_length=250, description="Filtrar por nombre de categoría")
    is_active: Optional[bool] = Field(None, description="Filtrar por estado de la categoría")

    model_config = {
        "extra": "forbid"
    }


# Forward reference resolution
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..products.schemas import ProductResponse
    from ..sales.schemas import SaleDetailResponse
