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