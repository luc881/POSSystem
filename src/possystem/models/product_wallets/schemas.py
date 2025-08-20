from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


# Base schema (shared fields)
class ProductWalletBase(BaseModel):
    type_client: int = Field(..., ge=1, le=2, description="Tipo de cliente (1 = final, 2 = empresa)")
    price: float = Field(..., gt=0, description="Precio asignado")
    product_id: int = Field(..., gt=0, description="ID del producto asociado")
    unit_id: int = Field(..., gt=0, description="ID de la unidad asociada")
    branch_id: int = Field(..., gt=0, description="ID de la sucursal asociada")


# Schema for creation
class ProductWalletCreate(ProductWalletBase):
    model_config = {
        "extra": "forbid",
        "json_schema_extra": {
            "example": {
                "type_client": 1,
                "price": 20.5,
                "product_id": 10,
                "unit_id": 2,
                "branch_id": 3
            }
        }
    }


# Schema for updating (all fields optional)
class ProductWalletUpdate(BaseModel):
    type_client: Optional[int] = Field(None, ge=1, le=2, description="Tipo de cliente (1 = final, 2 = empresa)")
    price: Optional[float] = Field(None, gt=0, description="Precio asignado")
    product_id: Optional[int] = Field(None, gt=0, description="ID del producto asociado")
    unit_id: Optional[int] = Field(None, gt=0, description="ID de la unidad asociada")
    branch_id: Optional[int] = Field(None, gt=0, description="ID de la sucursal asociada")
    deleted_at: Optional[datetime] = Field(None, description="Fecha de eliminación")

    model_config = {
        "extra": "forbid",
        "json_schema_extra": {
            "example": {
                "price": 22.0,
                "type_client": 2
            }
        }
    }


# Schema for response
class ProductWalletResponse(ProductWalletBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "type_client": 1,
                "price": 20.5,
                "product_id": 10,
                "unit_id": 2,
                "branch_id": 3,
                "created_at": "2024-07-01T12:00:00",
                "updated_at": "2024-07-02T09:30:00",
                "deleted_at": None
            }
        }
    }


# Schema for detailed response (with relationships)
class ProductWalletDetailsResponse(ProductWalletResponse):
    product: Optional["ProductResponse"] = None
    unit: Optional["UnitResponse"] = None
    branch: Optional["BranchResponse"] = None

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "type_client": 1,
                "price": 20.5,
                "created_at": "2024-07-01T12:00:00",
                "updated_at": "2024-07-02T09:30:00",
                "deleted_at": None,
                "product": {
                    "id": 10,
                    "name": "Refresco Cola 600ml",
                    "is_active": True
                },
                "unit": {
                    "id": 2,
                    "name": "Litro",
                    "description": "Unidad de volumen",
                    "is_active": True
                },
                "branch": {
                    "id": 3,
                    "name": "Sucursal Centro",
                    "address": "Av. Principal 123, CDMX",
                    "is_active": True
                }
            }
        }
    }


# Schema for search filters
class ProductWalletSearchParams(BaseModel):
    type_client: Optional[int] = Field(None, ge=1, le=2, description="Filtrar por tipo de cliente")
    product_id: Optional[int] = Field(None, gt=0, description="Filtrar por producto")
    unit_id: Optional[int] = Field(None, gt=0, description="Filtrar por unidad")
    branch_id: Optional[int] = Field(None, gt=0, description="Filtrar por sucursal")

    model_config = {
        "extra": "forbid"
    }


# Forward reference resolution
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..products.schemas import ProductResponse
    from ..units.schemas import UnitResponse
    from ..branches.schemas import BranchResponse
