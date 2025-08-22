from fastapi import Depends, HTTPException, APIRouter
from typing import Annotated
from sqlalchemy.orm import Session
from ...db.session import get_db
from starlette import status
from ...models.product_stock_initials.orm import ProductStockInitial
from ...models.product_stock_initials.schemas import ProductStockInitialCreate, ProductStockInitialResponse, ProductStockInitialUpdate
from ...utils.permissions import CAN_READ_PRODUCT_STOCK_INITIALS, CAN_CREATE_PRODUCT_STOCK_INITIALS, CAN_UPDATE_PRODUCT_STOCK_INITIALS, CAN_DELETE_PRODUCT_STOCK_INITIALS
from datetime import datetime, timezone
from ...models.products.orm import Product
from ...models.units.orm import Unit
from ...models.warehouses.orm import Warehouse

db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(
    prefix="/productstockinitials",
    tags=["Products Stock Initials"]
)

@router.get(
    "/",
    response_model=list[ProductStockInitialResponse],
    summary="List all product stock initials",
    description="Retrieve all product stock initials currently stored in the database.",
    status_code=status.HTTP_200_OK,
    dependencies=CAN_READ_PRODUCT_STOCK_INITIALS
)
async def read_all(db: db_dependency):
    product_stock_initials = db.query(ProductStockInitial).all()
    return product_stock_initials

@router.post(
    "/",
    response_model=ProductStockInitialResponse,
    summary="Create a new product stock initial",
    description="Create a new product stock initial with the provided details.",
    status_code=status.HTTP_201_CREATED,
    dependencies=CAN_CREATE_PRODUCT_STOCK_INITIALS
)
async def create(
    product_stock_initial: ProductStockInitialCreate,
    db: db_dependency
):
    # Validate product exists
    if not db.query(Product).filter_by(id=product_stock_initial.product_id).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product ID does not exist.")
    # Validate unit exists
    if not db.query(Unit).filter_by(id=product_stock_initial.unit_id).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unit ID does not exist.")
    # Validate warehouse exists
    if not db.query(Warehouse).filter_by(id=product_stock_initial.warehouse_id).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Warehouse ID does not exist.")

    # Check for existing product-stock-initial combination
    existing_psi = db.query(ProductStockInitial).filter_by(
        product_id=product_stock_initial.product_id,
        unit_id=product_stock_initial.unit_id,
        warehouse_id=product_stock_initial.warehouse_id
    ).first()

    if existing_psi:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product stock initial already exists for this product, unit, and warehouse.")

    new_product_stock_initial = ProductStockInitial(
        product_id=product_stock_initial.product_id,
        unit_id=product_stock_initial.unit_id,
        warehouse_id=product_stock_initial.warehouse_id,
        price_unit_avg=product_stock_initial.price_unit_avg,
        stock=product_stock_initial.stock,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )

    db.add(new_product_stock_initial)
    db.commit()
    db.refresh(new_product_stock_initial)

    return new_product_stock_initial

@router.put(
    "/{product_stock_initial_id}",
    response_model=ProductStockInitialResponse,
    summary="Update an existing product stock initial",
    description="Update the details of an existing product stock initial.",
    status_code=status.HTTP_200_OK,
    dependencies=CAN_UPDATE_PRODUCT_STOCK_INITIALS
)
async def update(
    product_stock_initial_id: int,
    product_stock_initial: ProductStockInitialUpdate,
    db: db_dependency
):
    existing_stock_initial = db.query(ProductStockInitial).filter_by(id=product_stock_initial_id).first()

    if not existing_stock_initial:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product stock initial not found.")

    # Validate product exists
    if not db.query(Product).filter_by(id=product_stock_initial.product_id).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product ID does not exist.")
    # Validate unit exists
    if not db.query(Unit).filter_by(id=product_stock_initial.unit_id).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unit ID does not exist.")
    # Validate warehouse exists
    if not db.query(Warehouse).filter_by(id=product_stock_initial.warehouse_id).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Warehouse ID does not exist.")

    # Check for duplicates (only if keys are being updated)
    if any([
        product_stock_initial.product_id != existing_stock_initial.product_id,
        product_stock_initial.unit_id != existing_stock_initial.unit_id,
        product_stock_initial.warehouse_id != existing_stock_initial.warehouse_id
    ]):
        duplicate_check = db.query(ProductStockInitial).filter_by(
            product_id=product_stock_initial.product_id,
            unit_id=product_stock_initial.unit_id,
            warehouse_id=product_stock_initial.warehouse_id
        ).first()

        if duplicate_check and duplicate_check.id != existing_stock_initial.id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product stock initial already exists for this product, unit, and warehouse.")
    # Update fields
    existing_stock_initial.product_id = product_stock_initial.product_id
    existing_stock_initial.unit_id = product_stock_initial.unit_id
    existing_stock_initial.warehouse_id = product_stock_initial.warehouse_id
    existing_stock_initial.price_unit_avg = product_stock_initial.price_unit_avg
    existing_stock_initial.stock = product_stock_initial.stock
    existing_stock_initial.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(existing_stock_initial)
    return existing_stock_initial

@router.delete(
    "/{product_stock_initial_id}",
    summary="Delete a product stock initial",
    description="Delete a product stock initial by its ID.",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=CAN_DELETE_PRODUCT_STOCK_INITIALS
)
async def delete(
    product_stock_initial_id: int,
    db: db_dependency
):
    existing_stock_initial = db.query(ProductStockInitial).filter_by(id=product_stock_initial_id).first()

    if not existing_stock_initial:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product stock initial not found.")

    db.delete(existing_stock_initial)
    db.commit()
    return {"detail": "Product stock initial deleted successfully."}