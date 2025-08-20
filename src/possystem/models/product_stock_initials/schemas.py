from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


# Base schema (shared fields)
class ProductStockInitialBase(BaseModel):
    price_unit_avg: float = Field(..., gt=0, description="Precio unitario promedio")
    stock: float = Field(..., ge=0, description="Cantidad inicial en stock")
    product_id: Optional[int] = Field(None, gt=0, description="ID del producto asociado")
    unit_id: Optional[int] = Field(None, gt=0, description="ID de la unidad asociada")
    warehouse_id: Optional[int] = Field(None, gt=0, description="ID del almacén asociado")


# Schema for creation
class ProductStockInitialCreate(ProductStockInitialBase):
    model_config = {
        "extra": "forbid",
        "json_schema_extra": {
            "example": {
                "price_unit_avg": 25.5,
                "stock": 100.0,
                "product_id": 1,
                "unit_id": 2,
                "warehouse_id": 3
            }
        }
    }


# Schema for update (all optional)
class ProductStockInitialUpdate(BaseModel):
    price_unit_avg: Optional[float] = Field(None, gt=0, description="Precio unitario promedio")
    stock: Optional[float] = Field(None, ge=0, description="Cantidad inicial en stock")
    product_id: Optional[int] = Field(None, gt=0, description="ID del producto asociado")
    unit_id: Optional[int] = Field(None, gt=0, description="ID de la unidad asociada")
    warehouse_id: Optional[int] = Field(None, gt=0, description="ID del almacén asociado")
    deleted_at: Optional[datetime] = Field(None, description="Fecha de eliminación")

    model_config = {
        "extra": "forbid",
        "json_schema_extra": {
            "example": {
                "price_unit_avg": 30.0,
                "stock": 80.0,
                "unit_id": 5
            }
        }
    }


# Schema for response
class ProductStockInitialResponse(ProductStockInitialBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True,  # allows ORM mapping
        "json_schema_extra": {
            "example": {
                "id": 1,
                "price_unit_avg": 25.5,
                "stock": 100.0,
                "product_id": 1,
                "unit_id": 2,
                "warehouse_id": 3,
                "created_at": "2024-07-01T12:00:00",
                "updated_at": "2024-07-02T09:30:00",
                "deleted_at": None
            }
        }
    }


# Detailed response (with relationships)
class ProductStockInitialDetailsResponse(ProductStockInitialResponse):
    product: Optional["ProductResponse"] = None
    unit: Optional["UnitResponse"] = None
    warehouse: Optional["WarehouseResponse"] = None

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "price_unit_avg": 25.5,
                "stock": 100.0,
                "created_at": "2024-07-01T12:00:00",
                "updated_at": "2024-07-02T09:30:00",
                "deleted_at": None,
                "product": {
                    "id": 1,
                    "name": "Refresco Cola 600ml",
                    "is_active": True
                },
                "unit": {
                    "id": 2,
                    "name": "Litro",
                    "description": "Unidad de volumen",
                    "is_active": True
                },
                "warehouse": {
                    "id": 3,
                    "name": "Almacén Central",
                    "address": "Av. Insurgentes 123, CDMX",
                    "branch_id": 1,
                    "is_active": True
                }
            }
        }
    }


# Search filters
class ProductStockInitialSearchParams(BaseModel):
    product_id: Optional[int] = Field(None, gt=0, description="Filtrar por producto")
    unit_id: Optional[int] = Field(None, gt=0, description="Filtrar por unidad")
    warehouse_id: Optional[int] = Field(None, gt=0, description="Filtrar por almacén")

    model_config = {
        "extra": "forbid"
    }


# Forward reference resolution
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..products.schemas import ProductResponse
    from ..units.schemas import UnitResponse
    from ..warehouses.schemas import WarehouseResponse
