from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


# Base schema (shared fields)
class WarehouseBase(BaseModel):
    name: str = Field(..., max_length=250, description="Nombre del almacén")
    address: str = Field(..., max_length=250, description="Dirección del almacén")
    branch_id: Optional[int] = Field(None, gt=0, description="ID de la sucursal asociada")
    is_active: Optional[bool] = Field(True, description="Estado del almacén (True = activo, False = inactivo)")


# Schema for creation
class WarehouseCreate(WarehouseBase):
    model_config = {
        "extra": "forbid",
        "json_schema_extra": {
            "example": {
                "name": "Almacén Central",
                "address": "Av. Insurgentes 123, CDMX",
                "branch_id": 1,
                "is_active": True
            }
        }
    }


# Schema for updating (all optional)
class WarehouseUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=250, description="Nombre del almacén")
    address: Optional[str] = Field(None, max_length=250, description="Dirección del almacén")
    branch_id: Optional[int] = Field(None, gt=0, description="ID de la sucursal asociada")
    is_active: Optional[bool] = Field(None, description="Estado del almacén (True = activo, False = inactivo)")
    deleted_at: Optional[datetime] = Field(None, description="Fecha de eliminación")

    model_config = {
        "extra": "forbid",
        "json_schema_extra": {
            "example": {
                "name": "Almacén Secundario",
                "address": "Calle Reforma 456, Puebla",
                "branch_id": 2,
                "is_active": False
            }
        }
    }


# Schema for response (includes id, timestamps)
class WarehouseResponse(WarehouseBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True,  # allows mapping directly from ORM objects
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "Almacén Central",
                "address": "Av. Insurgentes 123, CDMX",
                "branch_id": 1,
                "is_active": True,
                "created_at": "2024-07-01T12:00:00",
                "updated_at": "2024-07-02T09:30:00",
                "deleted_at": None
            }
        }
    }


# Schema for detailed response (with branch info)
class WarehouseDetailsResponse(WarehouseResponse):
    branch: Optional["BranchResponse"] = None

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "Almacén Central",
                "address": "Av. Insurgentes 123, CDMX",
                "branch_id": 1,
                "is_active": True,
                "created_at": "2024-07-01T12:00:00",
                "updated_at": "2024-07-02T09:30:00",
                "deleted_at": None,
                "branch": {
                    "id": 1,
                    "name": "Sucursal Centro",
                    "address": "Av. Principal 123, CDMX",
                    "is_active": True,
                    "created_at": "2024-06-01T12:00:00",
                    "updated_at": "2024-06-02T10:00:00",
                    "deleted_at": None
                }
            }
        }
    }


# Schema for search filters
class WarehouseSearchParams(BaseModel):
    name: Optional[str] = Field(None, max_length=250, description="Filtrar por nombre")
    branch_id: Optional[int] = Field(None, gt=0, description="Filtrar por sucursal")
    is_active: Optional[bool] = Field(None, description="Filtrar por estado (True = activo, False = inactivo)")

    model_config = {
        "extra": "forbid"
    }


# Forward reference resolution
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..branches.schemas import BranchResponse
