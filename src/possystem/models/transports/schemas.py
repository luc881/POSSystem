from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


# -----------------------
# Base schema
# -----------------------
class TransportBase(BaseModel):
    warehouse_origin_id: int = Field(..., description="ID del almacén de origen")
    warehouse_destination_id: int = Field(..., description="ID del almacén de destino")
    user_id: int = Field(..., description="Usuario que registra la transferencia")

    state: int = Field(..., description="1=Request, 2=Revision, etc.")
    total: Optional[float] = Field(None, ge=0, description="Monto total")
    amount: Optional[float] = Field(None, ge=0, description="Importe sin impuestos")
    vat: Optional[float] = Field(None, ge=0, description="Impuesto (IVA)")
    description: Optional[str] = Field(None, description="Notas adicionales")

    emission_date: Optional[datetime] = Field(None, description="Fecha de emisión")
    delivery_date: Optional[datetime] = Field(None, description="Fecha de entrega")
    departure_date: Optional[datetime] = Field(None, description="Fecha de salida")


# -----------------------
# Create schema
# -----------------------
class TransportCreate(TransportBase):
    model_config = {
        "extra": "forbid",
        "json_schema_extra": {
            "example": {
                "warehouse_origin_id": 1,
                "warehouse_destination_id": 2,
                "user_id": 15,
                "state": 1,
                "total": 2500.75,
                "amount": 2120.0,
                "vat": 380.75,
                "description": "Traslado de equipo de cómputo",
                "emission_date": "2024-09-01T10:30:00",
                "departure_date": "2024-09-02T08:00:00",
                "delivery_date": None
            }
        }
    }


# -----------------------
# Update schema
# -----------------------
class TransportUpdate(BaseModel):
    warehouse_origin_id: Optional[int] = None
    warehouse_destination_id: Optional[int] = None
    user_id: Optional[int] = None
    state: Optional[int] = None
    total: Optional[float] = Field(None, ge=0)
    amount: Optional[float] = Field(None, ge=0)
    vat: Optional[float] = Field(None, ge=0)
    description: Optional[str] = None
    emission_date: Optional[datetime] = None
    delivery_date: Optional[datetime] = None
    departure_date: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    model_config = {
        "extra": "forbid",
        "json_schema_extra": {
            "example": {
                "state": 2,
                "departure_date": "2024-09-02T08:30:00",
                "delivery_date": "2024-09-02T12:00:00",
                "description": "Entrega parcial completada"
            }
        }
    }


# -----------------------
# Response schema
# -----------------------
class TransportResponse(TransportBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 101,
                "warehouse_origin_id": 1,
                "warehouse_destination_id": 2,
                "user_id": 15,
                "state": 2,
                "total": 2500.75,
                "amount": 2120.0,
                "vat": 380.75,
                "description": "Traslado de equipo de cómputo",
                "emission_date": "2024-09-01T10:30:00",
                "departure_date": "2024-09-02T08:30:00",
                "delivery_date": "2024-09-02T12:00:00",
                "created_at": "2024-09-01T10:30:00",
                "updated_at": "2024-09-02T12:00:00",
                "deleted_at": None
            }
        }
    }


# -----------------------
# With relations (expandable)
# -----------------------
class TransportWithRelations(TransportResponse):
    # To expand later:
    # user: Optional["UserResponse"]
    # warehouse_origin: Optional["WarehouseResponse"]
    # warehouse_destination: Optional["WarehouseResponse"]
    pass


# -----------------------
# Search params
# -----------------------
class TransportSearchParams(BaseModel):
    warehouse_origin_id: Optional[int] = None
    warehouse_destination_id: Optional[int] = None
    user_id: Optional[int] = None
    state: Optional[int] = None
    emission_date_from: Optional[datetime] = None
    emission_date_to: Optional[datetime] = None
    departure_date_from: Optional[datetime] = None
    departure_date_to: Optional[datetime] = None
    delivery_date_from: Optional[datetime] = None
    delivery_date_to: Optional[datetime] = None
