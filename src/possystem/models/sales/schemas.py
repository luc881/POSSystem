from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


# -----------------------
# Base schema (shared fields)
# -----------------------
class SaleBase(BaseModel):
    user_id: Optional[int] = Field(None, gt=0, description="ID del usuario asociado")
    client_id: Optional[int] = Field(None, gt=0, description="ID del cliente asociado")
    type_client: int = Field(..., ge=1, le=2, description="Tipo de cliente (1 = final, 2 = empresa)")
    branch_id: Optional[int] = Field(None, gt=0, description="ID de la sucursal")

    subtotal: Optional[float] = Field(None, description="Subtotal de la venta")
    total: Optional[float] = Field(None, description="Total de la venta")
    tax: Optional[float] = Field(None, description="Impuesto aplicado (IGV)")
    discount: Optional[float] = Field(None, description="Descuento aplicado")

    state_sale: int = Field(..., ge=1, le=2, description="Estado de la venta (1 = venta, 2 = cotización)")
    state_payment: int = Field(..., ge=1, le=3, description="Estado de pago (1 = pendiente, 2 = parcial, 3 = completo)")
    state_delivery: Optional[int] = Field(None, ge=1, le=3, description="Estado de entrega (1 = pendiente, 2 = parcial, 3 = completo)")

    debt: Optional[float] = Field(None, description="Deuda restante")
    paid_out: Optional[float] = Field(None, description="Monto pagado o cancelado")

    date_validation: Optional[datetime] = Field(None, description="Fecha de validación (venta)")
    date_pay_complete: Optional[datetime] = Field(None, description="Fecha de pago completo")
    description: Optional[str] = Field(None, description="Descripción de la venta")


# -----------------------
# Create schema
# -----------------------
class SaleCreate(SaleBase):
    model_config = {
        "extra": "forbid",
        "json_schema_extra": {
            "example": {
                "user_id": 1,
                "client_id": 3,
                "type_client": 1,
                "branch_id": 2,
                "subtotal": 100.0,
                "total": 118.0,
                "tax": 18.0,
                "discount": 5.0,
                "state_sale": 1,
                "state_payment": 1,
                "state_delivery": 1,
                "debt": 118.0,
                "paid_out": 0.0,
                "description": "Venta de producto A"
            }
        }
    }


# -----------------------
# Update schema (all optional)
# -----------------------
class SaleUpdate(BaseModel):
    user_id: Optional[int] = Field(None, gt=0)
    client_id: Optional[int] = Field(None, gt=0)
    type_client: Optional[int] = Field(None, ge=1, le=2)
    branch_id: Optional[int] = Field(None, gt=0)

    subtotal: Optional[float] = None
    total: Optional[float] = None
    tax: Optional[float] = None
    discount: Optional[float] = None

    state_sale: Optional[int] = Field(None, ge=1, le=2)
    state_payment: Optional[int] = Field(None, ge=1, le=3)
    state_delivery: Optional[int] = Field(None, ge=1, le=3)

    debt: Optional[float] = None
    paid_out: Optional[float] = None

    date_validation: Optional[datetime] = None
    date_pay_complete: Optional[datetime] = None
    description: Optional[str] = None

    deleted_at: Optional[datetime] = None

    model_config = {
        "extra": "forbid",
        "json_schema_extra": {
            "example": {
                "state_payment": 2,
                "paid_out": 50.0,
                "debt": 68.0
            }
        }
    }


# -----------------------
# Response schema
# -----------------------
class SaleResponse(SaleBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 10,
                "user_id": 1,
                "client_id": 3,
                "type_client": 1,
                "branch_id": 2,
                "subtotal": 100.0,
                "total": 118.0,
                "tax": 18.0,
                "discount": 5.0,
                "state_sale": 1,
                "state_payment": 1,
                "state_delivery": 1,
                "debt": 118.0,
                "paid_out": 0.0,
                "description": "Venta de producto A",
                "created_at": "2024-07-01T10:00:00",
                "updated_at": "2024-07-05T10:30:00",
                "deleted_at": None
            }
        }
    }


# -----------------------
# Response with relations
# -----------------------
class SaleDetailsResponse(SaleResponse):
    user: Optional["UserResponse"] = None
    client: Optional["ClientResponse"] = None
    branch: Optional["BranchResponse"] = None

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 10,
                "total": 118.0,
                "tax": 18.0,
                "state_sale": 1,
                "state_payment": 2,
                "state_delivery": 1,
                "debt": 68.0,
                "paid_out": 50.0,
                "created_at": "2024-07-01T10:00:00",
                "updated_at": "2024-07-05T10:30:00",
                "deleted_at": None,
                "branch": {
                    "id": 2,
                    "name": "Sucursal Centro",
                    "address": "Av. Principal 123, CDMX",
                    "is_active": True
                },
                "user": {
                    "id": 1,
                    "name": "Juan",
                    "surname": "Pérez",
                    "email": "juan.perez@example.com"
                },
                "client": {
                    "id": 3,
                    "name": "Carlos",
                    "surname": "Ramírez",
                    "email": "carlos.ramirez@example.com"
                }
            }
        }
    }


# -----------------------
# Search params
# -----------------------
class SaleSearchParams(BaseModel):
    user_id: Optional[int] = Field(None, gt=0, description="Filter by user ID")
    client_id: Optional[int] = Field(None, gt=0, description="Filter by client ID")
    branch_id: Optional[int] = Field(None, gt=0, description="Filter by branch ID")
    state_sale: Optional[int] = Field(None, ge=1, le=2, description="Filter by sale state")
    state_payment: Optional[int] = Field(None, ge=1, le=3, description="Filter by payment state")
    state_delivery: Optional[int] = Field(None, ge=1, le=3, description="Filter by delivery state")
    date_validation: Optional[datetime] = Field(None, description="Filter by validation date")


# -----------------------
# Forward references
# -----------------------
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..users.schemas import UserResponse
    from ..clients.schemas import ClientResponse
    from ..branches.schemas import BranchResponse
