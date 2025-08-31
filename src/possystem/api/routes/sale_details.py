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