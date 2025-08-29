from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


# -----------------------
# Base schema (shared fields)
# -----------------------
class SalePaymentBase(BaseModel):
    method_payment: str = Field(..., max_length=100, description="Método de pago utilizado")
    n_transaction: Optional[str] = Field(None, max_length=100, description="Número de transacción")
    bank: Optional[str] = Field(None, max_length=100, description="Banco emisor/receptor")
    amount: float = Field(..., gt=0, description="Monto del pago")


# -----------------------
# Create schema
# -----------------------
class SalePaymentCreate(SalePaymentBase):
    sale_id: int = Field(..., gt=0, description="ID de la venta asociada")

    model_config = {
        "extra": "forbid",
        "json_schema_extra": {
            "example": {
                "sale_id": 10,
                "method_payment": "Tarjeta de crédito",
                "n_transaction": "TX123456",
                "bank": "BBVA",
                "amount": 118.0
            }
        }
    }


# -----------------------
# Update schema (all optional)
# -----------------------
class SalePaymentUpdate(BaseModel):
    method_payment: Optional[str] = Field(None, max_length=100)
    n_transaction: Optional[str] = Field(None, max_length=100)
    bank: Optional[str] = Field(None, max_length=100)
    amount: Optional[float] = Field(None, gt=0)

    deleted_at: Optional[datetime] = None

    model_config = {
        "extra": "forbid",
        "json_schema_extra": {
            "example": {
                "method_payment": "Transferencia",
                "bank": "Santander",
                "amount": 118.0
            }
        }
    }


# -----------------------
# Response schema
# -----------------------
class SalePaymentResponse(SalePaymentBase):
    id: int
    sale_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 55,
                "sale_id": 10,
                "method_payment": "Tarjeta de crédito",
                "n_transaction": "TX123456",
                "bank": "BBVA",
                "amount": 118.0,
                "created_at": "2024-07-01T10:00:00",
                "updated_at": "2024-07-05T10:30:00",
                "deleted_at": None
            }
        }
    }


# -----------------------
# Response with relation
# -----------------------
class SalePaymentDetailsResponse(SalePaymentResponse):
    sale: Optional["SaleResponse"] = None

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 55,
                "method_payment": "Transferencia",
                "bank": "Santander",
                "amount": 118.0,
                "sale": {
                    "id": 10,
                    "total": 118.0,
                    "state_payment": 3
                }
            }
        }
    }


# -----------------------
# Search params
# -----------------------
class SalePaymentSearchParams(BaseModel):
    sale_id: Optional[int] = Field(None, gt=0, description="Filtrar por ID de venta")
    method_payment: Optional[str] = Field(None, max_length=100, description="Filtrar por método de pago")
    bank: Optional[str] = Field(None, max_length=100, description="Filtrar por banco")
    date_from: Optional[datetime] = Field(None, description="Filtrar desde esta fecha")
    date_to: Optional[datetime] = Field(None, description="Filtrar hasta esta fecha")


# -----------------------
# Forward references
# -----------------------
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..sales.schemas import SaleResponse
