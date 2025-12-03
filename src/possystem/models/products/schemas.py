from typing import Optional, List, TYPE_CHECKING
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
    IsDiscountFlag,
    IsActiveFlag,
    IsTaxableFlag,
    AllowWarrantyFlag,
    AllowWithoutStockFlag,
    ProductUnitName,
    ProductBaseUnitName,
)

# =========================================================
# 🔹 Mini response (para Brand/Master)
# =========================================================
class ProductSimpleResponse(BaseModel):
    id: int
    title: ProductTitleStr
    sku: Optional[ProductSKUStr] = None
    price_retail: PriceRetail
    is_active: IsActiveFlag

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 10,
                "title": "Paracetamol 500mg",
                "sku": "PARA500",
                "price_retail": 25.0,
                "is_active": True
            }
        }
    )



# =========================================================
# 🔹 Base schema
# =========================================================
class ProductBase(BaseModel):
    title: ProductTitleStr
    image: Optional[ProductImageURL] = None

    price_retail: PriceRetail
    price_cost: PriceCost

    description: Optional[ProductDescriptionStr] = None
    sku: Optional[ProductSKUStr] = None

    is_discount: IsDiscountFlag = False
    max_discount: Optional[DiscountPercentage] = None
    is_taxable: IsTaxableFlag = True
    tax_percentage: Optional[TaxPercentage] = None

    allow_warranty: AllowWarrantyFlag = False
    warranty_days: Optional[WarrantyDays] = None

    unit_name: ProductUnitName = Field(default="pieza")
    base_unit_name: Optional[ProductBaseUnitName] = None
    units_per_base: Optional[float] = None

    allow_without_stock: AllowWithoutStockFlag = True
    is_active: IsActiveFlag = True


# =========================================================
# 🟢 Create
# =========================================================
class ProductCreate(ProductBase):
    brand_id: Optional[int] = Field(None)
    product_master_id: Optional[int] = Field(None)
    ingredient_ids: Optional[List[int]] = None

    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "title": "Ibuprofeno 400mg",
                "image": "https://example.com/img.png",
                "price_retail": 45.5,
                "price_cost": 30.0,
                "description": "Caja con 10 tabletas",
                "sku": "IBU400",
                "is_discount": False,
                "max_discount": 0,
                "is_taxable": True,
                "tax_percentage": 16,
                "allow_warranty": False,
                "warranty_days": None,
                "unit_name": "pieza",
                "base_unit_name": None,
                "units_per_base": None,
                "allow_without_stock": True,
                "is_active": True,
                "brand_id": 1,
                "product_master_id": None,
                "ingredient_ids": [1, 2]
            }
        }
    )



# =========================================================
# 🟡 Update
# =========================================================
class ProductUpdate(BaseModel):
    title: Optional[ProductTitleStr] = None
    image: Optional[ProductImageURL] = None

    price_retail: Optional[PriceRetail] = None
    price_cost: Optional[PriceCost] = None

    description: Optional[ProductDescriptionStr] = None
    sku: Optional[ProductSKUStr] = None

    is_discount: Optional[IsDiscountFlag] = None
    max_discount: Optional[DiscountPercentage] = None
    is_taxable: Optional[IsTaxableFlag] = None
    tax_percentage: Optional[TaxPercentage] = None

    allow_warranty: Optional[AllowWarrantyFlag] = None
    warranty_days: Optional[WarrantyDays] = None

    unit_name: Optional[ProductUnitName] = None
    base_unit_name: Optional[ProductBaseUnitName] = None
    units_per_base: Optional[float] = None

    allow_without_stock: Optional[AllowWithoutStockFlag] = None
    is_active: Optional[IsActiveFlag] = None

    brand_id: Optional[int] = None
    product_master_id: Optional[int] = None
    ingredient_ids: Optional[List[int]] = None

    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "title": "Ibuprofeno 400mg - Nueva presentación",
                "image": "https://example.com/new.png",
                "price_retail": 48.0,
                "price_cost": 31.0,
                "description": "Nueva caja de 12 tabletas",
                "sku": "IBU400",
                "is_discount": True,
                "max_discount": 10,
                "is_taxable": True,
                "tax_percentage": 16,
                "allow_warranty": False,
                "warranty_days": None,
                "unit_name": "pieza",
                "base_unit_name": None,
                "units_per_base": None,
                "allow_without_stock": True,
                "is_active": True,
                "ingredient_ids": [1, 3]
            }
        }
    )



# =========================================================
# 🔵 Response (sin relaciones)
# =========================================================
class ProductResponse(ProductBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    brand_id: Optional[int] = None
    product_master_id: Optional[int] = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 12,
                "title": "Ibuprofeno 400mg",
                "image": "https://example.com/img.png",
                "price_retail": 45.5,
                "price_cost": 30.0,
                "description": "Caja con 10 tabletas",
                "sku": "IBU400",
                "is_discount": False,
                "max_discount": 0,
                "is_taxable": True,
                "tax_percentage": 16,
                "allow_warranty": False,
                "warranty_days": None,
                "unit_name": "pieza",
                "base_unit_name": None,
                "units_per_base": None,
                "allow_without_stock": True,
                "is_active": True,
                "brand_id": 1,
                "product_master_id": None,
                "created_at": "2024-02-12T10:00:00Z",
                "updated_at": "2024-02-15T13:22:00Z"
            }
        }
    )



# =========================================================
# 🧩 Detallado (con relaciones)
# =========================================================
class ProductDetailsResponse(ProductResponse):
    brand: Optional["ProductBrandResponse"] = None
    product_master: Optional["ProductMasterResponse"] = None
    batches: Optional[List["ProductBatchResponse"]] = None
    ingredients: Optional[List["IngredientResponse"]] = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 12,
                "title": "Ibuprofeno 400mg",
                "image": "https://example.com/img.png",
                "price_retail": 45.5,
                "price_cost": 30.0,
                "description": "Caja con 10 tabletas",
                "sku": "IBU400",
                "is_discount": False,
                "max_discount": 0,
                "is_taxable": True,
                "tax_percentage": 16,
                "allow_warranty": False,
                "warranty_days": None,
                "unit_name": "pieza",
                "base_unit_name": None,
                "units_per_base": None,
                "allow_without_stock": True,
                "is_active": True,
                "brand_id": 1,
                "product_master_id": 5,
                "created_at": "2024-02-12T10:00:00Z",
                "updated_at": "2024-02-15T13:22:00Z",

                "brand": {
                    "id": 1,
                    "name": "Genfar"
                },

                "product_master": {
                    "id": 5,
                    "name": "Analgésicos",
                    "description": "Medicamentos para dolor"
                },

                "batches": [
                    {
                        "id": 101,
                        "batch_number": "L202401A",
                        "expiration_date": "2026-01-01",
                        "quantity": 35
                    }
                ],

                "ingredients": [
                    {"id": 1, "name": "Ibuprofeno"},
                    {"id": 2, "name": "Estearato de magnesio"}
                ]
            }
        }
    )



# =========================================================
# 🔍 Search params
# =========================================================
class ProductSearchParams(BaseModel):
    title: Optional[str] = Field(None, min_length=2, max_length=100)
    is_active: Optional[bool] = None
    brand_id: Optional[int] = None
    product_master_id: Optional[int] = None

    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "title": "ibu",
                "is_active": True,
                "brand_id": 1,
                "product_master_id": 5
            }
        }
    )



# =========================================================
# 🔁 Forward references
# =========================================================
if TYPE_CHECKING:
    from ..product_batch.schemas import ProductBatchResponse
    from ..product_brands.schemas import ProductBrandResponse
    from ..product_master.schemas import ProductMasterResponse
    from ..ingredients.schemas import IngredientResponse
