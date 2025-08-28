from fastapi import Depends, HTTPException, APIRouter
from typing import Annotated
from sqlalchemy.orm import Session
from ...db.session import get_db
from starlette import status
from datetime import datetime, timezone
from ...models.sales.schemas import SaleCreate, SaleResponse, SaleUpdate
from ...utils.permissions import CAN_READ_SALES, CAN_CREATE_SALES, CAN_UPDATE_SALES, CAN_DELETE_SALES
from ...models.sales.orm import Sale
from ...models.users.orm import User
from ...models.clients.orm import Client

db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(
    prefix="/sales",
    tags=["Sales"],
)

@router.get(
    "/",
    response_model=list[SaleResponse],
    summary="List all sales",
    description="Retrieve all sales currently stored in the database.",
    status_code=status.HTTP_200_OK,
    dependencies=CAN_READ_SALES
)
async def read_all(db: db_dependency):
    sales = db.query(Sale).all()
    return sales

@router.post(
    "/",
    response_model=SaleResponse,
    summary="Create a new sale",
    description="Create a new sale with the provided details.",
    status_code=status.HTTP_201_CREATED,
    dependencies=CAN_CREATE_SALES
)
async def create(
    sale: SaleCreate,
    db: db_dependency
):
    # Validate user exists
    if not db.query(User).filter_by(id=sale.user_id).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User ID does not exist.")
    # Validate client exists
    if sale.client_id and not db.query(Client).filter_by(id=sale.client_id).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Client ID does not exist.")

    new_sale = Sale(**sale.model_dump())
    db.add(new_sale)
    db.commit()
    db.refresh(new_sale)
    return new_sale