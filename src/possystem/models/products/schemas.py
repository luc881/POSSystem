from typing import Optional, List
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
# 🔹 Base schema (campos compartidos)
# =========================================================
class ProductBase(BaseModel):
    title: ProductTitleStr
    image: Optional[ProductImageURL] = None

    price_retail: PriceRetail
    price_cost: PriceCost

    description: Optional[ProductDescriptionStr] = None
    sku: Optional[ProductSKUStr] = None

    # --- Descuentos / impuestos ---
    is_discount: IsDiscountFlag = False
    max_discount: Optional[DiscountPercentage] = None
    is_taxable: IsTaxableFlag = True
    tax_percentage: Optional[TaxPercentage] = None

    # --- Garantía ---
    allow_warranty: AllowWarrantyFlag = False
    warranty_days: Optional[WarrantyDays] = None

    # --- Unidades / fraccionamiento ---
    unit_name: ProductUnitName = Field(default="pieza")
    base_unit_name: Optional[ProductBaseUnitName] = None
    units_per_base: Optional[float] = None

    # --- Estado ---
    allow_without_stock: AllowWithoutStockFlag = True
    is_active: IsActiveFlag = True


# =========================================================
# 🟢 Create schema
# =========================================================
class ProductCreate(ProductBase):
    brand_id: Optional[int] = Field(None, description="ID de la marca")
    product_master_id: Optional[int] = Field(None, description="ID del master product")
    ingredient_ids: Optional[List[int]] = Field(
        default=None, description="IDs de ingredientes"
    )

    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "title": "Paracetamol 500mg caja 10 tabletas",
                "image": "https://example.com/img.png",
                "price_retail": 35.0,
                "price_cost": 20.0,
                "description": "Caja con 10 tabletas",
                "sku": "PARA500-10TAB",
                "is_taxable": True,
                "tax_percentage": 16.0,
                "unit_name": "caja",
                "base_unit_name": "tableta",
                "units_per_base": 10,
                "brand_id": 2,
                "product_master_id": 1,
                "ingredient_ids": [4, 8]
            }
        }
    )


# =========================================================
# 🟡 Update schema (todos los campos opcionales)
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

    # --- Relaciones ---
    brand_id: Optional[int] = None
    product_master_id: Optional[int] = None
    ingredient_ids: Optional[List[int]] = None

    model_config = ConfigDict(extra="forbid")


# =========================================================
# 🔵 Response schema (sin relaciones completas)
# =========================================================
class ProductResponse(ProductBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    brand_id: Optional[int] = None
    product_master_id: Optional[int] = None

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# 🧩 Detailed response (con relaciones)
# =========================================================
class ProductDetailsResponse(ProductResponse):
    brand: Optional["ProductBrandResponse"] = None
    master: Optional["ProductMasterResponse"] = None
    batches: Optional[List["ProductBatchResponse"]] = None
    ingredients: Optional[List["IngredientResponse"]] = None

    model_config = ConfigDict(
        from_attributes=True
    )


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
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..product_batch.schemas import ProductBatchResponse
    from ..product_brands.schemas import ProductBrandResponse
    from ..product_master.schemas import ProductMasterResponse
    from ..ingredients.schemas import IngredientResponse
