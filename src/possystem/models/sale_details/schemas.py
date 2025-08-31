from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


# -----------------------
# Base schema (shared fields)
# -----------------------
class SaleDetailBase(BaseModel):
    sale_id: int = Field(..., gt=0, description="ID de la venta asociada")
    product_id: int = Field(..., gt=0, description="ID del producto asociado")
    product_category_id: Optional[int] = Field(None, gt=0, description="ID de la categoría del producto")

    quantity: float = Field(..., gt=0, description="Cantidad vendida")
    price_unit: float = Field(..., ge=0, description="Precio unitario del producto")
    discount: Optional[float] = Field(0.0, ge=0, description="Descuento aplicado")
    subtotal: Optional[float] = Field(None, ge=0, description="Subtotal (precio unitario - descuento)")
    total: Optional[float] = Field(None, ge=0, description="Total (subtotal * cantidad)")
    unit_id: Optional[int] = Field(None, gt=0, description="ID de la unidad de medida")
    warehouse_id: Optional[int] = Field(None, gt=0, description="ID del almacén")

    tax: Optional[float] = Field(None, ge=0, description="Impuesto aplicado (IGV)")
    description: Optional[str] = Field(None, description="Descripción del detalle de venta")
    state_attention: Optional[int] = Field(
        None, ge=1, le=3,
        description="Estado de atención (1 = pendiente, 2 = parcial, 3 = completo)"
    )
    quantity_pending: Optional[float] = Field(None, ge=0, description="Cantidad pendiente de atención")


# -----------------------
# Create schema
# -----------------------
class SaleDetailCreate(SaleDetailBase):
    model_config = {
        "extra": "forbid",
        "json_schema_extra": {
            "example": {
                "sale_id": 10,
                "product_id": 5,
                "product_category_id": 2,
                "quantity": 3,
                "price_unit": 50.0,
                "discount": 5.0,
                "subtotal": 45.0,
                "total": 135.0,
                "unit_id": 1,
                "warehouse_id": 4,
                "tax": 18.0,
                "description": "Detalle de venta de producto A",
                "state_attention": 1,
                "quantity_pending": 3
            }
        }
    }


# -----------------------
# Update schema (all optional)
# -----------------------
class SaleDetailUpdate(BaseModel):
    product_id: Optional[int] = Field(None, gt=0)
    product_category_id: Optional[int] = Field(None, gt=0)

    quantity: Optional[float] = Field(None, gt=0)
    price_unit: Optional[float] = Field(None, ge=0)
    discount: Optional[float] = Field(None, ge=0)
    subtotal: Optional[float] = Field(None, ge=0)
    total: Optional[float] = Field(None, ge=0)
    unit_id: Optional[int] = Field(None, gt=0)
    warehouse_id: Optional[int] = Field(None, gt=0)

    tax: Optional[float] = Field(None, ge=0)
    description: Optional[str] = None
    state_attention: Optional[int] = Field(None, ge=1, le=3)
    quantity_pending: Optional[float] = Field(None, ge=0)

    deleted_at: Optional[datetime] = None

    model_config = {
        "extra": "forbid",
        "json_schema_extra": {
            "example": {
                "quantity": 2,
                "state_attention": 2,
                "quantity_pending": 1
            }
        }
    }


# -----------------------
# Response schema
# -----------------------
class SaleDetailResponse(SaleDetailBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 100,
                "sale_id": 10,
                "product_id": 5,
                "product_category_id": 2,
                "quantity": 3,
                "price_unit": 50.0,
                "discount": 5.0,
                "subtotal": 45.0,
                "total": 135.0,
                "unit_id": 1,
                "warehouse_id": 4,
                "tax": 18.0,
                "description": "Detalle de venta de producto A",
                "state_attention": 1,
                "quantity_pending": 3,
                "created_at": "2024-07-01T10:00:00",
                "updated_at": "2024-07-05T10:30:00",
                "deleted_at": None
            }
        }
    }


# -----------------------
# Response with relations
# -----------------------
class SaleDetailWithRelations(SaleDetailResponse):
    product: Optional["ProductResponse"] = None
    product_category: Optional["ProductCategoryResponse"] = None
    warehouse: Optional["WarehouseResponse"] = None

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 100,
                "sale_id": 10,
                "quantity": 3,
                "total": 135.0,
                "state_attention": 1,
                "quantity_pending": 3,
                "created_at": "2024-07-01T10:00:00",
                "updated_at": "2024-07-05T10:30:00",
                "deleted_at": None,
                "product": {
                    "id": 5,
                    "name": "Producto A",
                    "price": 50.0,
                    "is_active": True
                },
                "product_category": {
                    "id": 2,
                    "name": "Categoría X"
                },
                "warehouse": {
                    "id": 4,
                    "name": "Almacén Central",
                    "location": "CDMX"
                }
            }
        }
    }


# -----------------------
# Search params
# -----------------------
class SaleDetailSearchParams(BaseModel):
    sale_id: Optional[int] = Field(None, gt=0, description="Filter by sale ID")
    product_id: Optional[int] = Field(None, gt=0, description="Filter by product ID")
    warehouse_id: Optional[int] = Field(None, gt=0, description="Filter by warehouse ID")
    state_attention: Optional[int] = Field(None, ge=1, le=3, description="Filter by attention state")


# -----------------------
# Forward references
# -----------------------
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..products.schemas import ProductResponse
    from ..products.schemas import ProductCategoryResponse
    from ..warehouses.schemas import WarehouseResponse
