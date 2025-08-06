from typing import Optional, List
from pydantic import BaseModel, Field

class PermissionRequest(BaseModel):
    name: str = Field(..., max_length=255, example="edit_users")

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "edit_users"
            }
        }
    }

class PermissionResponse(BaseModel):
    id: int
    name: str
    created_at: Optional[str]  # or datetime if you want
    updated_at: Optional[str]
    roles: Optional[List[str]] = None  # or List[int] or List[RoleResponse], depending on your needs

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "edit_users",
                "created_at": "2024-06-01T12:34:56",
                "updated_at": "2024-06-02T10:00:00",
                "roles": ["admin", "editor"]
            }
        }
    }
