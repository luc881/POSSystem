from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


# Base schema (shared fields)
class UnitBase(BaseModel):
    name: str = Field(..., max_length=250, description="Nombre de la unidad")
    description: Optional[str] = Field(None, description="Descripción de la unidad")
    is_active: Optional[bool] = Field(True, description="Estado de la unidad (True = activa, False = inactiva)")


# Schema for creation
class UnitCreate(UnitBase):
    model_config = {
        "extra": "forbid",
        "json_schema_extra": {
            "example": {
                "name": "Litro",
                "description": "Unidad de volumen",
                "is_active": True
            }
        }
    }


# Schema for updating (all fields optional)
class UnitUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=250, description="Nombre de la unidad")
    description: Optional[str] = Field(None, description="Descripción de la unidad")
    is_active: Optional[bool] = Field(None, description="Estado de la unidad (True = activa, False = inactiva)")
    deleted_at: Optional[datetime] = Field(None, description="Fecha de eliminación")

    model_config = {
        "extra": "forbid",
        "json_schema_extra": {
            "example": {
                "name": "Kilogramo",
                "description": "Unidad de peso",
                "is_active": False
            }
        }
    }


# Schema for response (includes id, timestamps)
class UnitResponse(UnitBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True,  # allows mapping directly from ORM
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "Litro",
                "description": "Unidad de volumen",
                "is_active": True,
                "created_at": "2024-07-01T12:00:00",
                "updated_at": "2024-07-02T09:30:00",
                "deleted_at": None
            }
        }
    }


# Schema for detailed response (with relationships)
class UnitDetailsResponse(UnitResponse):
    product_warehouses: Optional[list["ProductWarehouseResponse"]] = None
    product_wallets: Optional[list["ProductWalletResponse"]] = None

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "Litro",
                "description": "Unidad de volumen",
                "is_active": True,
                "created_at": "2024-07-01T12:00:00",
                "updated_at": "2024-07-02T09:30:00",
                "deleted_at": None,
                "product_warehouses": [
                    {
                        "id": 10,
                        "product_id": 5,
                        "warehouse_id": 2,
                        "quantity": 100
                    }
                ],
                "product_wallets": [
                    {
                        "id": 20,
                        "product_id": 5,
                        "wallet_id": 1,
                        "quantity": 50
                    }
                ]
            }
        }
    }


# Schema for search filters
class UnitSearchParams(BaseModel):
    name: Optional[str] = Field(None, max_length=250, description="Filtrar por nombre de unidad")
    is_active: Optional[bool] = Field(None, description="Filtrar por estado de la unidad")

    model_config = {
        "extra": "forbid"
    }


# Forward reference resolution (for relationships)
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..products.schemas import ProductWarehouseResponse, ProductWalletResponse
