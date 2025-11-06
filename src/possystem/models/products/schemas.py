from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from enum import IntEnum
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
    IsDiscountFlag,
    IsGiftFlag,
    AllowWithoutStockFlag,
    IsActiveFlag,
    IsTaxableFlag,
    AllowWarrantyFlag
)


# Base schema (shared fields)
class ProductBase(BaseModel):
    title: ProductTitleStr = Field(...)
    image: Optional[ProductImageURL] = None
    product_category_id: Optional[int] = None
    price_retail: PriceRetail = Field(...)
    price_cost: PriceCost = Field(...)
    description: Optional[ProductDescriptionStr] = None
    max_discount: Optional[DiscountPercentage] = None
    stock_state: StockStateEnum = Field(default=StockStateEnum.AVAILABLE)
    warranty_days: Optional[WarrantyDays] = None
    tax_percentage: Optional[TaxPercentage] = None
    sku: Optional[ProductSKUStr] = None

    allow_without_stock: AllowWithoutStockFlag = False
    allow_warranty: AllowWarrantyFlag = False
    is_discount: IsDiscountFlag = False
    is_gift: IsGiftFlag = False
    is_active: IsActiveFlag = True
    is_taxable: IsTaxableFlag = False

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
                "allow_warranty": True,
                "is_taxable": True,
                "tax_percentage": 16.0,
                "sku": "COLA600ML"
            }
        }
    )


# Schema for update (all optional)
class ProductUpdate(BaseModel):
    title: Optional[ProductTitleStr] = None
    price_retail: Optional[PriceRetail] = None
    price_cost: Optional[PriceCost] = None
    max_discount: Optional[DiscountPercentage] = None
    stock_state: Optional[StockStateEnum] = None

    allow_without_stock: Optional[AllowWithoutStockFlag] = None
    allow_warranty: Optional[AllowWarrantyFlag] = None
    is_discount: Optional[IsDiscountFlag] = None
    is_active: Optional[IsActiveFlag] = None
    is_taxable: Optional[IsTaxableFlag] = None
    is_gift: Optional[IsGiftFlag] = None



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

    model_config = ConfigDict(
        from_attributes=True,  # Permite usar ORM objects directamente
        json_schema_extra={
            "example": {
                "id": 1,
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
                "sku": "COLA600ML",
                "created_at": "2024-07-01T12:00:00",
                "updated_at": "2024-07-02T09:30:00",
            }
        }
    )


# Schema for detailed response (with relationships)
class ProductDetailsResponse(ProductResponse):
    category: Optional[ProductCategoryResponse] = None
    batches: Optional[List["ProductBatchResponse"]] = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "title": "Refresco Cola 600ml",
                "price_retail": 20.0,
                "price_cost": 18.0,
                "stock_state": 1,
                "category": {
                    "id": 1,
                    "name": "Bebidas",
                    "is_active": True
                },
                "batches": [
                    {
                        "id": 100,
                        "lot_code": "L2301",
                        "expiration_date": "2025-07-01",
                        "stock": 50,
                        "created_at": "2024-07-01T12:00:00",
                    }
                ]
            }
        }
    )

# Schema for search filters
class StockStateEnum(IntEnum):
    AVAILABLE = 1
    LOW_STOCK = 2
    OUT_OF_STOCK = 3

class ProductSearchParams(BaseModel):
    title: Optional[str] = Field(None, min_length=2, max_length=100, description="Buscar por título (coincidencia parcial)")
    product_category_id: Optional[int] = Field(None, gt=0, description="Filtrar por categoría")
    is_active: Optional[bool] = Field(None, description="Filtrar por estado de disponibilidad")
    stock_state: Optional[StockStateEnum] = Field(None, description="Filtrar por estado de stock")

    model_config = ConfigDict(extra="forbid")


# Forward reference resolution
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..product_categories.schemas import ProductCategoryResponse
    from ..product_warehouses.schemas import ProductWarehouseResponse
    from ..product_wallets.schemas import ProductWalletResponse
