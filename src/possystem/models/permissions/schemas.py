from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict, field_validator
import re


class PermissionBase(BaseModel):
    name: str = Field(..., max_length=255, min_length=1, description="Permission name")

    model_config = dict(from_attributes=True)  # compatible con objetos ORM

    @field_validator("name")
    @classmethod
    def strip_lower_and_validate(cls, v: str) -> str:
        # 1. Limpiar espacios y pasar a minúsculas
        v = v.strip().lower()

        # 2. Validar patrón
        if not re.fullmatch(r"^[a-z.]+$", v):
            raise ValueError("Invalid permission name pattern, only lowercase letters and '.' are allowed")

        return v



# Request schemas
class PermissionCreate(PermissionBase):
    """Schema for creating a new permission"""

    model_config = ConfigDict(
        extra= "forbid",
        json_schema_extra= {
            "example": {
                "name": "edit_users"
            }
        }
    )


class PermissionUpdate(PermissionBase):
    """Schema for updating an existing permission"""
    name: Optional[str] = Field(None, max_length=255, min_length=1, description="Permission name")

    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "name": "edit_users_updated"
            }
        }
    )


# Response schemas
class PermissionResponse(PermissionBase):
    """Basic permission response without relationships"""
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes= True,
        json_schema_extra= {
            "example": {
                "id": 1,
                "name": "edit_users",
                "created_at": "2024-06-01T12:34:56",
                "updated_at": "2024-06-02T10:00:00"
            }
        }
    )


class PermissionWithRoles(PermissionResponse):
    """Permission response with associated roles"""
    roles: List["RoleResponse"] = []

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "edit_users",
                "created_at": "2024-06-01T12:34:56",
                "updated_at": "2024-06-02T10:00:00",
                "roles": [
                    {
                        "id": 1,
                        "name": "admin",
                        "created_at": "2024-06-01T12:34:56",
                        "updated_at": "2024-06-02T10:00:00"
                    }
                ]
            }
        }
    )


# Forward reference resolution will be handled after importing RoleResponse
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..roles.schemas import RoleResponse