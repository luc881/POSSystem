from fastapi import Depends, HTTPException, APIRouter
from typing import Annotated
from sqlalchemy.orm import Session
from ...db.session import get_db
from starlette import status
from datetime import datetime, timezone

from ...models.purchase_details.orm import PurchaseDetail
from ...models.purchase_details.schemas import PurchaseDetailCreate, PurchaseDetailUpdate, PurchaseDetailResponse
from ...utils.permissions import CAN_READ_PURCHASE_DETAILS, CAN_CREATE_PURCHASE_DETAILS, CAN_UPDATE_PURCHASE_DETAILS, CAN_DELETE_PURCHASE_DETAILS

from ...models.purchases.orm import Purchase
from ...models.products.orm import Product
from ...models.units.orm import Unit


db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(
    prefix="/purchasedetails",
    tags=["Purchase Details"]
)

@router.get(
    "/",
    response_model=list[PurchaseDetailResponse],
    summary="List all purchase details",
    description="Retrieve all purchase details currently stored in the database.",
    status_code=status.HTTP_200_OK,
    dependencies=CAN_READ_PURCHASE_DETAILS
)
async def read_all(db: db_dependency):
    purchase_details = db.query(PurchaseDetail).all()
    return purchase_details


@router.post(
    "/",
    response_model=PurchaseDetailResponse,
    summary="Create a new purchase detail",
    description="Create a new purchase detail with the provided information.",
    status_code=status.HTTP_201_CREATED,
    dependencies=CAN_CREATE_PURCHASE_DETAILS
)
async def create(purchase_detail: PurchaseDetailCreate, db: db_dependency):
    # Check if the associated purchase exists
    purchase = db.query(Purchase).filter(Purchase.id == purchase_detail.purchase_id).first()
    if not purchase:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Associated purchase not found")

    # Check if the associated product exists
    product = db.query(Product).filter(Product.id == purchase_detail.product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Associated product not found")

    # Check if the associated unit exists
    unit = db.query(Unit).filter(Unit.id == purchase_detail.unit_id).first()
    if not unit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Associated unit not found")

    new_purchase_detail = PurchaseDetail(**purchase_detail.model_dump())
    db.add(new_purchase_detail)
    db.commit()
    db.refresh(new_purchase_detail)
    return new_purchase_detail