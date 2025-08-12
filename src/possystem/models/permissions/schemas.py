from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


# Base schemas (shared fields)
class PermissionBase(BaseModel):
    name: str = Field(..., max_length=255, min_length=1, description="Permission name")


# Request schemas
class PermissionCreate(PermissionBase):
    """Schema for creating a new permission"""

    model_config = {
        "extra": "forbid",
        "json_schema_extra": {
            "example": {
                "name": "edit_users"
            }
        }
    }


class PermissionUpdate(BaseModel):
    """Schema for updating an existing permission"""
    name: Optional[str] = Field(None, max_length=255, min_length=1, description="Permission name")

    model_config = {
        "extra": "forbid",
        "json_schema_extra": {
            "example": {
                "name": "edit_users_updated"
            }
        }
    }


# Response schemas
class PermissionResponse(PermissionBase):
    """Basic permission response without relationships"""
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "edit_users",
                "created_at": "2024-06-01T12:34:56",
                "updated_at": "2024-06-02T10:00:00"
            }
        }
    }


class PermissionWithRoles(PermissionResponse):
    """Permission response with associated roles"""
    roles: List["RoleResponse"] = []

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
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
    }


# Forward reference resolution will be handled after importing RoleResponse
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..roles.schemas import RoleResponse