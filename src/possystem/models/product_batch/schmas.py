from typing import Optional
from datetime import date, datetime
from pydantic import BaseModel, Field


# Base schema (campos compartidos)
class ProductBatchBase(BaseModel):
    lot_code: Optional[str] = Field(None, max_length=100, description="Código o identificador del lote")
    expiration_date: date = Field(..., description="Fecha de caducidad del lote")
    quantity: int = Field(..., ge=0, description="Cantidad disponible en el lote")
    purchase_price: Optional[float] = Field(None, ge=0, description="Precio de compra por unidad del lote")


# Schema para creación
class ProductBatchCreate(ProductBatchBase):
    product_id: int = Field(..., gt=0, description="ID del producto asociado")

    model_config = {
        "extra": "forbid",
        "json_schema_extra": {
            "example": {
                "product_id": 1,
                "lot_code": "A2025-01",
                "expiration_date": "2025-12-15",
                "quantity": 100,
                "purchase_price": 12.50
            }
        }
    }


# Schema para actualización
class ProductBatchUpdate(BaseModel):
    lot_code: Optional[str] = Field(None, max_length=100)
    expiration_date: Optional[date] = None
    quantity: Optional[int] = Field(None, ge=0)
    purchase_price: Optional[float] = Field(None, ge=0)

    model_config = {
        "extra": "forbid",
        "json_schema_extra": {
            "example": {
                "quantity": 80,
                "expiration_date": "2025-11-30"
            }
        }
    }


# Schema de respuesta (para API)
class ProductBatchResponse(ProductBatchBase):
    id: int
    product_id: int
    created_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 10,
                "product_id": 1,
                "lot_code": "A2025-01",
                "expiration_date": "2025-12-15",
                "quantity": 100,
                "purchase_price": 12.50,
                "created_at": "2025-06-01T14:25:00"
            }
        }
    }


# Schema de respuesta detallada (con relación al producto)
class ProductBatchDetailsResponse(ProductBatchResponse):
    product: Optional["ProductResponse"] = None

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 10,
                "lot_code": "A2025-01",
                "expiration_date": "2025-12-15",
                "quantity": 100,
                "purchase_price": 12.50,
                "product": {
                    "id": 1,
                    "title": "Paracetamol 500mg",
                    "price_general": 20.0,
                    "price_company": 18.0,
                    "sku": "PARA500",
                    "is_active": True
                }
            }
        }
    }


# Forward reference resolution (import diferido para evitar dependencias circulares)
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..products.schemas import ProductResponse
