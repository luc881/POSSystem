from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class ProductIngredientBase(BaseModel):
    ingredient_id: int = Field(..., description="Ingredient ID")
    amount: Optional[str] = Field(None, max_length=50, description="Amount of ingredient (e.g., '500 mg')")


class ProductIngredientCreate(ProductIngredientBase):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "ingredient_id": 1,
                "amount": "500 mg"
            }
        }
    )


class ProductIngredientUpdate(BaseModel):
    amount: Optional[str] = Field(None, max_length=50)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "amount": "650 mg"
            }
        }
    )


class ProductIngredientResponse(ProductIngredientBase):
    product_id: int

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "product_id": 20,
                "ingredient_id": 1,
                "amount": "500 mg"
            }
        }
    )
