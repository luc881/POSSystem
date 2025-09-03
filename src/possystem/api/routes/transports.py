from fastapi import Depends, HTTPException, APIRouter
from typing import Annotated
from sqlalchemy.orm import Session
from ...db.session import get_db
from starlette import status
from datetime import datetime, timezone

from ...models import Transport
from ...models.transports.schemas import TransportCreate, TransportUpdate, TransportResponse
from ...utils.permissions import CAN_READ_TRANSPORTS, CAN_CREATE_TRANSPORTS, CAN_UPDATE_TRANSPORTS, CAN_DELETE_TRANSPORTS

from ...models.users.orm import User
from ...models.warehouses.orm import Warehouse


db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(
    prefix="/transports",
    tags=["Transports"]
)

@router.get(
    "/",
    response_model=list[TransportResponse],
    summary="List all transports",
    description="Retrieve all transports currently stored in the database.",
    status_code=status.HTTP_200_OK,
    dependencies=CAN_READ_TRANSPORTS
)
async def read_all(db: db_dependency):
    transports = db.query(Transport).all()
    return transports

@router.post(
    "/",
    response_model=TransportResponse,
    summary="Create a new transport",
    description="Create a new transport with the provided details.",
    status_code=status.HTTP_201_CREATED,
    dependencies=CAN_CREATE_TRANSPORTS
)
async def create(transport: TransportCreate, db: db_dependency):
    # Verify that the user exists
    user = db.query(User).filter(User.id == transport.user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Verify that the origin warehouse exists
    origin_warehouse = db.query(Warehouse).filter(Warehouse.id == transport.warehouse_origin_id).first()
    if not origin_warehouse:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Origin warehouse not found")

    # Verify that the destination warehouse exists
    destination_warehouse = db.query(Warehouse).filter(Warehouse.id == transport.warehouse_destination_id).first()
    if not destination_warehouse:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Destination warehouse not found")

    new_transport = Transport(**transport.model_dump())
    db.add(new_transport)
    db.commit()
    db.refresh(new_transport)
    return new_transport