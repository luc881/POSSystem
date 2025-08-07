from typing import List
from pydantic import BaseModel, Field


class RolePermissionAssignment(BaseModel):
    """Schema for assigning/removing permissions to/from roles"""
    role_id: int = Field(..., description="Role ID")
    permission_ids: List[int] = Field(..., description="List of permission IDs")

    model_config = {
        "json_schema_extra": {
            "example": {
                "role_id": 1,
                "permission_ids": [1, 2, 3]
            }
        }
    }


class RolePermissionResponse(BaseModel):
    """Response schema for role-permission assignments"""
    role_id: int
    permission_id: int

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "role_id": 1,
                "permission_id": 1
            }
        }
    }


class BulkRolePermissionResponse(BaseModel):
    """Response schema for bulk role-permission operations"""
    role_id: int
    assigned_permissions: List[int] = []
    removed_permissions: List[int] = []

    model_config = {
        "json_schema_extra": {
            "example": {
                "role_id": 1,
                "assigned_permissions": [1, 2, 3],
                "removed_permissions": [4, 5]
            }
        }
    }