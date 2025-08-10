from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


# Base schemas (shared fields)
class RoleBase(BaseModel):
    name: str = Field(..., max_length=255, min_length=1, description="Role name")


# Request schemas
class RoleCreate(RoleBase):
    """Schema for creating a new role"""
    # permission_ids: Optional[List[int]] = Field(default=[], description="List of permission IDs to assign to this role")

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "admin",
                # "permission_ids": [1, 2, 3]
            }
        }
    }


class RoleUpdate(BaseModel):
    """Schema for updating an existing role"""
    name: Optional[str] = Field(None, max_length=255, min_length=1, description="Role name")
    # permission_ids: Optional[List[int]] = Field(None, description="List of permission IDs to assign to this role")

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "admin_updated",
                # "permission_ids": [1, 2, 4]
            }
        }
    }


# Response schemas
class RoleResponse(RoleBase):
    """Basic role response without relationships"""
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "admin",
                "created_at": "2024-06-01T12:34:56",
                "updated_at": "2024-06-02T10:00:00"
            }
        }
    }


class RoleWithPermissions(RoleResponse):
    """Role response with associated permissions"""
    permissions: List["PermissionResponse"] = []

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "admin",
                "created_at": "2024-06-01T12:34:56",
                "updated_at": "2024-06-02T10:00:00",
                "permissions": [
                    {
                        "id": 1,
                        "name": "edit_users",
                        "created_at": "2024-06-01T12:34:56",
                        "updated_at": "2024-06-02T10:00:00"
                    }
                ]
            }
        }
    }

class RolePermissionAssociation(BaseModel):
    permission_id: int


# Forward reference resolution
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..permissions.schemas import PermissionResponse