from fastapi import Depends, HTTPException, APIRouter, Query
from sqlalchemy.orm import Session
from typing import Annotated
from ...db.session import get_db
from passlib.context import CryptContext
from starlette import status
from ...models.warehouses.schemas import WarehouseBase, WarehouseCreate, WarehouseUpdate, WarehouseResponse, WarehouseDetailsResponse, WarehouseSearchParams
from ...utils.permissions import CAN_READ_WAREHOUSES, CAN_CREATE_WAREHOUSES, CAN_UPDATE_WAREHOUSES, CAN_DELETE_WAREHOUSES
from ...models.warehouses.orm import Warehouse


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
db_dependency = Annotated[Session, Depends(get_db)]


router = APIRouter(
    prefix="/warehouses",
    tags=["Warehouses"]
)

@router.get('/',
            response_model=list[WarehouseResponse],
            summary="List all warehouses",
            description="Retrieve all warehouses currently stored in the database.",
            status_code=status.HTTP_200_OK,
            dependencies=CAN_READ_WAREHOUSES
            )
async def read_all(db: db_dependency):
    warehouses = db.query(Warehouse).all()
    return warehouses

@router.post('/',
            response_model=WarehouseResponse,
            summary="Create a new warehouse",
            description="Create a new warehouse with the provided details.",
            status_code=status.HTTP_201_CREATED,
            dependencies=CAN_CREATE_WAREHOUSES
            )
async def create_warehouse(warehouse: WarehouseCreate, db: db_dependency):
    existing_warehouse = db.query(Warehouse).filter(Warehouse.name == warehouse.name).first()
    if existing_warehouse:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Warehouse with this name already exists."
        )

    new_warehouse = Warehouse(**warehouse.model_dump())
    db.add(new_warehouse)
    db.commit()
    db.refresh(new_warehouse)
    return new_warehouse

@router.put('/{warehouse_id}',
            response_model=WarehouseResponse,
            summary="Update an existing warehouse",
            description="Update the details of an existing warehouse.",
            status_code=status.HTTP_200_OK,
            dependencies=CAN_UPDATE_WAREHOUSES
            )
async def update_warehouse(warehouse_id: int, warehouse: WarehouseUpdate, db: db_dependency):
    existing_warehouse = db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()
    if not existing_warehouse:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Warehouse not found."
        )

    if warehouse.name and warehouse.name != existing_warehouse.name:
        name_conflict = db.query(Warehouse).filter(Warehouse.name == warehouse.name).first()
        if name_conflict:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Another warehouse with this name already exists."
            )

    for key, value in warehouse.model_dump(exclude_unset=True).items():
        setattr(existing_warehouse, key, value)

    db.commit()
    db.refresh(existing_warehouse)
    return existing_warehouse

@router.delete(
    '/{warehouse_id}',
    response_model=WarehouseResponse,
    summary="Delete a warehouse",
    description="Delete a warehouse by its ID.",
    status_code=status.HTTP_200_OK,
    dependencies=CAN_DELETE_WAREHOUSES
)
async def delete_warehouse(warehouse_id: int, db: db_dependency):
    existing_warehouse = db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()
    if not existing_warehouse:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Warehouse not found."
        )

    db.delete(existing_warehouse)
    db.commit()
    return existing_warehouse