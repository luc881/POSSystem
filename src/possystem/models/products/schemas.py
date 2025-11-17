from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from ..product_categories.schemas import ProductCategoryResponse
from ..product_batch.schemas import ProductBatchResponse
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
    UnitsPerBase,
)


# =========================================================
# 🔹 Base schema (campos compartidos)
# =========================================================
class ProductBase(BaseModel):
    title: ProductTitleStr = Field(...)
    image: Optional[ProductImageURL] = None

    price_retail: PriceRetail = Field(...)
    price_cost: PriceCost = Field(...)

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
    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "title": "Paracetamol 500mg caja 10 tabletas",
                "image": "https://example.com/images/paracetamol.png",
                "price_retail": 35.0,
                "price_cost": 20.0,
                "description": "Caja con 10 tabletas de paracetamol 500mg.",
                "sku": "PARA500-10TAB",
                "is_discount": False,
                "is_taxable": True,
                "tax_percentage": 16.0,
                "allow_without_stock": True,
                "unit_name": "caja",
                "base_unit_name": "tableta",
                "units_per_base": 10,
                "allow_warranty": False,
                "is_active": True
            }
        }
    )


# =========================================================
# 🟡 Update schema (todos los campos opcionales)
# =========================================================
class ProductUpdate(ProductBase):
    title: Optional[ProductTitleStr] = None
    price_retail: Optional[PriceRetail] = None
    price_cost: Optional[PriceCost] = None

    is_discount: Optional[IsDiscountFlag] = None
    is_taxable: Optional[IsTaxableFlag] = None

    allow_warranty: Optional[AllowWarrantyFlag] = None

    unit_name: Optional[str] = Field(None, max_length=50)

    allow_without_stock: Optional[AllowWithoutStockFlag] = None
    is_active: Optional[IsActiveFlag] = None

    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "price_retail": 33.0,
                "is_discount": True,
                "max_discount": 10.0,
                "is_active": True
            }
        }
    )


# =========================================================
# 🔵 Response schema (sin relaciones)
# =========================================================
class ProductResponse(ProductBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "title": "Paracetamol 500mg caja 10 tabletas",
                "price_retail": 35.0,
                "price_cost": 20.0,
                "is_discount": False,
                "is_active": True,
                "unit_name": "caja",
                "base_unit_name": "tableta",
                "units_per_base": 10,
                "sku": "PARA500-10TAB",
                "created_at": "2025-11-11T10:00:00",
                "updated_at": "2025-11-11T10:00:00"
            }
        }
    )


# =========================================================
# 🧩 Detailed response (con relaciones)
# =========================================================
class ProductDetailsResponse(ProductResponse):
    batches: Optional[List["ProductBatchResponse"]] = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "title": "Paracetamol 500mg caja 10 tabletas",
                "price_retail": 35.0,
                "price_cost": 20.0,
                "batches": [
                    {
                        "id": 10,
                        "lot_code": "L2301",
                        "expiration_date": "2026-02-01",
                        "stock": 120
                    }
                ]
            }
        }
    )


# =========================================================
# 🔍 Search params
# =========================================================
class ProductSearchParams(BaseModel):
    title: Optional[str] = Field(None, min_length=2, max_length=100, description="Buscar por título (coincidencia parcial)")
    is_active: Optional[bool] = Field(None, description="Filtrar por estado de disponibilidad")

    model_config = ConfigDict(extra="forbid")


# =========================================================
# 🔁 Forward references
# =========================================================
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..product_batch.schemas import ProductBatchResponse
