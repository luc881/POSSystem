from fastapi import Depends, HTTPException, APIRouter
from typing import Annotated
from sqlalchemy.orm import Session
from ...db.session import get_db
from starlette import status
from datetime import datetime, timezone
from ...models.sale_details.schemas import SaleDetailCreate, SaleDetailResponse, SaleDetailUpdate
from ...models.sale_details.orm import SaleDetail
from ...utils.permissions import CAN_READ_SALE_DETAILS, CAN_CREATE_SALE_DETAILS, CAN_UPDATE_SALE_DETAILS, CAN_DELETE_SALE_DETAILS

from ...models.sales.orm import Sale
from ...models.warehouses.orm import Warehouse
from ...models.products.orm import Product
from ...models.units.orm import Unit


db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(
    prefix="/saledetails",
    tags=["Sale Details"]
)

@router.get(
    "/",
    response_model=list[SaleDetailResponse],
    summary="List all sale details",
    description="Retrieve all sale details currently stored in the database.",
    status_code=status.HTTP_200_OK,
    dependencies=CAN_READ_SALE_DETAILS
)
async def read_all(db: db_dependency):
    sale_details = db.query(SaleDetail).all()
    return sale_details

@router.post(
    "/",
    response_model=SaleDetailResponse,
    summary="Create a new sale detail",
    description="Create a new sale detail with the provided details.",
    status_code=status.HTTP_201_CREATED,
    dependencies=CAN_CREATE_SALE_DETAILS
)
async def create(sale_detail: SaleDetailCreate, db: db_dependency):
    # Check if the associated sale exists
    sale = db.query(Sale).filter(Sale.id == sale_detail.sale_id).first()
    if not sale:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Associated sale not found")

    # Check if the associated product exists
    product = db.query(Product).filter(Product.id == sale_detail.product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Associated product not found")

    # Check if the associated product category exists (if provided)
    if sale_detail.product_category_id is not None:
        product_category = db.query(Product).filter(Product.id == sale_detail.product_category_id).first()
        if not product_category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Associated product category not found")

    # Check if the associated warehouse exists (if provided)
    if sale_detail.warehouse_id is not None:
        warehouse = db.query(Warehouse).filter(Warehouse.id == sale_detail.warehouse_id).first()
        if not warehouse:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Associated warehouse not found")

    # Check if the associated unit exists (if provided)
    if sale_detail.unit_id is not None:
        unit = db.query(Unit).filter(Unit.id == sale_detail.unit_id).first()
        if not unit:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Associated unit not found")

    new_sale_detail = SaleDetail(**sale_detail.model_dump())
    db.add(new_sale_detail)
    db.commit()
    db.refresh(new_sale_detail)
    return new_sale_detail