from fastapi import Depends, HTTPException, APIRouter
from typing import Annotated
from sqlalchemy.orm import Session
from ...db.session import get_db
from starlette import status
from datetime import datetime, timezone
from ...models.sale_payments.schemas import SalePaymentCreate, SalePaymentResponse, SalePaymentUpdate
from ...models.sale_payments.orm import SalePayment
from ...utils.permissions import CAN_READ_SALE_PAYMENTS, CAN_CREATE_SALE_PAYMENTS, CAN_UPDATE_SALE_PAYMENTS, CAN_DELETE_SALE_PAYMENTS
from ...models.sales.orm import Sale


db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(
    prefix="/salepayments",
    tags=["Sale Payments"]
)

@router.get(
    "/",
    response_model=list[SalePaymentResponse],
    summary="List all sale payments",
    description="Retrieve all sale payments currently stored in the database.",
    status_code=status.HTTP_200_OK,
    dependencies=CAN_READ_SALE_PAYMENTS
)
async def read_all(db: db_dependency):
    sale_payments = db.query(SalePayment).all()
    return sale_payments
