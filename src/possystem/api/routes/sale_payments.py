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

@router.post(
    "/",
    response_model=SalePaymentResponse,
    summary="Create a new sale payment",
    description="Create a new sale payment with the provided details.",
    status_code=status.HTTP_201_CREATED,
    dependencies=CAN_CREATE_SALE_PAYMENTS
)
async def create(sale_payment: SalePaymentCreate, db: db_dependency):
    # Check if the associated sale exists
    sale = db.query(Sale).filter(Sale.id == sale_payment.sale_id).first()
    if not sale:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Associated sale not found")

    new_sale_payment = SalePayment(**sale_payment.model_dump())
    db.add(new_sale_payment)
    db.commit()
    db.refresh(new_sale_payment)
    return new_sale_payment