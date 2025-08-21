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
