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