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

    model_config = ConfigDict(from_attributes=True)


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

    model_config = ConfigDict(extra="forbid")


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

    model_config = ConfigDict(extra="forbid")


# =========================================================
# 🔵 Response (sin relaciones)
# =========================================================
class ProductResponse(ProductBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    brand_id: Optional[int] = None
    product_master_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


# =========================================================
# 🧩 Detallado (con relaciones)
# =========================================================
class ProductDetailsResponse(ProductResponse):
    brand: Optional["ProductBrandResponse"] = None
    product_master: Optional["ProductMasterResponse"] = None
    batches: Optional[List["ProductBatchResponse"]] = None
    ingredients: Optional[List["IngredientResponse"]] = None

    model_config = ConfigDict(from_attributes=True)


# =========================================================
# 🔍 Search params
# =========================================================
class ProductSearchParams(BaseModel):
    title: Optional[str] = Field(None, min_length=2, max_length=100)
    is_active: Optional[bool] = None
    brand_id: Optional[int] = None
    product_master_id: Optional[int] = None

    model_config = ConfigDict(extra="forbid")


# =========================================================
# 🔁 Forward references
# =========================================================
if TYPE_CHECKING:
    from ..product_batch.schemas import ProductBatchResponse
    from ..product_brands.schemas import ProductBrandResponse
    from ..product_master.schemas import ProductMasterResponse
    from ..ingredients.schemas import IngredientResponse
