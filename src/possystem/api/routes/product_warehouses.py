from fastapi import Depends, HTTPException, APIRouter
from typing import Annotated
from sqlalchemy.orm import Session
from ...db.session import get_db
from starlette import status
from ...models.product_warehouses.orm import ProductWarehouse
from ...models.products.orm import Product
from ...models.warehouses.orm import Warehouse
from ...models.units.orm import Unit
from ...models.product_warehouses.schemas import ProductWarehouseCreate, ProductWarehouseResponse, ProductWarehouseUpdate, ProductWarehouseSearchParams, ProductWarehouseDetailsResponse
from ...utils.permissions import CAN_READ_PRODUCT_WAREHOUSES, CAN_CREATE_PRODUCT_WAREHOUSES, CAN_UPDATE_PRODUCT_WAREHOUSES, CAN_DELETE_PRODUCT_WAREHOUSES
from datetime import datetime, timezone

db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(
    prefix="/productswarehouses",
    tags=["Products Warehouses"]
)

@router.get("/",
            response_model=list[ProductWarehouseResponse],
            summary="List all product warehouses",
            description="Retrieve all product warehouses currently stored in the database.",
            status_code=status.HTTP_200_OK,
            dependencies=CAN_READ_PRODUCT_WAREHOUSES
            )
async def read_all(db: db_dependency):
    product_warehouses = db.query(ProductWarehouse).all()
    return product_warehouses

@router.post(
    "/",
    response_model=ProductWarehouseResponse,
    summary="Create a new product warehouse",
    description="Create a new product warehouse with the provided details.",
    status_code=status.HTTP_201_CREATED,
    dependencies=CAN_CREATE_PRODUCT_WAREHOUSES
)
async def create(
    product_warehouse: ProductWarehouseCreate,
    db: db_dependency
):
    # Validate product exists
    if not db.query(Product).filter_by(id=product_warehouse.product_id).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product ID does not exist.")

    # Validate warehouse exists
    if not db.query(Warehouse).filter_by(id=product_warehouse.warehouse_id).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Warehouse ID does not exist.")

    # Validate unit exists
    if not db.query(Unit).filter_by(id=product_warehouse.unit_id).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unit ID does not exist.")

    # Check for existing product-warehouse-unit combination
    existing_pw = db.query(ProductWarehouse).filter_by(
        product_id=product_warehouse.product_id,
        warehouse_id=product_warehouse.warehouse_id,
        unit_id=product_warehouse.unit_id
    ).first()
    if existing_pw:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This product is already assigned to this warehouse with the same unit."
        )

    # Create new ProductWarehouse record
    new_product_warehouse = ProductWarehouse(**product_warehouse.model_dump())
    db.add(new_product_warehouse)
    db.commit()
    db.refresh(new_product_warehouse)
    return new_product_warehouse

@router.put(
    "/{product_warehouse_id}",
    response_model=ProductWarehouseResponse,
    summary="Update an existing product warehouse",
    description="Update the details of an existing product warehouse.",
    status_code=status.HTTP_200_OK,
    dependencies=CAN_UPDATE_PRODUCT_WAREHOUSES
)
async def update(
    product_warehouse_id: int,
    product_warehouse_update: ProductWarehouseUpdate,
    db: db_dependency
):
    # Fetch existing product warehouse
    product_warehouse = db.query(ProductWarehouse).filter_by(id=product_warehouse_id).first()
    if not product_warehouse:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product warehouse not found.")

    # Validate product exists if provided
    if product_warehouse_update.product_id and not db.query(Product).filter_by(id=product_warehouse_update.product_id).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product ID does not exist.")

    # Validate warehouse exists if provided
    if product_warehouse_update.warehouse_id and not db.query(Warehouse).filter_by(id=product_warehouse_update.warehouse_id).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Warehouse ID does not exist.")

    # Validate unit exists if provided
    if product_warehouse_update.unit_id and not db.query(Unit).filter_by(id=product_warehouse_update.unit_id).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unit ID does not exist.")

    # Check for duplicates (only if keys are being updated)
    if (
        product_warehouse_update.product_id or
        product_warehouse_update.warehouse_id or
        product_warehouse_update.unit_id
    ):
        new_product_id = product_warehouse_update.product_id or product_warehouse.product_id
        new_warehouse_id = product_warehouse_update.warehouse_id or product_warehouse.warehouse_id
        new_unit_id = product_warehouse_update.unit_id or product_warehouse.unit_id

        duplicate = db.query(ProductWarehouse).filter(
            ProductWarehouse.product_id == new_product_id,
            ProductWarehouse.warehouse_id == new_warehouse_id,
            ProductWarehouse.unit_id == new_unit_id,
            ProductWarehouse.id != product_warehouse_id
        ).first()
        if duplicate:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Another product warehouse with the same product, warehouse, and unit already exists."
            )

    # Apply updates
    update_data = product_warehouse_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(product_warehouse, key, value)

    db.commit()
    db.refresh(product_warehouse)
    return product_warehouse

@router.delete(
    "/{product_warehouse_id}",
    summary="Delete a product warehouse",
    description="Delete an existing product warehouse by its ID.",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=CAN_DELETE_PRODUCT_WAREHOUSES
)
async def delete(
    product_warehouse_id: int,
    db: db_dependency
):
    # Fetch existing product warehouse
    product_warehouse = db.query(ProductWarehouse).filter_by(id=product_warehouse_id).first()
    if not product_warehouse:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product warehouse not found.")

    # Soft delete by setting deleted_at
    product_warehouse.deleted_at = datetime.now(timezone.utc)
    db.commit()
    return {"detail": "Product warehouse deleted successfully."}