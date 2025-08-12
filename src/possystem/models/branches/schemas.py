from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


# ---------------------------
# Base (campos compartidos)
# ---------------------------
class BranchBase(BaseModel):
    name: str = Field(..., max_length=255, description="Nombre de la sucursal")
    address: str = Field(..., max_length=255, description="Dirección física de la sucursal")
    is_active: Optional[bool] = Field(True, description="Estado de la sucursal (True = activa, False = inactiva)")

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Sucursal Centro",
                "address": "Av. Principal 123, CDMX",
                "is_active": True
            }
        }
    }


# ---------------------------
# Create
# ---------------------------
class BranchCreate(BranchBase):
    # Si en el futuro agregas más campos que sean solo para creación, hazlo aquí.
    model_config = {
        "extra": "forbid",
        "json_schema_extra": {
            "example": {
                "name": "Sucursal Norte",
                "address": "Calle 5 #234, Monterrey",
                "is_active": True
            }
        }
    }


# ---------------------------
# Update (todos opcionales)
# ---------------------------
class BranchUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255, description="Nuevo nombre de la sucursal")
    address: Optional[str] = Field(None, max_length=255, description="Nueva dirección")
    is_active: Optional[bool] = Field(None, description="Cambiar estado (True/False)")
    deleted_at: Optional[datetime] = Field(None, description="Soft delete timestamp (solo internamente)")

    model_config = {
        "extra": "forbid",
        "json_schema_extra": {
            "example": {
                "name": "Sucursal Norte Renovada",
                "is_active": False
            }
        }
    }


# ---------------------------
# Response (lectura estándar)
# ---------------------------
class BranchResponse(BranchBase):
    id: int
    created_at: Optional[datetime] = Field(None, description="Fecha de creación")
    updated_at: Optional[datetime] = Field(None, description="Fecha de última actualización")
    deleted_at: Optional[datetime] = Field(None, description="Fecha de borrado lógico (si aplica)")

    model_config = {
        "from_attributes": True,  # Permite usar .from_orm / en Pydantic v2: from_attributes
        "json_schema_extra": {
            "example": {
                "id": 10,
                "name": "Sucursal Centro",
                "address": "Av. Principal 123, CDMX",
                "is_active": True,
                "created_at": "2024-07-01T10:15:00",
                "updated_at": "2024-07-05T09:00:00",
                "deleted_at": None
            }
        }
    }


# ---------------------------
# (Opcional) Respuesta extendida con métricas ligeras
# Útil para listados si quieres devolver conteos relacionados sin anidar objetos pesados
# ---------------------------
class BranchStatsResponse(BranchResponse):
    users_count: Optional[int] = Field(None, description="Número de usuarios asociados")
    warehouses_count: Optional[int] = Field(None, description="Número de almacenes")
    product_wallets_count: Optional[int] = Field(None, description="Número de wallets de productos")
    clients_count: Optional[int] = Field(None, description="Número de clientes")
    sales_count: Optional[int] = Field(None, description="Número de ventas")
    purchases_count: Optional[int] = Field(None, description="Número de compras")

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 10,
                "name": "Sucursal Centro",
                "address": "Av. Principal 123, CDMX",
                "is_active": True,
                "created_at": "2024-07-01T10:15:00",
                "updated_at": "2024-07-05T09:00:00",
                "deleted_at": None,
                "users_count": 12,
                "warehouses_count": 3,
                "product_wallets_count": 45,
                "clients_count": 230,
                "sales_count": 1290,
                "purchases_count": 87
            }
        }
    }


# ---------------------------
# (Opcional) Lista paginada
# ---------------------------
class BranchListResponse(BaseModel):
    total: int
    page: int
    size: int
    items: list[BranchResponse]

    model_config = {
        "json_schema_extra": {
            "example": {
                "total": 25,
                "page": 1,
                "size": 10,
                "items": [
                    {
                        "id": 1,
                        "name": "Sucursal Centro",
                        "address": "Av. Principal 123, CDMX",
                        "is_active": True,
                        "created_at": "2024-07-01T10:15:00",
                        "updated_at": "2024-07-05T09:00:00",
                        "deleted_at": None
                    }
                ]
            }
        }
    }
