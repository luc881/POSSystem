from fastapi import Depends, HTTPException, APIRouter
from typing import Annotated
from sqlalchemy.orm import Session
from ...db.session import get_db
from starlette import status
from datetime import datetime, timezone

from ...models.purchases.orm import Purchase
from ...models.purchases.schemas import PurchaseResponse, PurchaseCreate, PurchaseUpdate
from ...utils.permissions import CAN_READ_PURCHASES, CAN_CREATE_PURCHASES, CAN_UPDATE_PURCHASES, CAN_DELETE_PURCHASES

from ...models.users.orm import User
from ...models.warehouses.orm import Warehouse
from ...models.branches.orm import Branch
from ...models.suppliers.orm import Supplier


db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(
    prefix="/purchases",
    tags=["Purchases"]
)

@router.get(
    "/",
    response_model=list[PurchaseResponse],
    summary="List all purchases",
    description="Retrieve all purchases currently stored in the database.",
    status_code=status.HTTP_200_OK,
    dependencies=CAN_READ_PURCHASES
)
async def read_all(db: db_dependency):
    purchases = db.query(Purchase).all()
    return purchases


@router.post(
    "/",
    response_model=PurchaseResponse,
    summary="Create a new purchase",
    description="Create a new purchase with the provided details.",
    status_code=status.HTTP_201_CREATED,
    dependencies=CAN_CREATE_PURCHASES
)
async def create(purchase: PurchaseCreate, db: db_dependency):
    # Check if the associated user exists
    user = db.query(User).filter(User.id == purchase.user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Associated user not found")

    # Check if the associated warehouse exists
    warehouse = db.query(Warehouse).filter(Warehouse.id == purchase.warehouse_id).first()
    if not warehouse:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Associated warehouse not found")

    # Check if the associated branch exists
    branch = db.query(Branch).filter(Branch.id == purchase.branch_id).first()
    if not branch:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Associated branch not found")

    # Check if the associated supplier exists
    supplier = db.query(Supplier).filter(Supplier.id == purchase.supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Associated supplier not found")

    new_purchase = Purchase(**purchase.model_dump())

    db.add(new_purchase)
    db.commit()
    db.refresh(new_purchase)
    return new_purchase