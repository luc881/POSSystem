from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


# Base schema (shared fields)
class ProductBase(BaseModel):
    title: str = Field(..., max_length=250, description="Título o nombre del producto")
    image: Optional[str] = Field(None, max_length=250, description="Imagen del producto")
    product_category_id: int = Field(..., gt=0, description="ID de la categoría del producto")
    price_general: float = Field(..., ge=0, description="Precio general del producto")
    price_company: float = Field(..., ge=0, description="Precio para clientes empresa")
    description: Optional[str] = Field(None, description="Descripción del producto")
    is_discount: bool = Field(default=False, description="Indica si el producto tiene descuento")
    max_discount: Optional[float] = Field(None, ge=0, le=100, description="Porcentaje máximo de descuento permitido")
    is_gift: bool = Field(default=False, description="Indica si el producto puede usarse como obsequio")
    allow_without_stock: bool = Field(default=True, description="Permitir venta sin stock")
    is_active: bool = Field(default=True, description="Estado de disponibilidad del producto")
    stock_state: int = Field(default=1, ge=1, le=3, description="Estado del stock (1 disponible, 2 bajo stock, 3 agotado)")
    warranty_days: Optional[float] = Field(None, ge=0, description="Días de garantía del producto")
    is_taxable: bool = Field(default=True, description="Indica si aplica impuesto")
    tax_percentage: Optional[float] = Field(None, ge=0, le=100, description="Porcentaje de impuesto")
    sku: Optional[str] = Field(None, max_length=100, description="Código SKU del producto")


# Schema for creation
class ProductCreate(ProductBase):
    model_config = {
        "extra": "forbid",
        "json_schema_extra": {
            "example": {
                "title": "Refresco Cola 600ml",
                "image": "https://example.com/images/cola600.png",
                "product_category_id": 1,
                "price_general": 20.0,
                "price_company": 18.0,
                "description": "Refresco de cola en presentación de 600ml",
                "is_discount": True,
                "max_discount": 15.0,
                "is_gift": False,
                "allow_without_stock": True,
                "is_active": True,
                "stock_state": 1,
                "warranty_days": 30,
                "is_taxable": True,
                "tax_percentage": 16.0,
                "sku": "COLA600ML"
            }
        }
    }


# Schema for update (all optional)
class ProductUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=250)
    image: Optional[str] = Field(None, max_length=250)
    product_category_id: Optional[int] = Field(None, gt=0)
    price_general: Optional[float] = Field(None, ge=0)
    price_company: Optional[float] = Field(None, ge=0)
    description: Optional[str] = None
    is_discount: Optional[bool] = None
    max_discount: Optional[float] = Field(None, ge=0, le=100)
    is_gift: Optional[bool] = None
    allow_without_stock: Optional[bool] = None
    is_active: Optional[bool] = None
    stock_state: Optional[int] = Field(None, ge=1, le=3)
    warranty_days: Optional[float] = Field(None, ge=0)
    is_taxable: Optional[bool] = None
    tax_percentage: Optional[float] = Field(None, ge=0, le=100)
    sku: Optional[str] = Field(None, max_length=100)
    deleted_at: Optional[datetime] = None

    model_config = {
        "extra": "forbid",
        "json_schema_extra": {
            "example": {
                "price_general": 19.0,
                "is_discount": False,
                "stock_state": 2,
                "is_active": True
            }
        }
    }


# Schema for response
class ProductResponse(ProductBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True,  # ORM mode
        "json_schema_extra": {
            "example": {
                "id": 1,
                "title": "Refresco Cola 600ml",
                "image": "https://example.com/images/cola600.png",
                "product_category_id": 1,
                "price_general": 20.0,
                "price_company": 18.0,
                "description": "Refresco de cola en presentación de 600ml",
                "is_discount": True,
                "max_discount": 15.0,
                "is_gift": False,
                "allow_without_stock": True,
                "is_active": True,
                "stock_state": 1,
                "warranty_days": 30,
                "is_taxable": True,
                "tax_percentage": 16.0,
                "sku": "COLA600ML",
                "created_at": "2024-07-01T12:00:00",
                "updated_at": "2024-07-02T09:30:00",
                "deleted_at": None
            }
        }
    }


# Schema for detailed response (with relationships)
class ProductDetailsResponse(ProductResponse):
    category: Optional["ProductCategoryResponse"] = None
    product_warehouses: Optional[list["ProductWarehouseResponse"]] = []
    product_wallets: Optional[list["ProductWalletResponse"]] = []

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "title": "Refresco Cola 600ml",
                "price_general": 20.0,
                "stock_state": 1,
                "category": {
                    "id": 1,
                    "name": "Bebidas",
                    "is_active": True
                },
                "product_warehouses": [
                    {
                        "id": 10,
                        "warehouse_id": 2,
                        "stock": 120.0,
                        "state_stock": 1
                    }
                ],
                "product_wallets": [
                    {
                        "id": 5,
                        "branch_id": 3,
                        "price": 19.0,
                        "type_client": 1
                    }
                ]
            }
        }
    }


# Schema for search filters
class ProductSearchParams(BaseModel):
    title: Optional[str] = Field(None, description="Buscar por título (coincidencia parcial)")
    product_category_id: Optional[int] = Field(None, gt=0, description="Filtrar por categoría")
    is_active: Optional[bool] = Field(None, description="Filtrar por estado de disponibilidad")
    stock_state: Optional[int] = Field(None, ge=1, le=3, description="Filtrar por estado de stock")

    model_config = {
        "extra": "forbid"
    }


# Forward reference resolution
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..product_categories.schemas import ProductCategoryResponse
    from ..product_warehouses.schemas import ProductWarehouseResponse
    from ..product_wallets.schemas import ProductWalletResponse
