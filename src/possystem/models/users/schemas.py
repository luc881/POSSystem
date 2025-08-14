from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

# Base schema (campos compartidos)
class UserBase(BaseModel):
    name: str = Field(..., max_length=255, description="Nombre del usuario")
    surname: Optional[str] = Field(None, max_length=255, description="Apellido del usuario")
    email: EmailStr = Field(..., max_length=255, description="Correo electrónico")
    avatar: Optional[str] = Field(None, max_length=255, description="URL del avatar")
    branch_id: Optional[int] = Field(None, gt=0, description="ID de la sucursal")
    phone: Optional[str] = Field(None, max_length=50, description="Número telefónico")
    type_document: Optional[str] = Field(None, max_length=50, description="Tipo de documento")
    n_document: Optional[str] = Field(None, max_length=50, description="Número de documento")
    state: Optional[bool] = Field(True, description="Estado del usuario (True = activo, False = inactivo)")
    gender: Optional[str] = Field(None, max_length=5, description="Género (M/F)")
    role_id: Optional[int] = Field(None, gt=0, description="ID del rol asignado")

# Esquema para creación (password obligatorio, email_verified_at y deleted_at no se envían al crear)
class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=255, description="Contraseña del usuario")

    model_config ={
        "extra": "forbid",
        "json_schema_extra": {
            "example": {
                "name": "Juan",
                "surname": "Pérez",
                "email": "juan.perez@example.com",
                "password": "securepassword123",
                "avatar": "http://example.com/avatar.jpg",
                "phone": "5551234567",
                "type_document": "INE",
                "n_document": "ABC123456",
                "state": True,
                "gender": "M",
                "branch_id": 1,
                "role_id": 2
            }
        }
    }

# Esquema para actualización (todos opcionales)
class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    surname: Optional[str] = Field(None, max_length=255)
    email: Optional[EmailStr] = Field(None, max_length=255)
    password: Optional[str] = Field(None, min_length=6, max_length=255)
    avatar: Optional[str] = Field(None, max_length=255)
    phone: Optional[str] = Field(None, max_length=50)
    branch_id: Optional[int] = Field(None, gt=0)
    role_id: Optional[int] = Field(None, gt=0)
    type_document: Optional[str] = Field(None, max_length=50)
    n_document: Optional[str] = Field(None, max_length=50)
    state: Optional[bool] = True
    gender: Optional[str] = Field(None, max_length=5)
    email_verified_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    model_config = {
        "extra": "forbid",
        "json_schema_extra": {
            "example": {
                "name": "Juanito",
                "email": "juanito.perez@example.com",
                "state": 2
            }
        }
    }

# Esquema para respuesta (incluye id, timestamps y relaciones mínimas)
class UserResponse(UserBase):
    id: int
    email_verified_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "Juan",
                "surname": "Pérez",
                "email": "juan.perez@example.com",
                "email_verified_at": "2024-06-01T12:34:56",
                "avatar": "http://example.com/avatar.jpg",
                "phone": "5551234567",
                "type_document": "INE",
                "n_document": "ABC123456",
                "state": True,
                "gender": "M",
                "created_at": "2024-06-01T12:00:00",
                "updated_at": "2024-06-02T10:00:00",
                "deleted_at": None,
                "branch_id": None,
                "role_id": None
            }
        }
    }

class UserDetailsResponse(UserResponse):
    role: Optional['RoleWithPermissions'] = None
    branch: Optional['BranchResponse'] = None

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "Juan",
                "surname": "Pérez",
                "email": "juan.perez@example.com",
                "email_verified_at": "2024-06-01T12:34:56",
                "avatar": "http://example.com/avatar.jpg",
                "phone": "5551234567",
                "type_document": "INE",
                "n_document": "ABC123456",
                "state": True,
                "gender": "M",
                "created_at": "2024-06-01T12:00:00",
                "updated_at": "2024-06-02T10:00:00",
                "deleted_at": None,
                "branch": {
                    "id": 10,
                    "name": "Sucursal Centro",
                    "address": "Av. Principal 123, CDMX",
                    "is_active": True,
                    "created_at": "2024-07-01T10:15:00",
                    "updated_at": "2024-07-05T09:00:00",
                    "deleted_at": None
                },
                "role": {
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
    }

# Forward reference resolution
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..roles.schemas import RoleWithPermissions
    from ..branches.schemas import BranchResponse

