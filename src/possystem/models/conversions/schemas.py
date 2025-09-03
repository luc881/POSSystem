from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


# -----------------------
# Base schema
# -----------------------
class ConversionBase(BaseModel):
    product_id: int = Field(..., description="ID del producto")
    warehouse_id: int = Field(..., description="ID del almacén")
    unit_start_id: int = Field(..., description="Unidad de inicio (ej. caja)")
    unit_end_id: int = Field(..., description="Unidad de destino (ej. pieza)")
    user_id: int = Field(..., description="Usuario que realizó la conversión")

    quantity_start: float = Field(..., gt=0, description="Cantidad en unidad de inicio")
    quantity_end: float = Field(..., gt=0, description="Cantidad en unidad de destino")
    description: Optional[str] = Field(None, description="Notas de la conversión")


# -----------------------
# Create schema
# -----------------------
class ConversionCreate(ConversionBase):
    model_config = {
        "extra": "forbid",
        "json_schema_extra": {
            "example": {
                "product_id": 12,
                "warehouse_id": 3,
                "unit_start_id": 1,
                "unit_end_id": 2,
                "user_id": 7,
                "quantity_start": 2.0,
                "quantity_end": 20.0,
                "description": "Conversión de 2 cajas en 20 piezas"
            }
        }
    }


# -----------------------
# Update schema
# -----------------------
class ConversionUpdate(BaseModel):
    product_id: Optional[int] = None
    warehouse_id: Optional[int] = None
    unit_start_id: Optional[int] = None
    unit_end_id: Optional[int] = None
    user_id: Optional[int] = None
    quantity_start: Optional[float] = Field(None, gt=0)
    quantity_end: Optional[float] = Field(None, gt=0)
    description: Optional[str] = None
    deleted_at: Optional[datetime] = None

    model_config = {
        "extra": "forbid",
        "json_schema_extra": {
            "example": {
                "quantity_start": 5.0,
                "quantity_end": 50.0,
                "description": "Corrección en la conversión"
            }
        }
    }


# -----------------------
# Response schema
# -----------------------
class ConversionResponse(ConversionBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 101,
                "product_id": 12,
                "warehouse_id": 3,
                "unit_start_id": 1,
                "unit_end_id": 2,
                "user_id": 7,
                "quantity_start": 2.0,
                "quantity_end": 20.0,
                "description": "Conversión de 2 cajas en 20 piezas",
                "created_at": "2024-09-01T10:30:00",
                "updated_at": "2024-09-01T12:00:00",
                "deleted_at": None
            }
        }
    }


# -----------------------
# With relations (expandable)
# -----------------------
class ConversionWithRelations(ConversionResponse):
    # To expand later with nested schemas
    # product: Optional["ProductResponse"]
    # warehouse: Optional["WarehouseResponse"]
    # unit_start: Optional["UnitResponse"]
    # unit_end: Optional["UnitResponse"]
    # user: Optional["UserResponse"]
    pass


# -----------------------
# Search params
# -----------------------
class ConversionSearchParams(BaseModel):
    product_id: Optional[int] = None
    warehouse_id: Optional[int] = None
    unit_start_id: Optional[int] = None
    unit_end_id: Optional[int] = None
    user_id: Optional[int] = None
    created_from: Optional[datetime] = None
    created_to: Optional[datetime] = None
