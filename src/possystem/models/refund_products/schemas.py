from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


# -----------------------
# Base schema
# -----------------------
class RefundProductBase(BaseModel):
    product_id: int = Field(..., gt=0, description="ID del producto")
    quantity: float = Field(..., gt=0, description="Cantidad a devolver")
    type: int = Field(..., ge=1, le=3, description="1=Repair, 2=Replacement, 3=Return")
    state: int = Field(..., ge=1, le=4, description="1=Pending, 2=Review, 3=Repaired, 4=Discarded")

    unit_id: Optional[int] = Field(None, gt=0, description="Unidad de medida")
    warehouse_id: Optional[int] = Field(None, gt=0, description="Almacén de devolución")
    sale_detail_id: Optional[int] = Field(None, gt=0, description="Detalle de venta relacionado")
    client_id: Optional[int] = Field(None, gt=0, description="Cliente relacionado")
    description: Optional[str] = Field(None, description="Descripción del problema")
    user_id: Optional[int] = Field(None, gt=0, description="Usuario que registró la devolución")
    resolution_date: Optional[datetime] = Field(None, description="Fecha de resolución")
    description_resolution: Optional[str] = Field(None, description="Descripción de la resolución")
    state_clone: Optional[int] = Field(None, description="Estado de clonación (backup)")


# -----------------------
# Create schema
# -----------------------
class RefundProductCreate(RefundProductBase):
    model_config = {
        "extra": "forbid",
        "json_schema_extra": {
            "example": {
                "product_id": 12,
                "unit_id": 1,
                "warehouse_id": 2,
                "quantity": 3,
                "sale_detail_id": 100,
                "client_id": 55,
                "type": 2,
                "state": 1,
                "description": "Producto con defecto de fábrica",
                "user_id": 10
            }
        }
    }


# -----------------------
# Update schema
# -----------------------
class RefundProductUpdate(BaseModel):
    product_id: Optional[int] = Field(None, gt=0)
    unit_id: Optional[int] = Field(None, gt=0)
    warehouse_id: Optional[int] = Field(None, gt=0)
    quantity: Optional[float] = Field(None, gt=0)
    sale_detail_id: Optional[int] = Field(None, gt=0)
    client_id: Optional[int] = Field(None, gt=0)
    type: Optional[int] = Field(None, ge=1, le=3)
    state: Optional[int] = Field(None, ge=1, le=4)
    description: Optional[str] = None
    user_id: Optional[int] = Field(None, gt=0)
    resolution_date: Optional[datetime] = None
    description_resolution: Optional[str] = None
    state_clone: Optional[int] = None
    deleted_at: Optional[datetime] = None

    model_config = {
        "extra": "forbid",
        "json_schema_extra": {
            "example": {
                "state": 3,
                "resolution_date": "2024-07-15T15:30:00",
                "description_resolution": "Producto reparado con éxito"
            }
        }
    }


# -----------------------
# Response schema
# -----------------------
class RefundProductResponse(RefundProductBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 200,
                "product_id": 12,
                "unit_id": 1,
                "warehouse_id": 2,
                "quantity": 3,
                "sale_detail_id": 100,
                "client_id": 55,
                "type": 2,
                "state": 3,
                "description": "Producto con defecto de fábrica",
                "user_id": 10,
                "resolution_date": "2024-07-15T15:30:00",
                "description_resolution": "Producto reparado con éxito",
                "created_at": "2024-07-01T10:00:00",
                "updated_at": "2024-07-15T16:00:00",
                "deleted_at": None,
                "state_clone": None
            }
        }
    }


# -----------------------
# With relations
# -----------------------
class RefundProductWithRelations(RefundProductResponse):
    product: Optional["ProductResponse"] = None
    unit: Optional["UnitResponse"] = None
    warehouse: Optional["WarehouseResponse"] = None
    sale_detail: Optional["SaleDetailResponse"] = None
    client: Optional["ClientResponse"] = None
    user: Optional["UserResponse"] = None

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 200,
                "product_id": 12,
                "unit_id": 1,
                "warehouse_id": 2,
                "quantity": 3,
                "sale_detail_id": 100,
                "client_id": 55,
                "type": 2,
                "state": 3,
                "description": "Producto con defecto de fábrica",
                "user_id": 10,
                "resolution_date": "2024-07-15T15:30:00",
                "description_resolution": "Producto reparado con éxito",
                "created_at": "2024-07-01T10:00:00",
                "updated_at": "2024-07-15T16:00:00",
                "deleted_at": None,
                "state_clone": None,
                "product": {"id": 12, "name": "Laptop X"},
                "unit": {"id": 1, "name": "Unidad"},
                "warehouse": {"id": 2, "name": "Almacén Central"},
                "sale_detail": {"id": 100, "total": 500.0},
                "client": {"id": 55, "name": "Cliente A"},
                "user": {"id": 10, "username": "admin"}
            }
        }
    }


# -----------------------
# Search params
# -----------------------
class RefundProductSearchParams(BaseModel):
    product_id: Optional[int] = None
    client_id: Optional[int] = None
    state: Optional[int] = None
    type: Optional[int] = None
    warehouse_id: Optional[int] = None
    user_id: Optional[int] = None


# -----------------------
# Forward references
# -----------------------
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..products.schemas import ProductResponse
    from ..units.schemas import UnitResponse
    from ..warehouses.schemas import WarehouseResponse
    from ..sales.schemas import SaleDetailResponse
    from ..clients.schemas import ClientResponse
    from ..users.schemas import UserResponse
