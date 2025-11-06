from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from possystem.types.products import (
    ProductTitleStr,
    ProductImageURL,
    ProductDescriptionStr,
    ProductSKUStr,
    PriceRetail,
    PriceCost,
    DiscountPercentage,
    TaxPercentage,
    WarrantyDays,
    StockStateEnum,
    ProductFlags
)


# Base schema (shared fields)
class ProductBase(BaseModel):
    title: ProductTitleStr = Field(...)
    image: Optional[ProductImageURL] = None
    product_category_id: Optional[int] = None
    price_retail: PriceRetail = Field(...)
    price_cost: PriceCost = Field(...)
    description: Optional[ProductDescriptionStr] = None
    is_discount: bool = ProductFlags.IS_DISCOUNT
    max_discount: Optional[DiscountPercentage] = None
    is_gift: bool = ProductFlags.IS_GIFT
    allow_without_stock: bool = ProductFlags.ALLOW_WITHOUT_STOCK
    is_active: bool = ProductFlags.IS_ACTIVE
    stock_state: StockStateEnum = Field(default=StockStateEnum.AVAILABLE)
    warranty_applicable: bool = ProductFlags.ALLOW_WARRANTY
    warranty_days: Optional[WarrantyDays] = None
    is_taxable: bool = ProductFlags.IS_TAXABLE
    tax_percentage: Optional[TaxPercentage] = None
    sku: Optional[ProductSKUStr] = None


# Schema for creation
class ProductCreate(ProductBase):
    model_config = ConfigDict(
        extra= "forbid",
        json_schema_extra= {
            "example": {
                "title": "Refresco Cola 600ml",
                "image": "https://example.com/images/cola600.png",
                "product_category_id": 1,
                "price_retail": 20.0,
                "price_cost": 18.0,
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
    )


# Schema for update (all optional)
class ProductUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=250)
    image: Optional[str] = Field(None, max_length=250)
    product_category_id: Optional[int] = Field(None, gt=0)
    price_retail: Optional[float] = Field(None, ge=0)
    price_cost: Optional[float] = Field(None, ge=0)
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

    model_config = ConfigDict(
        extra= "forbid",
        json_schema_extra= {
            "example": {
                "price_retail": 19.0,
                "is_discount": False,
                "stock_state": 2,
                "is_active": True
            }
        }
    )


# Schema for response
class ProductResponse(ProductBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes= True,  # ORM mode
        json_schema_extra= {
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
    )


# Schema for detailed response (with relationships)
class ProductDetailsResponse(ProductResponse):
    category: Optional["ProductCategoryResponse"] = None
    product_warehouses: Optional[list["ProductWarehouseResponse"]] = []
    product_wallets: Optional[list["ProductWalletResponse"]] = []

    model_config = ConfigDict(
        from_attributes= True,
        json_schema_extra= {
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
    )


# Schema for search filters
class ProductSearchParams(BaseModel):
    title: Optional[str] = Field(None, description="Buscar por título (coincidencia parcial)")
    product_category_id: Optional[int] = Field(None, gt=0, description="Filtrar por categoría")
    is_active: Optional[bool] = Field(None, description="Filtrar por estado de disponibilidad")
    stock_state: Optional[int] = Field(None, ge=1, le=3, description="Filtrar por estado de stock")

    model_config = ConfigDict(
        extra= "forbid"
    )


# Forward reference resolution
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..product_categories.schemas import ProductCategoryResponse
    from ..product_warehouses.schemas import ProductWarehouseResponse
    from ..product_wallets.schemas import ProductWalletResponse
