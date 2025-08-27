from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

# -----------------------
# Base schema (shared fields)
# -----------------------
class ClientBase(BaseModel):
    name: Optional[str] = Field(None, max_length=250, description="Nombre del cliente")
    surname: Optional[str] = Field(None, max_length=250, description="Apellido del cliente")
    full_name: Optional[str] = Field(None, max_length=250, description="Nombre completo del cliente")
    phone: Optional[str] = Field(None, max_length=35, description="Número telefónico")
    email: Optional[EmailStr] = Field(None, max_length=250, description="Correo electrónico")
    type_client: int = Field(..., ge=1, le=2, description="Tipo de cliente (1 = final, 2 = empresa)")
    type_document: Optional[str] = Field(None, max_length=200, description="Tipo de documento")
    n_document: Optional[str] = Field(None, max_length=100, description="Número de documento")
    birth_date: Optional[datetime] = Field(None, description="Fecha de nacimiento")
    user_id: Optional[int] = Field(None, gt=0, description="ID del usuario asociado")
    branch_id: Optional[int] = Field(None, gt=0, description="ID de la sucursal")
    state: Optional[int] = Field(1, ge=1, le=2, description="Estado (1 = activo, 2 = inactivo)")

    ubigeo_region: Optional[str] = Field(None, max_length=25, description="Código ubigeo de región")
    ubigeo_provincia: Optional[str] = Field(None, max_length=25, description="Código ubigeo de provincia")
    ubigeo_distrito: Optional[str] = Field(None, max_length=25, description="Código ubigeo de distrito")
    region: Optional[str] = Field(None, max_length=100, description="Nombre de la región")
    provincia: Optional[str] = Field(None, max_length=100, description="Nombre de la provincia")
    distrito: Optional[str] = Field(None, max_length=100, description="Nombre del distrito")
    address: Optional[str] = Field(None, max_length=250, description="Dirección")

    gender: Optional[str] = Field(None, max_length=4, description="Género del cliente")


# -----------------------
# Create schema
# -----------------------
class ClientCreate(ClientBase):
    model_config = {
        "extra": "forbid",
        "json_schema_extra": {
            "example": {
                "name": "Carlos",
                "surname": "Ramírez",
                "full_name": "Carlos Ramírez",
                "phone": "5559876543",
                "email": "carlos.ramirez@example.com",
                "type_client": 1,
                "type_document": "DNI",
                "n_document": "87654321",
                "birth_date": "1990-05-20T00:00:00",
                "gender": "M",
                "user_id": 1,
                "branch_id": 2,
                "state": 1,
                "address": "Av. Siempre Viva 742",
                "region": "Lima",
                "provincia": "Lima",
                "distrito": "Miraflores"
            }
        }
    }


# -----------------------
# Update schema (all optional)
# -----------------------
class ClientUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=250)
    surname: Optional[str] = Field(None, max_length=250)
    full_name: Optional[str] = Field(None, max_length=250)
    phone: Optional[str] = Field(None, max_length=35)
    email: Optional[EmailStr] = Field(None, max_length=250)
    type_client: Optional[int] = Field(None, ge=1, le=2)
    type_document: Optional[str] = Field(None, max_length=200)
    n_document: Optional[str] = Field(None, max_length=100)
    birth_date: Optional[datetime] = None
    user_id: Optional[int] = Field(None, gt=0)
    branch_id: Optional[int] = Field(None, gt=0)
    state: Optional[int] = Field(None, ge=1, le=2)

    ubigeo_region: Optional[str] = Field(None, max_length=25)
    ubigeo_provincia: Optional[str] = Field(None, max_length=25)
    ubigeo_distrito: Optional[str] = Field(None, max_length=25)
    region: Optional[str] = Field(None, max_length=100)
    provincia: Optional[str] = Field(None, max_length=100)
    distrito: Optional[str] = Field(None, max_length=100)
    address: Optional[str] = Field(None, max_length=250)

    gender: Optional[str] = Field(None, max_length=4)

    deleted_at: Optional[datetime] = None

    model_config = {
        "extra": "forbid",
        "json_schema_extra": {
            "example": {
                "phone": "5551112222",
                "email": "carlos.new@example.com",
                "state": 2
            }
        }
    }


# -----------------------
# Response schema
# -----------------------
class ClientResponse(ClientBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 5,
                "name": "Carlos",
                "surname": "Ramírez",
                "full_name": "Carlos Ramírez",
                "phone": "5559876543",
                "email": "carlos.ramirez@example.com",
                "type_client": 1,
                "type_document": "DNI",
                "n_document": "87654321",
                "birth_date": "1990-05-20T00:00:00",
                "gender": "M",
                "state": 1,
                "address": "Av. Siempre Viva 742",
                "region": "Lima",
                "provincia": "Lima",
                "distrito": "Miraflores",
                "created_at": "2024-07-01T10:00:00",
                "updated_at": "2024-07-05T10:30:00",
                "deleted_at": None,
                "branch_id": 2,
                "user_id": 1
            }
        }
    }


# -----------------------
# Response with relations
# -----------------------
class ClientDetailsResponse(ClientResponse):
    user: Optional["UserResponse"] = None
    branch: Optional["BranchResponse"] = None

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 5,
                "name": "Carlos",
                "surname": "Ramírez",
                "full_name": "Carlos Ramírez",
                "email": "carlos.ramirez@example.com",
                "phone": "5559876543",
                "type_client": 1,
                "state": 1,
                "gender": "M",
                "created_at": "2024-07-01T10:00:00",
                "updated_at": "2024-07-05T10:30:00",
                "deleted_at": None,
                "branch": {
                    "id": 2,
                    "name": "Sucursal Centro",
                    "address": "Av. Principal 123, CDMX",
                    "is_active": True,
                    "created_at": "2024-06-01T12:00:00",
                    "updated_at": "2024-06-05T15:00:00",
                    "deleted_at": None
                },
                "user": {
                    "id": 1,
                    "name": "Juan",
                    "surname": "Pérez",
                    "email": "juan.perez@example.com"
                }
            }
        }
    }


# -----------------------
# Search params
# -----------------------
class ClientSearchParams(BaseModel):
    name: Optional[str] = Field(None, max_length=250, description="Filter by name")
    surname: Optional[str] = Field(None, max_length=250, description="Filter by surname")
    email: Optional[str] = Field(None, max_length=250, description="Filter by email")
    phone: Optional[str] = Field(None, max_length=35, description="Filter by phone")
    type_client: Optional[int] = Field(None, ge=1, le=2, description="Filter by type of client")
    branch_id: Optional[int] = Field(None, gt=0, description="Filter by branch ID")
    state: Optional[int] = Field(None, ge=1, le=2, description="Filter by state")

# -----------------------
# Forward references
# -----------------------
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..users.schemas import UserResponse
    from ..branches.schemas import BranchResponse
