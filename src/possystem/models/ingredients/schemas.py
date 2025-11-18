from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict, field_validator
import re


# --- Base ---
class IngredientBase(BaseModel):
    name: str = Field(..., max_length=255, min_length=1, description="Ingredient name")
    description: Optional[str] = Field(None, description="Optional description of ingredient")

    @field_validator("name")
    @classmethod
    def normalize_name(cls, v: str) -> str:
        v = v.strip().lower()

        if not re.fullmatch(r"^[a-z0-9._\- ]+$", v):
            raise ValueError("Invalid ingredient name, only letters, numbers and ._- are allowed")

        return v


# --- Create ---
class IngredientCreate(IngredientBase):
    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "name": "paracetamol",
                "description": "Analgesic and antipyretic"
            }
        },
    )


# --- Update ---
class IngredientUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255, min_length=1)
    description: Optional[str] = None

    @field_validator("name")
    @classmethod
    def normalize_optional_name(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        v = v.strip().lower()
        if not re.fullmatch(r"^[a-z0-9._\- ]+$", v):
            raise ValueError("Invalid ingredient name")
        return v

    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "name": "ibuprofen updated",
                "description": "Updated description"
            }
        },
    )


# --- Response ---
class IngredientResponse(IngredientBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 10,
                "name": "paracetamol",
                "description": "Analgesic and antipyretic",
                "created_at": "2024-01-01T10:00:00",
                "updated_at": "2024-01-01T10:00:00",
            }
        },
    )
