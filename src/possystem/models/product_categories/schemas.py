from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from ...types.products_categories import (
    CategoryNameStr,
    CategoryImageURL,
    IsCategoryActiveFlag
)


# Base schema (shared fields)
class ProductCategoryBase(BaseModel):
    name: CategoryNameStr = Field(...)
    image: Optional[CategoryImageURL] = None
    is_active: Optional[IsCategoryActiveFlag] = True


# Schema for creation
class ProductCategoryCreate(ProductCategoryBase):
    model_config = ConfigDict(
        extra= "forbid",
        json_schema_extra= {
            "example": {
                "name": "Bebidas",
                "image": "http://example.com/bebidas.png",
                "is_active": True
            }
        }
    )


# Schema for update (all optional)
class ProductCategoryUpdate(ProductCategoryBase):
    name: Optional[CategoryNameStr] = None

    model_config = ConfigDict(
        extra= "forbid",
        json_schema_extra= {
            "example": {
                "name": "Snacks",
                "image": "http://example.com/snacks.png",
                "is_active": False
            }
        }
    )


# Schema for response (basic)
class ProductCategoryResponse(ProductCategoryBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes= True,
        json_schema_extra= {
            "example": {
                "id": 1,
                "name": "Bebidas",
                "image": "http://example.com/bebidas.png",
                "is_active": True,
                "created_at": "2024-07-01T12:00:00",
                "updated_at": "2024-07-02T09:30:00",
            }
        }
    )


# Schema for detailed response (with relationships)
class ProductCategoryDetailsResponse(ProductCategoryResponse):
    products: Optional[List["ProductResponse"]] = None
    # sale_details: Optional[List["SaleDetailResponse"]] = None

    model_config = ConfigDict(
        from_attributes= True,
        json_schema_extra= {
            "example": {
                "id": 1,
                "name": "Bebidas",
                "image": "http://example.com/bebidas.png",
                "is_active": True,
                "created_at": "2024-07-01T12:00:00",
                "updated_at": "2024-07-02T09:30:00",
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
    )


# Schema for search filters
class ProductCategorySearchParams(BaseModel):
    name: Optional[str] = Field(None, max_length=250, description="Filtrar por nombre de categoría")
    is_active: Optional[bool] = Field(None, description="Filtrar por estado de la categoría")

    model_config = ConfigDict(
        extra= "forbid"
    )


# Forward reference resolution
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..products.schemas import ProductResponse
    from ..sales.schemas import SaleDetailResponse
