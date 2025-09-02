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