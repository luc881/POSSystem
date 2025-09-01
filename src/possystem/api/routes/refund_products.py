from fastapi import Depends, HTTPException, APIRouter
from typing import Annotated
from sqlalchemy.orm import Session
from ...db.session import get_db
from starlette import status
from datetime import datetime, timezone

from ...models.refund_products.orm import RefundProduct
from ...models.refund_products.schemas import RefundProductCreate, RefundProductResponse, RefundProductUpdate
from ...utils.permissions import CAN_READ_REFUND_PRODUCTS, CAN_CREATE_REFUND_PRODUCTS, CAN_UPDATE_REFUND_PRODUCTS, CAN_DELETE_REFUND_PRODUCTS

from ...models.products.orm import Product
from ...models.units.orm import Unit
from ...models.warehouses.orm import Warehouse
from ...models.sale_details.orm import SaleDetail
from ...models.clients.orm import Client
from ...models.users.orm import User


db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(
    prefix="/refundproducts",
    tags=["Refund Products"]
)

@router.get(
    "/",
    response_model=list[RefundProductResponse],
    summary="List all refund products",
    description="Retrieve all refund products currently stored in the database.",
    status_code=status.HTTP_200_OK,
    dependencies=CAN_READ_REFUND_PRODUCTS
)
async def read_all(db: db_dependency):
    refund_products = db.query(RefundProduct).all()
    return refund_products


@router.post(
    "/",
    response_model=RefundProductResponse,
    summary="Create a new refund product",
    description="Create a new refund product with the provided details.",
    status_code=status.HTTP_201_CREATED,
    dependencies=CAN_CREATE_REFUND_PRODUCTS
)
async def create(refund_product: RefundProductCreate, db: db_dependency):
    # Check if the associated product exists
    product = db.query(Product).filter(Product.id == refund_product.product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Associated product not found")

    # Check if the associated unit exists (if provided)
    if refund_product.unit_id is not None:
        unit = db.query(Unit).filter(Unit.id == refund_product.unit_id).first()
        if not unit:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Associated unit not found")

    # Check if the associated warehouse exists (if provided)
    if refund_product.warehouse_id is not None:
        warehouse = db.query(Warehouse).filter(Warehouse.id == refund_product.warehouse_id).first()
        if not warehouse:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Associated warehouse not found")

    # Check if the associated sale detail exists (if provided)
    if refund_product.sale_detail_id is not None:
        sale_detail = db.query(SaleDetail).filter(SaleDetail.id == refund_product.sale_detail_id).first()
        if not sale_detail:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Associated sale detail not found")

    # Check if the associated client exists (if provided)
    if refund_product.client_id is not None:
        client = db.query(Client).filter(Client.id == refund_product.client_id).first()
        if not client:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Associated client not found")

    # Check if the associated user exists (if provided)
    if refund_product.user_id is not None:
        user = db.query(User).filter(User.id == refund_product.user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Associated user not found")

    new_refund_product = RefundProduct(**refund_product.model_dump())
    db.add(new_refund_product)
    db.commit()
    db.refresh(new_refund_product)
    return new_refund_product