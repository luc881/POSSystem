from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


# -----------------------
# Base schema (shared fields)
# -----------------------
class SaleDetailAttentionBase(BaseModel):
    sale_detail_id: int = Field(..., gt=0, description="ID del detalle de venta")
    product_id: int = Field(..., gt=0, description="ID del producto")
    warehouse_id: int = Field(..., gt=0, description="ID del almacén")
    unit_id: int = Field(..., gt=0, description="ID de la unidad de medida")
    quantity: float = Field(..., gt=0, description="Cantidad atendida")


# -----------------------
# Create schema
# -----------------------
class SaleDetailAttentionCreate(SaleDetailAttentionBase):
    model_config = {
        "extra": "forbid",
        "json_schema_extra": {
            "example": {
                "sale_detail_id": 100,
                "product_id": 5,
                "warehouse_id": 2,
                "unit_id": 1,
                "quantity": 2
            }
        }
    }


# -----------------------
# Update schema (all optional)
# -----------------------
class SaleDetailAttentionUpdate(BaseModel):
    product_id: Optional[int] = Field(None, gt=0)
    warehouse_id: Optional[int] = Field(None, gt=0)
    unit_id: Optional[int] = Field(None, gt=0)
    quantity: Optional[float] = Field(None, gt=0)
    deleted_at: Optional[datetime] = None

    model_config = {
        "extra": "forbid",
        "json_schema_extra": {
            "example": {
                "quantity": 3
            }
        }
    }


# -----------------------
# Response schema
# -----------------------
class SaleDetailAttentionResponse(SaleDetailAttentionBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 10,
                "sale_detail_id": 100,
                "product_id": 5,
                "warehouse_id": 2,
                "unit_id": 1,
                "quantity": 2,
                "created_at": "2024-07-01T10:00:00",
                "updated_at": "2024-07-02T11:00:00",
                "deleted_at": None
            }
        }
    }


# -----------------------
# Response with relations
# -----------------------
class SaleDetailAttentionWithRelations(SaleDetailAttentionResponse):
    sale_detail: Optional["SaleDetailResponse"] = None
    product: Optional["ProductResponse"] = None
    warehouse: Optional["WarehouseResponse"] = None
    unit: Optional["UnitResponse"] = None

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 10,
                "sale_detail_id": 100,
                "product_id": 5,
                "warehouse_id": 2,
                "unit_id": 1,
                "quantity": 2,
                "created_at": "2024-07-01T10:00:00",
                "updated_at": "2024-07-02T11:00:00",
                "deleted_at": None,
                "sale_detail": {
                    "id": 100,
                    "quantity": 5,
                    "total": 250.0
                },
                "product": {
                    "id": 5,
                    "name": "Producto A",
                    "price": 50.0
                },
                "warehouse": {
                    "id": 2,
                    "name": "Almacén Central"
                },
                "unit": {
                    "id": 1,
                    "name": "Unidad"
                }
            }
        }
    }


# -----------------------
# Search params
# -----------------------
class SaleDetailAttentionSearchParams(BaseModel):
    sale_detail_id: Optional[int] = Field(None, gt=0, description="Filter by sale detail ID")
    product_id: Optional[int] = Field(None, gt=0, description="Filter by product ID")
    warehouse_id: Optional[int] = Field(None, gt=0, description="Filter by warehouse ID")
    unit_id: Optional[int] = Field(None, gt=0, description="Filter by unit ID")


# -----------------------
# Forward references
# -----------------------
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..sales.schemas import SaleDetailResponse
    from ..products.schemas import ProductResponse
    from ..warehouses.schemas import WarehouseResponse
    from ..units.schemas import UnitResponse
