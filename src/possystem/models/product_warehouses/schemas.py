from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


# Base schema (shared fields)
class ProductWarehouseBase(BaseModel):
    product_id: int = Field(..., gt=0, description="ID del producto asociado")
    warehouse_id: int = Field(..., gt=0, description="ID del almacén asociado")
    unit_id: int = Field(..., gt=0, description="ID de la unidad asociada")
    stock: float = Field(..., ge=0, description="Stock actual")
    threshold: float = Field(..., ge=0, description="Umbral mínimo para alerta de bajo stock")
    state_stock: int = Field(..., ge=1, le=3, description="Estado del stock (1 = disponible, 2 = bajo, 3 = agotado)")


# Schema for creation
class ProductWarehouseCreate(ProductWarehouseBase):
    model_config = {
        "extra": "forbid",
        "json_schema_extra": {
            "example": {
                "product_id": 1,
                "warehouse_id": 2,
                "unit_id": 3,
                "stock": 120.0,
                "threshold": 20.0,
                "state_stock": 1
            }
        }
    }


# Schema for update (all optional)
class ProductWarehouseUpdate(BaseModel):
    product_id: Optional[int] = Field(None, gt=0, description="ID del producto asociado")
    warehouse_id: Optional[int] = Field(None, gt=0, description="ID del almacén asociado")
    unit_id: Optional[int] = Field(None, gt=0, description="ID de la unidad asociada")
    stock: Optional[float] = Field(None, ge=0, description="Stock actual")
    threshold: Optional[float] = Field(None, ge=0, description="Umbral mínimo para alerta de bajo stock")
    state_stock: Optional[int] = Field(None, ge=1, le=3, description="Estado del stock (1 = disponible, 2 = bajo, 3 = agotado)")
    deleted_at: Optional[datetime] = Field(None, description="Fecha de eliminación")

    model_config = {
        "extra": "forbid",
        "json_schema_extra": {
            "example": {
                "stock": 50.0,
                "threshold": 10.0,
                "state_stock": 2
            }
        }
    }


# Schema for response
class ProductWarehouseResponse(ProductWarehouseBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True,  # ORM mode
        "json_schema_extra": {
            "example": {
                "id": 1,
                "product_id": 1,
                "warehouse_id": 2,
                "unit_id": 3,
                "stock": 120.0,
                "threshold": 20.0,
                "state_stock": 1,
                "created_at": "2024-07-01T12:00:00",
                "updated_at": "2024-07-02T09:30:00",
                "deleted_at": None
            }
        }
    }


# Schema for detailed response (with relationships)
class ProductWarehouseDetailsResponse(ProductWarehouseResponse):
    product: Optional["ProductResponse"] = None
    warehouse: Optional["WarehouseResponse"] = None
    unit: Optional["UnitResponse"] = None

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "stock": 120.0,
                "threshold": 20.0,
                "state_stock": 1,
                "created_at": "2024-07-01T12:00:00",
                "updated_at": "2024-07-02T09:30:00",
                "deleted_at": None,
                "product": {
                    "id": 1,
                    "name": "Refresco Cola 600ml",
                    "is_active": True
                },
                "warehouse": {
                    "id": 2,
                    "name": "Almacén Central",
                    "address": "Av. Insurgentes 123, CDMX",
                    "is_active": True
                },
                "unit": {
                    "id": 3,
                    "name": "Litro",
                    "description": "Unidad de volumen",
                    "is_active": True
                }
            }
        }
    }


# Schema for search filters
class ProductWarehouseSearchParams(BaseModel):
    product_id: Optional[int] = Field(None, gt=0, description="Filtrar por producto")
    warehouse_id: Optional[int] = Field(None, gt=0, description="Filtrar por almacén")
    unit_id: Optional[int] = Field(None, gt=0, description="Filtrar por unidad")
    state_stock: Optional[int] = Field(None, ge=1, le=3, description="Filtrar por estado del stock")

    model_config = {
        "extra": "forbid"
    }


# Forward reference resolution
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..products.schemas import ProductResponse
    from ..warehouses.schemas import WarehouseResponse
    from ..units.schemas import UnitResponse
